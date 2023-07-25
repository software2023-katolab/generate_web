import sqlite3
import pickle
import pandas as pd

def before30 ():
    shutuba_table = pd.read_pickle("nitiyo_score")
    # shutuba_table.drop(columns=['斤量','jockey_id', 'trainer_id', '体重'\
    #                             , '体重変化', 'n_horses', 'course_len', 'weather' \
    #                             , 'race_type', 'ground_state', 'around'], inplace=True)
    
    shutuba_table = shutuba_table.astype(str) # 全体を文字列に
    shutuba_table.reset_index(inplace=True)
    shutuba_table = shutuba_table.rename(columns={'index': 'race_id'}) # インデックスを列に
    
    conn = sqlite3.connect('races.sqlite')
    cursor = conn.cursor()
    
    
    runner_table = shutuba_table[['race_id', '馬番', '枠番', '騎手名', '単勝', 'horse_id']].copy()
    # runner_table = shutuba_table[['race_id', '馬番', '枠番', '騎手名', '単勝', 'horse_id']].copy()
    runner_table.rename(columns={'馬番' : 'number', 
                                '枠番' : 'position',
                                '騎手名' : 'jockey',
                                '単勝' : 'odds'}, 
                    inplace=True)
    
    ids = shutuba_table['race_id'].unique()
    for i in range(ids.shape[0]):
        conn.execute("DELETE from runners where race_id=?;", (ids[i],))
    conn.commit()
    
    # 新しいオッズにするために、該当のrace_idのデータを一度すべて消して新しく書き込む
    for i in range(ids.shape[0]):
        new_odds_table = runner_table[runner_table['race_id'] == ids[i]]
        new_odds_table.to_sql('runners', conn, if_exists='append', index=None)
        
    pred_table = shutuba_table[['race_id', '馬番', 'oddsrank_score', 'rank1to1_score', 'speed_score', '開催']].copy()
    pred_table.rename(columns={'馬番' : 'runners_number', 
                                'oddsrank_score' : 'model1',
                                'rank1to1_score' : 'model2',
                                'speed_score' : 'model3',
                                #   'モデル4' : 'model4'
                                '開催' : 'model4',}, 
                        inplace=True)
    
    pred_table.to_sql('predicts', conn, if_exists='append', index=None)

    conn.close()