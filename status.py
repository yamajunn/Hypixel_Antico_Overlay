import time
import requests
import pprint
import json

dic_labels = [
    # 'karma',
    'networkExp',
    ]
achievements = [
    # 'bedwars_beds',
    # 'bedwars_bedwars_challenger',
    # 'bedwars_bedwars_killer',
    # 'bedwars_collectors_edition',
    'bedwars_level',
    # 'bedwars_loot_box',
    # 'bedwars_slumber_ticket_master',
    # 'bedwars_wins',
    ]
challenges = [
    # 'challenges',
    # 'all_time',
    # 'BEDWARS__defensive',
    # 'BEDWARS__offensive',
    # 'BEDWARS__support',
    ]
statuses = [
    # 'Bedwars_openedChests',
    'Experience',
    # '_items_purchased_bedwars',
    'beds_broken_bedwars',
    'beds_lost_bedwars',
    'coins',
    'deaths_bedwars',
    'diamond_resources_collected_bedwars',
    'emerald_resources_collected_bedwars',
    # 'fall_deaths_bedwars',
    # 'fall_final_deaths_bedwars',
    # 'fall_final_kills_bedwars',
    # 'fall_kills_bedwars',
    'final_deaths_bedwars',
    'final_kills_bedwars',
    'games_played_bedwars',
    'games_played_bedwars_1',
    'kills_bedwars',
    'losses_bedwars',
    # 'void_deaths_bedwars',
    'void_final_deaths_bedwars',
    # 'void_final_kills_bedwars',
    # 'void_kills_bedwars',
    'wins_bedwars',
    ]

def getinfo(call):
    try:
        r = requests.get(call, timeout=10)
        r.raise_for_status()  # エラーがあれば例外を発生させる
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_shop(data_dic):
    if "success" in data_dic and data_dic["success"] == True and "player" in data_dic and data_dic["player"] != None and "stats" in data_dic["player"] and "Bedwars" in data_dic["player"]["stats"] and "favourites_2" in data_dic["player"]["stats"]["Bedwars"]:
        return len(set(data_dic["player"]["stats"]["Bedwars"]["favourites_2"].split(",")) & set(["golden_apple", "fireball", "diamond_boots"]))
def get_language(data_dic):
    if "success" in data_dic and data_dic["success"] == True and "player" in data_dic and data_dic["player"] != None and "userLanguage" in data_dic["player"]:
        return data_dic["player"]["userLanguage"]
def get_status(uuid, API_KEY):
    uuid_link = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
    data_dic = getinfo(uuid_link)
    # pprint.pprint(data_dic)
    datas = []
    if data_dic != None:
        if "cause" in data_dic and data_dic["cause"] == "Key throttle":
            time.sleep(5)
        if "success" in data_dic and data_dic["success"] == True and "player" in data_dic and data_dic["player"] != None:
            for dic_label in dic_labels:
                if dic_label in data_dic["player"]:
                    datas.append(data_dic["player"][dic_label])
                else:
                    datas.append(0)
            for achievement in achievements:
                if 'achievements' in data_dic["player"] and achievement in data_dic["player"]['achievements']:
                    datas.append(data_dic["player"]['achievements'][achievement])
                else:
                    datas.append(0)
            for challenge in challenges:
                if 'challenges' in data_dic["player"] and 'all_time' in data_dic["player"]['challenges'] and challenge in data_dic["player"]['challenges']['all_time']:
                    datas.append(data_dic["player"]['challenges']['all_time'][challenge])
                else:
                    datas.append(0)
            for stats in statuses:
                if 'stats' in data_dic["player"] and 'Bedwars' in data_dic["player"]['stats'] and stats in data_dic["player"]['stats']['Bedwars']:
                    datas.append(data_dic["player"]['stats']['Bedwars'][stats])
                else:
                    datas.append(0)
            for a in range(len(datas)):
                # if a in [27,32,18,6]:
                if a in [9, 14, 4, 1]:
                    if datas[a] == 0:
                        datas[a] = 1
            # for j in [datas[28] / datas[27], datas[37] / datas[32], datas[17] / datas[18], datas[28] / datas[6], datas[31] / datas[6], datas[17] / datas[6]]:
            for j in [datas[10] / datas[9], datas[16] / datas[14], datas[3] / datas[4], datas[10] / datas[1], datas[13] / datas[1], datas[3] / datas[1]]:
                datas.append(j)
        return [datas, get_shop(data_dic), get_language(data_dic)]
    else:
        return [None, None, None]
    
def games(uuid, API_KEY):
    games_link = f"https://api.hypixel.net/v2/recentgames?key={API_KEY}&uuid={uuid}"
    data_dic = getinfo(games_link)
    modes = []
    game_nums = []
    if data_dic != None and "games" in data_dic:
        if len(data_dic["games"]) == 3:
            modes.append(data_dic["games"][0]["gameType"])
            modes.append(data_dic["games"][1]["gameType"])
            modes.append(data_dic["games"][2]["gameType"])
        if len(data_dic["games"]) == 2:
            modes.append(data_dic["games"][0]["gameType"])
            modes.append(data_dic["games"][1]["gameType"])
        if len(data_dic["games"]) == 1:
            modes.append(data_dic["games"][0]["gameType"])
        for mode in modes:
            if mode == "BEDWARS":
                game_nums.append(0)
            elif mode == "SKYWARS":
                game_nums.append(1)
            elif mode == "TNTGAMES":
                game_nums.append(2)
            elif mode == "UHC":
                game_nums.append(3)
            elif mode == "MURDER_MYSTERY":
                game_nums.append(4)
            elif mode == "BUILD_BATTLE":
                game_nums.append(5)
            elif mode == "DUELS":
                game_nums.append(6)
            elif mode == "SKYBLOCK":
                game_nums.append(7)
            elif mode == "PIT":
                game_nums.append(8)
            else:
                game_nums.append(9)
    return game_nums

def pols(uuid):
    url = "https://api.polsu.xyz/polsu/ping"
    querystring = {"uuid":f"{uuid}"}
    headers = {"Api-Key": "a5759d02-94e9-466a-8e40-6679b1ccb256"}

    response = requests.get(url, headers=headers, params=querystring)

    pings = response.json()
    if pings != None and "success" in pings and pings["success"] == True and "data" in pings and "history" in pings["data"] and len(pings["data"]["history"]) != 0:
        ping = pings["data"]["history"][0]["ping"]
    else:
        ping = "???"
    return ping

def status(name, API_KEY):
    name_link = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    info = getinfo(name_link)
    if info != None and "id" in info:
        uuid = info["id"]
        return [get_status(uuid, API_KEY)[0], pols(uuid), games(uuid, API_KEY), get_status(uuid, API_KEY)[1], get_status(uuid, API_KEY)[2], uuid]
    else:
        return [None, None, None, None, None, None]

# API_KEY = "456aa888-2e2c-4f8c-86a5-6994ab5b5941"
# name = "Gokiton"
# print(status(name, API_KEY))

# names = ["Gokiton", "Hakuryu_999", "vrukz", "DragonCrane87"]
# print("[")
# for i in names:
#     print(f"{status(i, API_KEY)[0]},")
# print("]")
# print(dic_labels + achievements + challenges + statuses)
# print(len(dic_labels + achievements + challenges + statuses))

# print(pols())