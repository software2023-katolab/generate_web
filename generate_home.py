import sqlite3
import datetime

conn = sqlite3.connect('races.sqlite')
cursor = conn.cursor()

# 先週・今週と土曜・日曜の日時を取得
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

dates = [last_saturday, last_sunday, this_saturday, this_sunday, ]

# 各日のレース情報を取得
cursor.execute("SELECT * FROM races WHERE date = '" + last_saturday + "'")
last_sat_data = cursor.fetchall()
cursor.execute("SELECT * FROM races WHERE date = '" + last_sunday + "'")
last_sun_data = cursor.fetchall()
cursor.execute("SELECT * FROM races WHERE date = '" + this_saturday + "'")
this_sat_data = cursor.fetchall()
cursor.execute("SELECT * FROM races WHERE date = '" + this_sunday + "'")
this_sun_data = cursor.fetchall()

conn.close()

# 静的
html1 = """<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"""
    
# title

html2 = """</title>
    <link rel="stylesheet" href='css/style.css'>
</head>

<body>
    <header class="header">
        <p class="weekTitle">AIによる競馬の結果予想</p>
        <div class="header-inner">
            <a class="header-logo" href="this_sat.html">
                <img id="logo-img" class="logo" src="image/katomusume_clear.png">
            </a>    
        </div>
    </header>
    
    <script src="js/logo_resize.js"></script>
"""

# button
# rtOOO or mitei

mitei = """
    <div class="mitei">
        <p class="notyet">レース情報は当日朝に更新されます</p>
        <img class="dogeza" src="image/pose_syazai_man.png">
    </div>
"""

html3 = """
    <footer>
        <div class="caution">
            <ul>
                <li>(注)本サイトはあくまで競馬の結果を予測するものであり、結果を保証するものではありません。</li>
                <li>&emsp;&nbsp;&nbsp;&thinsp;本サイトが提供するいかなるサービスを利用したことにより利用者に発生した損害について</li>
                <li>&emsp;&nbsp;&nbsp;&thinsp;本サービス提供者は一切賠償責任を負いません。</li>
                <li>&emsp;&nbsp;&nbsp;&thinsp;馬券の購入はご自身の判断で行ってください。</li>
            </ul>
            
            <a class="returnpage" href="this_sat.html">
                <p>トップページへ</p>
            </a>
        </div>
    </footer>
</body>

</html>
"""

# 動的
title = ["先週土曜", "先週日曜", "今週土曜", "今週日曜",]

button_last_sat = """
    <div class="dateButtons">
        <div class="weekButtons">
            <a class="pushed"><span>先週</span></a>
            <a class="btn btn-border" href="this_sat.html"><span>今週</span></a>
        </div>

        <div class="dayButtons">
            <a class="pushed"><span>土曜</span></a>
            <a class="btn btn-border" href="last_sun.html"><span>日曜</span></a>
        </div>
    </div>
"""

button_last_sun = """
    <div class="dateButtons">
        <div class="weekButtons">
            <a class="pushed"><span>先週</span></a>
            <a class="btn btn-border" href="this_sun.html"><span>今週</span></a>
        </div>

        <div class="dayButtons">
            <a class="btn btn-border" href="last_sat.html"><span>土曜</span></a>
            <a class="pushed"><span>日曜</span></a>
        </div>
    </div>
"""

button_this_sat = """
    <div class="dateButtons">
        <div class="weekButtons">
            <a class="btn btn-border" href="last_sat.html"><span>先週</span></a>
            <a class="pushed"><span>今週</span></a>
        </div>

        <div class="dayButtons">
            <a class="pushed"><span>土曜</span></a>
            <a class="btn btn-border" href="this_sun.html"><span>日曜</span></a>
        </div>
    </div>
"""

