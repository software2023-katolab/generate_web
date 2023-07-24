import schedule
import time
import datetime

# 現在時刻を取得
current_time = datetime.datetime.now()
stop_time = current_time.replace(hour=10, minute=35, second=0)

def ex ():
    print("aa")
    return schedule.CancelJob()
    
start_times = ["10:33", "10:34"]

for start_time in start_times:
    print(start_time)
    schedule.every().day.at(start_time).do(ex)
    
while (True):
    if (datetime.datetime.now() > stop_time):
        break
    schedule.run_pending()
    time.sleep(1)