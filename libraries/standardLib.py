async def removeat(name):
    return name.replace("@", "😳")


def make_4_long(input):
    while len(str(input)) < 4:
        input = "0" + str(input)
    return input


async def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

async def invoke(self, message, command):
    prefix = await self.bot.get_prefix(message)
    message.content = prefix[-1] + command
    await self.bot.invoke(await self.bot.get_context(message))