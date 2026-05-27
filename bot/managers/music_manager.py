from bot.services.player_service import PlayerService


class MusicManager:
    def __init__(self, bot):
        self.bot = bot
        self.player_service = PlayerService(bot)

    async def play(self, interaction, query: str):
        await self.player_service.play(interaction, query)

    async def pause(self, interaction):
        await self.player_service.pause(interaction)

    async def resume(self, interaction):
        await self.player_service.resume(interaction)

    async def skip(self, interaction):
        await self.player_service.skip(interaction)

    async def stop(self, interaction):
        await self.player_service.stop(interaction)