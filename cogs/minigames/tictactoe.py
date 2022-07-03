from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import random
import asyncio

from libraries.standardLib import removeat
   

class tictactoe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = 'tictactoe',
        aliases = ['ttt', 'tic', 'tick'],
        brief = 'Play a game of tic tac toe with your friends!',
    )
    @commands.max_concurrency(1, BucketType.channel)
    @cooldown(1, 5, BucketType.channel)
    async def tictactoeCommand(self, ctx, SelectedPlayer: Member):
        await ctx.send(f"Starting game with {SelectedPlayer.mention}")
        
        valid_placements = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        board = [
            "-", "-", "-",
            "-", "-", "-",
            "-", "-", "-"
        ]
        
        gamestr = "```"
        for i in range(3):
            for j in range(3):
                gamestr += board[i*3+j] + "   "
            gamestr += "\n"
        gamestr += "```"
        
        reference = [
            "1️⃣", "2️⃣", "3️⃣",
            "4️⃣", "5️⃣", "6️⃣",
            "7️⃣", "8️⃣", "9️⃣",
        ]
        
        referencestr = ""
        for i in range(3):
            for j in range(3):
                referencestr += reference[i*3+j]
            referencestr += "\n"

        player1 = ctx.author
        player2 = SelectedPlayer
        piece = "X"
        
        turn = random.randint(0, 1)
        
        if turn % 2 == 0:
            player = player2
            otherPlayer = player1
            piece = "O"
        else:
            player = player1
            otherPlayer = player2
            piece = "X"
            
        embed = Embed(title="Tic Tac Toe", description="", color=0xe91e63)
        embed.add_field(name="||\n||", value=f"{gamestr}\n\n{referencestr}", inline=False)
        
        embedMsg = await ctx.send(embed=embed)
            
        oldMsg = await ctx.send(f"{player.mention}'s turn")
        
        
        
        while True:
            
            move = await self.get_move(ctx, valid_placements, board, player, piece)

            if move == "exit":
                return
            
            board[move] = piece
            
            
            gamestr = "```"
            for i in range(3):
                for j in range(3):
                    gamestr += board[i*3+j] + "   "
                gamestr += "\n"
            gamestr += "```"
            
            embed.clear_fields()
            embed.add_field(name="||\n||", value=f"{gamestr}\n\n{referencestr}", inline=False)
        
            await embedMsg.edit(embed=embed)
            await oldMsg.delete()
            
            valid_placements.remove(move)
            
            if await self.check_win(ctx, board, piece):
                await ctx.send(f"{player.mention} wins!")
                return
            
            if await self.check_tie(ctx, board):
                await ctx.send("It's a tie!")
                return
            
            oldMsg = await ctx.send((f"{player.display_name} chose {move + 1}\nit's now {otherPlayer.mention}'s turn"))
            
            turn += 1
            if turn % 2 == 0:
                player = player2
                otherPlayer = player1
                piece = "O"
            else:
                player = player1
                otherPlayer = player2
                piece = "X"
    
    @commands.Cog.listener()
    async def check_win(self, ctx, board, piece):
        
        for i in range(3):
            # check horizontal rows
            if board[i*3] == piece and board[i*3+1] == piece and board[i*3+2] == piece:
                return True
        
            # check vertical columns
            if board[i] == piece and board[i+3] == piece and board[i+6] == piece:
                return True
        
        # check diagonal
        if (board[0] == piece and board[4] == piece and board[8] == piece) or (board[2] == piece and board[4] == piece and board[6] == piece):
            return True

        return False

    @commands.Cog.listener()
    async def check_draw(self, ctx, board):
        if "-" not in board:
            return True
        return False
    
    
    @commands.Cog.listener()
    async def get_move(self, ctx, valid_placements, board, player, piece):
        for i in range(5):
            try:    
                message = await self.bot.wait_for(
                    "message", check=lambda m: m.author == player, timeout=120
                )
                try:
                    move = int(message.content) - 1
                    await message.delete()
                    break
                except:
                    pass
            except asyncio.TimeoutError:
                await ctx.send(f"{player.mention} took too long to make a move, cancelling game")
                return "exit"

        #await ctx.send(board)
        
        if move not in range(0, 9):
            await ctx.send(await removeat(f"{player.display_name} didn't choose a valid placement, try again"), delete_after=10)
            return await self.get_move(ctx, valid_placements, board, player, piece)
        
        elif board[move] != "-":
            await ctx.send(await removeat(f"{player.display_name} didn't choose a valid placement, try again"), delete_after=10)
            return await self.get_move(ctx, valid_placements, board, player, piece)
        
        else:
            try:
                if type(move) != int:
                    return await self.get_move(ctx, valid_placements, board, player, piece)
                #await ctx.send(valid_placements)
                return move
            except Exception as e:
                print(e)
                await ctx.send(await removeat(f"{player.display_name} didn't choose a valid placement, try again"), delete_after=10)
                return await self.get_move(ctx, valid_placements, board, player, piece)

def setup(bot):
    bot.add_cog(tictactoe(bot))
