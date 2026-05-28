from bot.models.music_player import MusicPlayer

from bot.services.player_service import PlayerService
from bot.services.queue_service import QueueService


class MusicManager:
    def __init__(self, bot):
        self.bot = bot

        self.players = {}

        self.player_service = PlayerService(bot)

        self.queue_service = QueueService()

    def get_player(self, guild_id):
        if guild_id not in self.players:
            self.players[guild_id] = MusicPlayer(guild_id)

        return self.players[guild_id]

    def get_player_by_voice(self, voice_client):
        for player in self.players.values():
            if player.voice_client == voice_client:
                return player

        return None

    async def play(self, interaction, query):
        music_player = self.get_player(interaction.guild.id)

        await self.player_service.play(interaction, music_player, query)

    async def pause(self, guild_id):
        music_player = self.get_player(guild_id)

        await self.player_service.pause(music_player)

    async def resume(self, guild_id):
        music_player = self.get_player(guild_id)

        await self.player_service.resume(music_player)

    async def skip(self, guild_id):
        music_player = self.get_player(guild_id)

        await self.player_service.skip(music_player)

    async def stop(self, guild_id):
        music_player = self.get_player(guild_id)

        await self.player_service.stop(music_player)

    async def set_volume(self, guild_id, volume):
        music_player = self.get_player(guild_id)

        await self.player_service.set_volume(music_player, volume)
