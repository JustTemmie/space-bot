import asyncio

async def get_input(self, ctx, time = 30):
    try:
        return await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author, timeout=time
        )
    except asyncio.TimeoutError:
        return await ctx.send(f"**Timed out** You took too long to answer the question, Please try again")

# this was old code that has been rewritten in rust by https://github.com/Radiicall
# async def str_replacer(initial_string, ch,
#         replacing_character, occurrence):
    
#     # breaking a string into it's
#     # every single character in list
#     lst1 = list(initial_string)
#     lst2 = list(ch)
    
#     # List to store the indexes in which
#     # it is replaced with the
#     # replacing_character
#     lst3 = []
    
#     # Loop to find the Nth occurrence of
#     # given characters in the string
#     for i in lst2:
#         if(lst1.count(i)>= occurrence):
#             count = 0
#             for j in range(0, len(initial_string)):
#                 if(i == lst1[j]):
#                     count+= 1
#                     if(count == occurrence):
#                         lst3.append(j)
    
#     for i in lst3:
#         # Replacing that particular index
#         # with the requested character
#         lst1[i] = replacing_character

#     val = (''.join(lst1))
    
#     return val