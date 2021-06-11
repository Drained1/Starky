import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import os

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 45, commands.BucketType.member)

    @commands.command(description='Why do you need help with the help command?')
    @commands.cooldown(1, 3, BucketType.user)
    async def help(self, ctx, cmd=None):
        if not cmd:
            embed = discord.Embed(title='All Commands', color=0x000001)
            for a in sorted(list(self.client.cogs)):
                commands = []
                if a not in ["Dev", "Events", "Help"]:
                    for command in self.client.get_cog(a).get_commands():
                        if not command.hidden:
                            commands.append(f"`{command.name}`")
                    embed.add_field(name=a, value=", ".join(sorted(commands)), inline=False)
            embed.set_footer(icon_url=self.client.user.avatar_url, text=f'Do {ctx.prefix}help to get more info on a command')
            await ctx.send(embed=embed)
        else:
            try:
                fcmd = self.client.get_command(cmd.lower())
            except:
                return await ctx.send('That command doesnt exist')
            await ctx.send(embed=discord.Embed(title=f"Command: {fcmd}", color=0x000001).add_field(name='Information', value=f'```Description: {fcmd.description}\nUsage: {ctx.prefix}{fcmd} {fcmd.signature}\nAliases: {", ".join(fcmd.aliases)}```', inline=False).set_footer(icon_url=self.client.user.avatar_url, text=f'<> means required [] means optional')    )

def setup(client):
    client.add_cog(Help(client))