import asyncio

async def get_input(self, ctx, time = 30):
    try:
        return await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author, timeout=time
        )
    except asyncio.TimeoutError:
        return await ctx.send(f"**Timed out** You took too long to answer the question, Please try again")
