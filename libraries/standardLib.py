async def removeat(name):
    return name.replace("@", "😳")

def make_4_long(input):
    while len(str(input)) < 4:
        input = "0" + str(input)
    return input