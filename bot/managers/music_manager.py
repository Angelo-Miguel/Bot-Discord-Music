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
        player = self.get_player(interaction.guild.id)

        await self.player_service.play(interaction, player, query)

    async def pause(self, interaction):
        player = self.get_player(interaction.guild.id)

        await self.player_service.pause(interaction, player)

    async def resume(self, interaction):
        player = self.get_player(interaction.guild.id)

        await self.player_service.resume(interaction, player)

    async def skip(self, interaction):
        player = self.get_player(interaction.guild.id)

        await self.player_service.skip(interaction, player)

    async def stop(self, interaction):
        player = self.get_player(interaction.guild.id)

        await self.player_service.stop(interaction, player)
