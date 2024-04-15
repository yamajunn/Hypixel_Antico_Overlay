# import json

# from status import status
# from ai import judgment_cheater

# # path = r"/Users/chinq500/Library/Application Support/minecraft/versions/1.8.9/logs/latest.log"
# path = r"C:/Users/Owner/AppData/Roaming/.minecraft/logs/blclient/minecraft/latest.log"

# def checker(mcid, model, scaler):
#     with open('key.json') as k:
#         key = json.load(k)
#     API_KEY = key[1]
#     POLSU_KEY = key[2]
#     data, ping, mode, shop, language, met = status(mcid, API_KEY, POLSU_KEY)
#     if data != None and len(data) == 23:
#         cheater = judgment_cheater(data, model, scaler)
#         return [mcid, cheater, ping, mode, shop, language, met]
#     elif ping != None and mode != None and shop != None and language != None and met != None:
#         return [mcid, None, ping, mode, shop, language, met]
#     else:
#         return [mcid, None, None, None, None, None, None]