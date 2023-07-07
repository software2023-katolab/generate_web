import sqlite3
import datetime


def get_dates():
    today = datetime.date.today()
    current_weekday = today.weekday()
    last_saturday = today - datetime.timedelta(days=current_weekday + 2)
    last_saturday = last_saturday.strftime('%Y-%m-%d')
    last_sunday = today - datetime.timedelta(days=current_weekday + 1)
    last_sunday = last_sunday.strftime('%Y-%m-%d')
    this_sunday = today + datetime.timedelta(days=6 - current_weekday)
    this_sunday = this_sunday.strftime('%Y-%m-%d')
    this_saturday = today + datetime.timedelta(days=5 - current_weekday)
    this_saturday = this_saturday.strftime('%Y-%m-%d')

    return [last_saturday, last_sunday, this_saturday, this_sunday]


def gen_result_html(cursor, race_id, name, location, number):
    head = """
    <!-- ２ページ目 -->
    <!DOCTYPE html>
    <html>
        <head>
            <title>{}</title>
            <style src="style.css"></style>
        </head>

        <body>
        
            <header class="header">
                <div class="header-inner">
                    <a class="header-logo" href="../this_sat.html">
                        <img class="logo" src="../image/katomusume_clear.png') }}">
                    </a>
                </div>
                <div class="race-info">
                    <p>{} {}R:{}</p>
                </div>
            </header>    
        
            <h1>name: {}</h2>
            <h2>location: {}</h2>
            <table>
                <thead>
                    <tr>
                        <th>枠</th>
                        <th>馬番</th>
                        <th>馬名</th>
                        <th>性齢</th>
                        <th>騎手</th>
                        <th>予想オッズ</th>
                    </tr>
                </thead>
                <tbody>
    """.format(name, location, number, name, name, location)
    column = """
                </tbody>
            </table>
            
            <h3>予測結果</h3>
            <table>
                <thead>
                    <tr>
                        <th></th>
                        <th>単勝</th>
                        <th>複勝</th>
                        <th>枠連</th>
                        <th>馬連</th>
                        <th>馬単</th>
                        <th>ワイド</th>
                        <th>3連単</th>
                        <th>3連複</th>
                    </tr>
                </thead>
                <tbody>
    """
    foot = """
                </tbody>
            </table>
        </body>
    </html>
    """

    ###############################################################################
    cursor.execute("""
                SELECT 
                        number, position, name, gender, age, jockey, odds
                FROM 
                        runners inner join horses 
                ON 
                        runners.horse_id = horses.id
                WHERE
                        race_id = {}

    """.format(race_id))
    runners = cursor.fetchall()
    runners_table = ""
    for runner in runners:
        row = """
        <tr>
            <td>枠番：{}</td>
            <td>馬番：{}</td>
            <td>馬名：{}</td>
            <td>性齢：{}{}</td>
            <td>騎手：{}</td>
            <td>予想オッズ：{}</td>
        </tr>
        """.format(
            runner[0],
            runner[1],
            runner[2],
            runner[3],
            runner[4],
            runner[5],
            runner[6],
        )
        runners_table += row
    ###############################################################################
    pred_table = ""
    for i in range(1, 6):
        pred_head = """
        <tr>
            <th>{}</th>
        """.format(i)

        pred_foot = """
        </tr>
        """.format(i)

        pred_kinds = ""
        cursor.execute(
            'SELECT kind, rank, forecast, payoff FROM predicts where race_id={}'.format(race_id))
        predicts = cursor.fetchall()
        for predict in predicts:
            if predict[1] == i:
                pred = """
                    <td>{}<br>{}<br>{}<br>{}</td>
                """.format(
                    predict[0],
                    predict[1],
                    predict[2],
                    predict[3],
                )
                pred_kinds += pred

        pred_table += pred_head + pred_kinds + pred_foot
        
    footer = """
            <footer>
                <div class="caution">
                    <ul>
                        <li>(注)本サイトはあくまで競馬の結果を予測するものであり、結果を保証するものではありません。</li>
                        <li>&emsp;&nbsp;&nbsp;&thinsp;本サイトが提供するいかなるサービスを利用したことにより利用者に発生した損害について</li>
                        <li>&emsp;&nbsp;&nbsp;&thinsp;本サービス提供者は一切賠償責任を負いません。</li>
                        <li>&emsp;&nbsp;&nbsp;&thinsp;馬券の購入はご自身の判断で行ってください。</li>
                    </ul>
                    
                    <a class="returnpage" href="{{ url_for('this_saturday') }}">
                        <p>トップページへ</p>
                    </a>
                </div>
            </footer>
        """

    html = head + runners_table + column + pred_table + foot + footer
    return html


def main():
    conn = sqlite3.connect('./races.sqlite')
    cursor = conn.cursor()

    dates = get_dates()
    # dates[0] = "2023-06-17"
    for date in dates:
        cursor.execute("""
                    SELECT id, name, location, number FROM races WHERE date='{}'
        """.format(date))
        races = cursor.fetchall()

        for race in races:
            html = gen_result_html(cursor, race[0], race[1], race[2], race[3])
            f = open(
                'src/result/{}.html'.format(race[0]), 'w', encoding='utf-8')
            f.write(html)
            f.close
    conn.close()


if __name__ == "__main__":
    main()
