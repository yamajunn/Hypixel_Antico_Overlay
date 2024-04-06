# import time
# import joblib

from status import status
from ai import judgment_cheater

# path = r"/Users/chinq500/Library/Application Support/minecraft/versions/1.8.9/logs/latest.log"
path = r"C:/Users/Owner/AppData/Roaming/.minecraft/logs/blclient/minecraft/latest.log"
API_KEY = "456aa888-2e2c-4f8c-86a5-6994ab5b5941"

def checker(mcid, model, scaler):
    data, ping = status(mcid, API_KEY)
    print(data, ping)
    if data != None and len(data) == 23:
        cheater = judgment_cheater(data, model, scaler)
        return [mcid, cheater, ping]
    elif ping != None:
        return [mcid, None, ping]
# with open(path) as f:
#     while True:
#         datas = []
#         mcids = []
#         s = f.read()
#         for mcid in who(s):
#             datas.append(status(mcid, API_KEY))
#             mcids.append(mcid)
#         if datas != []:
#             cheater = judgment_cheater(datas)
#         return_list = []
#         for i in range(len(mcids)):
#             return_list.append([mcids[i], cheater[i]])
#         if return_list != []:
#             print(return_list)
#         time.sleep(1)
# with open(path) as f:
#     checker(f)