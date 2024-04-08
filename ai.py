import pandas as pd

def judgment_cheater(data, model, scaler):
    columns = ['networkExp', 'bedwars_level', 'Experience', 'beds_broken_bedwars', 'beds_lost_bedwars', 'coins', 'deaths_bedwars', 'diamond_resources_collected_bedwars', 'emerald_resources_collected_bedwars', 'final_deaths_bedwars', 'final_kills_bedwars', 'games_played_bedwars', 'games_played_bedwars_1', 'kills_bedwars', 'losses_bedwars', 'void_final_deaths_bedwars',  'wins_bedwars','fkdr','wlr','bblr','fk_lev','bb_lev','kill_lev']
    scaled = pd.DataFrame([data], columns=columns)
    scaled = scaler.transform(scaled)

    y_pred = model.predict_proba(scaled)
    # print(y_pred)
    return y_pred[0][0]

# import joblib
# model = joblib.load('Cheater.pkl')
# scaler = joblib.load('scaler.joblib')
# print(judgment_cheater(
#     [
#     [6522912.0, 1, 837122, 810, 1, 751015, 9236, 2488, 1449, 1, 1994, 2544, 2991, 5444, 1, 412, 1263, 1994.0, 1263.0, 810.0, 1994.0, 5444.0, 810.0],
#     [34357269.0, 1, 6472490, 6451, 1, 11325936, 35297, 45344, 17878, 1, 19764, 15398, 18916, 43304, 1, 2660, 6826, 19764.0, 6826.0, 6451.0, 19764.0, 43304.0, 6451.0],
#     [385682, 1, 40867, 48, 1, 8295, 397, 1749, 734, 1, 157, 179, 179, 661, 1, 52, 31, 157.0, 31.0, 48.0, 157.0, 661.0, 48.0],
#     [413592.0, 1, 36767, 16, 1, 10777, 290, 1518, 330, 1, 51, 158, 162, 252, 1, 42, 33, 51.0, 33.0, 16.0, 51.0, 252.0, 16.0],
#     ]
#     ,model, scaler))
