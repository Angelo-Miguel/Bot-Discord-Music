import discord
from discord.ext import commands

from bot.managers.music_manager import MusicManager


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = MusicManager(bot)

    @discord.app_commands.command(
        name="play",
        description="Toca uma música"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        query: str
    ):
        await self.manager.play(interaction, query)

    @discord.app_commands.command(
        name="pause",
        description="Pausa a música"
    )
    async def pause(self, interaction: discord.Interaction):
        await self.manager.pause(interaction)

    @discord.app_commands.command(
        name="resume",
        description="Retoma a música"
    )
    async def resume(self, interaction: discord.Interaction):
        await self.manager.resume(interaction)

    @discord.app_commands.command(
        name="skip",
        description="Pula a música"
    )
    async def skip(self, interaction: discord.Interaction):
        await self.manager.skip(interaction)

    @discord.app_commands.command(
        name="stop",
        description="Para o player"
    )
    async def stop(self, interaction: discord.Interaction):
        await self.manager.stop(interaction)


async def setup(bot):
    await bot.add_cog(Music(bot))