button_this_sun = """
    <div class="dateButtons">
        <div class="weekButtons">
            <a class="btn btn-border" href="last_sun.html"><span>先週</span></a>
            <a class="pushed"><span>今週</span></a>
        </div>

        <div class="dayButtons">
            <a class="btn btn-border" href="this_sat.html"><span>土曜</span></a>
            <a class="pushed"><span>日曜</span></a>
        </div>
    </div>
"""

rt_last_sat = """
<h2 class="raceTableTitle">レース一覧({})</h1>
<div class="raceTable">""".format(last_saturday)

location = list(set(row[4] for row in last_sat_data))

for loc in location:
    for1 = """
        <ul>
        <li class="location">{}</li>""".format(loc)
    for race in last_sat_data:
        if race[4] == loc:
            racedata = """
                    <li class="'raceData"><a href="result/{}.html">{}R:{}</a></li>""".format(race[0],race[3], race[2])
            for1 = for1 + racedata
    rt_last_sat = rt_last_sat + for1 + """
        </ul>"""
rt_last_sat = rt_last_sat + """
</div>"""

rt_last_sun = """
<h2 class="raceTableTitle">レース一覧({})</h1>
<div class="raceTable">""".format(last_sunday)

location = list(set(row[4] for row in last_sun_data))

for loc in location:
    for1 = """
        <ul>
        <li class="location">{}</li>""".format(loc)
    for race in last_sun_data:
        if race[4] == loc:
            racedata = """
                    <li class="'raceData"><a href="result/{}.html">{}R:{}</a></li>""".format(race[0],race[3],race[2])
            for1 = for1 + racedata
    rt_last_sun = rt_last_sat + for1 + """
        </ul>"""
rt_last_sun = rt_last_sun + """
</div>"""

rt_this_sat = """
<h2 class="raceTableTitle">レース一覧({})</h1>
<div class="raceTable">""".format(this_saturday)

location = list(set(row[4] for row in this_sat_data))

for loc in location:
    for1 = """
        <ul>
        <li class="location">{}</li>""".format(loc)
    for race in this_sat_data:
        if race[4] == loc:
            racedata = """
                    <li class="'raceData"><a href="result/{}.html">{}R:{}</a></li>""".format(race[0],race[3],race[2])
            for1 = for1 + racedata
    rt_this_sat = rt_this_sat + for1 + """
        </ul>"""
rt_this_sat = rt_this_sat + """
</div>"""

rt_this_sun = """
<h2 class="raceTableTitle">レース一覧({})</h1>
<div class="raceTable">""".format(this_sunday)

location = list(set(row[4] for row in this_sun_data))

for loc in location:
    for1 = """
        <ul>
        <li class="location">{}</li>""".format(loc)
    for race in this_sun_data:
        if race[4] == loc:
            racedata = """
                    <li class="'raceData"><a href="result/{}.html">{}R:{}</a></li>""".format(race[0],race[3],race[2])
            for1 = for1 + racedata
    rt_this_sun = rt_this_sun + for1 + """
        </ul>"""
rt_this_sun = rt_this_sun + """
</div>"""

# 統合
last_sat_file = html1 + title[0] + html2 + button_last_sat + (rt_last_sat if len(last_sat_data) > 0 else mitei) + html3
                
last_sun_file = html1 + title[1] + html2 + button_last_sun + (rt_last_sun if len(last_sun_data) > 0 else mitei) + html3
                
this_sat_file = html1 + title[2] + html2 + button_this_sat + (rt_this_sat if len(this_sat_data) > 0 else mitei) + html3
                
this_sun_file = html1 + title[3] + html2 + button_this_sun + (rt_this_sun if len(this_sun_data) > 0 else mitei) + html3
                
with open('src/last_sat.html', 'w', encoding="utf-8") as f:
    f.write(last_sat_file)
    
with open('src/last_sun.html', 'w', encoding="utf-8") as f:
    f.write(last_sun_file)
    
with open('src/this_sat.html', 'w', encoding="utf-8") as f:
    f.write(this_sat_file)
    
with open('src/this_sun.html', 'w', encoding="utf-8") as f:
    f.write(this_sun_file)