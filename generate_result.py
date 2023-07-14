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
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="../css/style.css">
            <title>{}</title>
        </head>

        <body>

            <header class="header">
                <div class="header-inner">
                    <a class="header-logo" href="../this_sat.html">
                        <img class="logo" src="../image/katomusume_clear.png">
                    </a>
                </div>
                <div class="race-info">
                    <p>{} {}R:{}</p>
                </div>
            </header>

            <script src="../js/logo_resize.js"></script>

            <div class="raceCard">
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

    apologize = """
        <div class="mitei">
            <p class="notyet">まだ予測結果はありません</p>
            <div class="leftTime">
                <p>
                    予想結果更新まで残り <span id="left_days"></span>日 <span id="left_hours"></span>時間
                    <span id="left_mins"></span>分 <span id="left_secs"></span>秒
                </p>
                <script src="../js/countdown.js"></script>
            </div>
            <img class="dogeza" src="../image/pose_syazai_man.png">
        </div>
    """

    pred_footer = """
            </tbody>
        </table>
    """

    footer = """
        <script src="../js/zawazawa.js"></script>
            <footer>
                <div class="caution">
                    <ul>
                        <li>(注)本サイトはあくまで競馬の結果を予測するものであり、結果を保証するものではありません。</li>
                        <li>&emsp;&nbsp;&nbsp;&thinsp;本サイトが提供するいかなるサービスを利用したことにより利用者に発生した損害について</li>
                        <li>&emsp;&nbsp;&nbsp;&thinsp;本サービス提供者は一切賠償責任を負いません。</li>
                        <li>&emsp;&nbsp;&nbsp;&thinsp;馬券の購入はご自身の判断で行ってください。</li>
                    </ul>

                    <a class="returnpage" href="../this_sat.html">
                        <p>トップページへ</p>
                    </a>
                </div>
            </footer>
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
    colors = [
        "background-color: white;",
        "color: white; background-color: black;",
        "background-color: red;",
        "background-color: blue;",
        "background-color: yellow;",
        "background-color: green;",
        "background-color: orange;",
        "background-color: pink;",
        ]
    for runner in runners:
        row = """
        <tr>
            <td style="{}">{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        """.format(
            colors[runner[0]-1],
            runner[0],
            runner[1],
            runner[2],
            runner[3],
            runner[4],
            runner[5],
            runner[6],
        )
        runners_table += row

    runners_table += """
                    </tbody>
            </table>
        </div>
    """
    ###############################################################################
# <h3>予測結果</h3>
    pred_table = """
         <table>
             <thead>
                 <tr>
                     <th>馬番</th>
                     <th>モデル1</th>
                     <th>モデル2</th>
                     <th>モデル3</th>
                     <th>モデル4</th>
                     <th>モデル5</th>
                     <th>モデル6</th>
                     <th>モデル7</th>
                     <th>モデル8</th>
                 </tr>
             </thead>
             <tbody>
    """

    cursor.execute(
        'SELECT runners_number, model1, model2, model3, model4, model5, model6, model7, model8 FROM predicts where race_id={}'.format(race_id))
    predicts = cursor.fetchall()
    for predict in predicts:
        pred = """
        <tr>
            <th>{}</th>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        """.format(
            predict[0],
            predict[1],
            predict[2],
            predict[3],
            predict[4],
            predict[5],
            predict[6],
            predict[7],
            predict[8],
        )
        pred_table += pred

    pred_table += """
        </tbody>
    </table>
    """

    html = head + runners_table + (pred_table if len(predicts) > 0 else apologize) + footer
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
