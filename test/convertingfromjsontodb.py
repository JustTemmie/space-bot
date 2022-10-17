import json
import sqlite3

connection = sqlite3.connect("./storage/db/database.db")
cur = connection.cursor()

cur.execute("SELECT * FROM playerData")
print(cur.fetchone())

# marriage = {
#     "marriage": {
#             "338627190956490753": {
#                 "married": True,
#                 "married_to": 338627190956490753,
#                 "time": 1652298434.787113,
#                 "ring": "common"
#             },
#             "765222621779853312": {
#                 "married": True,
#                 "married_to": 765222621779853312,
#                 "time": 1653334453.5179198,
#                 "ring": "common"
#             },
#             "705399466710007908": {
#                 "married": True,
#                 "married_to": 705399466710007908,
#                 "time": 1653640278.2675602,
#                 "ring": "common"
#             },
#             "689565874612469784": {
#                 "married": False,
#                 "married_to": None,
#                 "time": 0
#             },
#             "398181370725400577": {
#                 "married": True,
#                 "married_to": 398181370725400577,
#                 "time": 1654585921.8575413,
#                 "ring": "common"
#             },
#             "248859702547578881": {
#                 "married": True,
#                 "married_to": 248859702547578881,
#                 "time": 1654598446.105668,
#                 "ring": "common"
#             },
#             "297448834102198272": {
#                 "married": True,
#                 "married_to": 297448834102198272,
#                 "time": 1655141263.3201692,
#                 "ring": "common"
#             }
#         }
#     }

# cur.execute(f"""
# UPDATE playerData
# SET QUOTE='hi'
# WHERE UserID=368423564229083137;
# """)

entries = [
    "WALLET",
    "XP",
    "SPOKE_DAY",
    "SPOKEN_TODAY",
    "SPEAK_COOLDOWN",
    "SCAVENGE_COOLDOWN",
    "QUOTE",
]
f = json.load(open("./storage/playerInfo/bank.json"))
for entry in f:
    # cur.execute("INSERT INTO playerData VALUES (?,?,?,?,?,?,?,?)",
    #         (entry,
    #         f[entry]["wallet"],
    #         f[entry]["xp"],
    #         f[entry]["spoke_day"],
    #         f[entry]["spoken_today"],

    #         f[entry]["speak_cooldown"],
    #         f[entry]["scavenge_cooldown"],

    #         f[entry]["quote"]
    #     )
    # )
    for j, i in enumerate(entries):
        print(j, i)

        cur.execute(
            f"""
        UPDATE playerData
        SET {i}='{f[entry][str(entries[j]).lower()]}'
        WHERE UserID={entry};
        """
        )
        connection.commit()

#         print(i, f[entry][i.lower()])
# print(entry)
# print(f[entry]["version"])

# print(f[entry]["wallet"])
# print(f[entry]["xp"])
#     print(f[entry]["spoke_day"])
#     print(f[entry]["spoken_today"])

#     print(f[entry]["speak_cooldown"])
#     print(f[entry]["scavenge_cooldown"])

#     print(f[entry]["quote"])


#     print(f[entry]["marriage"])
#     print(f[entry]["inventory"])
#     print(f[entry]["daily"])
#     print(f[entry]["stats"])
#     print(f[entry]["dam"])
#     print(f[entry]["lodge"])
#     print(f[entry]["dailyvote"])
#     print(f[entry]["anti-cheat"])

connection.commit()
connection.close()
