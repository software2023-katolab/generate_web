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


def waku_color(runners, pred_run_num):
    for runner in runners:
        if (runner[0] == pred_run_num):
            return runner[1]
    return 1


def gen_result_html(cursor, race_id, name, location, number, time):
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
                <div class="start-time">
                    <p>{}開始</p>
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
    """.format(name, location, number, name, time)

    apologize = """
        <div class="mitei">
            <p class="notyet">まだ予測結果はありません</p>
            <p class="notyet">レース開始の30分前に更新されます</p>
            <img class="dogeza" src="../image/yakidogeza.jpg">
        </div>
    """
    
    explanation = """
          <div class="setumei">
                <table>
                    <thead>
                        <tr>
                            <th>モデル</th>
                            <th>予測対象</th>
                            <th>過去三年分の回収率シミュレーション</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>擬似期待値型モデル</td>
                            <td>その馬の単勝オッズに順位の要素を掛け合わせた値</td>
                            <td>スコア2.7以上の馬に単勝で賭け続けた時、回収率が100%を超えました。最大で回収率は1500%となりました。成績としては一番良いモデルです。</td>
                        </tr>
                        <tr>
                            <td>的中型モデル</td>
                            <td>その馬が1位になるかどうか</td>
                            <td>スコア3.7以上の馬に単勝で賭け続けた時、回収率が100%を超えました。一番回収率のブレが少ないですが、一番回収率も小さいモデルです。</td>
                        </tr>
                        <tr>
                            <td>スピード型モデル</td>
                            <td>その馬のゴールまでの平均速度</td>
                            <td>スコア2.4以上の馬に単勝で賭け続けた時、回収率が100%を超えました。しかし、その後ブレがありスコアが高くても100%を超えない時があります。</td>
                        </tr>
                        <tr>
                            <td>スタッキング擬似期待値型モデル</td>
                            <td>その馬の単勝オッズに順位の要素を掛け合わせた値<</td>
                            <td>このモデルは三年分ではなく2023年の1月〜7月23日のレースについてシミュレーションした時、スコア2.6以上の馬に複勝で賭けると回収率が100%を超えました。スタッキングモデルの特徴は元のモデルと同じです。</td>
                        </tr>
                        <tr>
                            <td>スタッキング的中型モデル</td>
                            <td>その馬が1位になるかどうか</td>
                            <td>このモデルは三年分ではなく2023年の1月〜7月23日のレースについてシミュレーションした時、スコア1.8以上の馬に三連単でかけた場合に回収率が100%を超えました。最大で300%の回収率となりました。</td>
                        </tr>
                        <tr>
                            <td>スタッキングスピード型モデル</td>
                            <td>その馬のゴールまでの平均速度</td>
                            <td>このモデルは三年分ではなく2023年の1月〜7月23日のレースについてシミュレーションした時、スコア2.8以上の馬に単勝でかけた場合に回収率が100%を超えました。最大で250%の回収率となりました。</td>
                        </tr>
                    </tbody>
                </table>
            </div>
    """

    footer = """
        <script src="../js/addTop3Class.js"></script>
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
    runners = sorted(runners, key=lambda x: int(x[0]))
    runners = sorted(runners, key=lambda x: int(x[1]))
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
            colors[int(runner[1])-1],
            runner[1],
            runner[0],
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
        <p style="text-align: center;">最新のオッズは公式を参照してください</p>
    """
    ###############################################################################
# <h3>予測結果</h3>
    pred_table = """
    <p class="predText">予測結果</p>
    <div class="predictTable">
         <table>
             <thead>
                 <tr>
                     <th>馬番</th>
                     <th style="background-color: hsl(0, 100%, 70%);">擬似期待値型モデル</th>
                     <th style="background-color: hsl(220, 100%, 70%);">スタッキング擬似期待値型モデル</th>
                     <th style="background-color: hsl(39, 100%, 70%);">的中型モデル</th>
                     <th style="background-color: hsl(92, 100%, 70%);">スタッキング的中型モデル</th>
                     <th style="background-color: hsl(60, 100%, 75%);">スピード型モデル</th>
                     <th style="background-color: hsl(19, 100%, 75%);">スタッキングスピード型モデル</th>
                 </tr>
             </thead>
             <tbody id="data-table">
    """

    cursor.execute(
        'SELECT runners_number, model1, model2, model3, model4, model5, model6 FROM predicts where race_id={}'.format(race_id))
    predicts = cursor.fetchall()
    predicts = sorted(predicts, key=lambda x: int(x[0]))
    for predict in predicts:
        pred = """
        <tr>
            <th style="{}">{}</th>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        """.format(
            colors[int(waku_color(runners, predict[0]))-1],
            predict[0],
            round(predict[1],4),
            round(predict[2],4),
            round(predict[3],4),
            round(predict[4],4),
            round(predict[5],4),
            round(predict[6],4),
        )
        pred_table += pred

    pred_table += """
        </tbody>
    </table>
  </div>
    """

    html = head + runners_table + \
        (pred_table if len(predicts) > 0 else apologize) + explanation + footer
    return html


def main():
    conn = sqlite3.connect('./races.sqlite')
    cursor = conn.cursor()

    dates = get_dates()
    # dates[0] = "2023-06-17"
    for date in dates:
        cursor.execute("""
                    SELECT id, name, location, number, time FROM races WHERE date='{}'
        """.format(date))
        races = cursor.fetchall()

        for race in races:
            html = gen_result_html(cursor, race[0], race[1], race[2], race[3], race[4])
            f = open(
                'src/result/{}.html'.format(race[0]), 'w', encoding='utf-8')
            f.write(html)
            f.close
    conn.close()


if __name__ == "__main__":
    main()
