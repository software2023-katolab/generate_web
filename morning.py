import sqlite3
import pickle
import pandas as pd


location = {'01' : '札幌',
            '02' : '函館',
            '03' : '福島',
            '04' : '新潟',
            '05' : '東京',
            '06' : '中山',
            '07' : '中京' ,
            '08' : '京都',
            '09' : '阪神',
            '10' : '小倉', }

def remove_leading_zero(input_string):
    if input_string.startswith('0'):
        return str(int(input_string))
    else:
        return input_string

def morning ():
    shutuba_table = pd.read_pickle("nitiyo_score")

    
    shutuba_table = shutuba_table.astype(str) # 全体を文字列に
    shutuba_table.reset_index(inplace=True)
    shutuba_table = shutuba_table.rename(columns={'index': 'race_id'}) # インデックスを列に
    shutuba_table['race_num'] = shutuba_table['race_id'].str[-2:] # race_num列を追加
    shutuba_table['race_num'] = shutuba_table['race_num'].apply(remove_leading_zero) # レース番号を0からはじまらないように変更
    shutuba_table['開催'] = shutuba_table['開催'].replace(location) # 開催地をIDから地名
    
    conn = sqlite3.connect('races.sqlite')
    cursor = conn.cursor()
    
    
    race_table = shutuba_table.drop_duplicates(subset='race_id')[['race_id', 'date', 'race_name', 'race_num', '開催', 'start_time']]
    race_table.rename(columns={'race_id' : 'id', 
                           'race_name' : 'name',
                           'race_num' : 'number',
                           '開催' : 'location',
                           'start_time' : 'time'}, 
                  inplace=True)
    race_table.to_sql('races', conn, if_exists='append', index=None)
    
    horse_table = shutuba_table.drop_duplicates(subset='horse_id')[['horse_id', '馬名', '年齢', '性']]
    horse_table.rename(columns={'horse_id' : 'id', 
                           '馬名' : 'name',
                           '年齢' : 'age',
                           '性' : 'gender'}, 
                  inplace=True)
    
    old = pd.read_sql_query("SELECT id FROM horses", conn)  # 登録済みのidを取得
    mask = ~horse_table.iloc[:, 0].isin(old.iloc[:, 0])
    new_horse_table = horse_table[mask]
    new_horse_table.to_sql('horses', conn, if_exists='append', index=None)
    
    runner_table = shutuba_table[['race_id', '馬番', '枠番', '騎手名', '単勝', 'horse_id']].copy()
    runner_table.rename(columns={'馬番' : 'number', 
                             '枠番' : 'position',
                             '騎手名' : 'jockey',
                             '単勝' : 'odds'}, 
                  inplace=True)
    runner_table.to_sql('runners', conn, if_exists='append', index=None)
    
    conn.close()