import json

with open ('./storage/playerInfo/bank.json', 'r') as f:
    data = json.load(f)
    
print(len(data))
print(data)

def remove_fake_accounts(data):
    for user in data:
        #print(data[user])
        try:
            wal = data[user]['wallet']
        except:
            wal = 25
        if round(wal) <= 20:
            print("a")
            data = data.pop(user)
            break
    

for i in range(0, 100):
    data = remove_fake_accounts(data)

print(data)