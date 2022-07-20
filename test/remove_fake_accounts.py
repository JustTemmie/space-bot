import json

if __name__ == '__main__':
    
    with open ('./storage/playerInfo/bank.json', 'r') as f:
        data = json.load(f)
        
    print(len(data))

    removes = []
    what = []
    for user in data:
        try:
            if round(data[user]["wallet"]) <= 100 and round(data[user]["inventory"]["logs"]) < 1 and round(data[user]["dam"]["spent"]["logs"]) < 1 and round(data[user]["dam"]["level"]) == 0 and data[user]["marriage"] == {}:
                    removes.append(user)
        except:
            try:
                if round(data[user]["wallet"]) <= 20:
                    removes.append(user)
            except:
                what.append(user)

    for user in removes:
        data.pop(user)

    for user in what:
        print(data[user])
        print("---------------------")

    print(len(data))
    
    #for user in data:
    #    print(data[user]["wallet"])
    
    with open ('./storage/playerInfo/bank.json', 'w') as f:
        json.dump(data, f)
