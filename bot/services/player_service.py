import wavelink

from bot.ui.embeds import music_panel
from bot.ui.views import MusicControls
from bot.ui.player_panel import update_player_panel


class PlayerService:
    def __init__(self, bot):
        self.bot = bot

    async def connect_player(self, interaction, music_player):
        if music_player.voice_client:
            return music_player.voice_client

        player: wavelink.Player = await interaction.user.voice.channel.connect(
            cls=wavelink.Player
        )

        music_player.voice_client = player

        return player

    async def play(self, interaction, music_player, query: str):
        await interaction.response.defer()

        if not interaction.user.voice:
            await interaction.followup.send(
                "❌ Entre em um canal de voz.", ephemeral=True
            )
            return

        player = await self.connect_player(interaction, music_player)

        tracks = await wavelink.Playable.search(
            query, source=wavelink.TrackSource.YouTube
        )

        if not tracks:
            await interaction.followup.send("❌ Música não encontrada.", ephemeral=True)
            return

        raw_track = tracks[0]

        from bot.models.track import Track

        track = Track(
            title=raw_track.title,
            url=raw_track.uri,
            duration=raw_track.length,
            author=raw_track.author,
            thumbnail=raw_track.artwork,
            requester=interaction.user,
            raw=raw_track,
        )

        # ADD QUEUE
        if player.playing or player.paused:
            music_player.queue.append(track)

            await interaction.followup.send(f"➕ Adicionado à fila: **{track.title}**")

            return

        # FIRST TRACK
        music_player.current_track = track

        await player.play(track.raw)

        embed = music_panel(
            title=track.title,
            url=track.url,
            requested_by=track.requester,
            duration=track.duration,
            author=track.author,
            thumbnail_url=track.thumbnail,
            volume=music_player.volume,
        )

        view = MusicControls(self.bot.manager, music_player.guild_id)

        message = await interaction.followup.send(embed=embed, view=view)

        music_player.panel_message = message

    async def pause(self, music_player):
        player = music_player.voice_client

        if not player:
            return

        await player.pause(True)

    async def resume(self, music_player):
        player = music_player.voice_client

        if not player:
            return

        await player.pause(False)

    async def skip(self, music_player):
        player = music_player.voice_client

        if not player:
            return

        music_player.skip_requested = True
        await player.skip()

    async def stop(self, music_player):
        player = music_player.voice_client

        if not player:
            return

        music_player.queue.clear()

        music_player.current_track = None

        await player.disconnect()

        music_player.voice_client = None

    async def set_volume(self, music_player, volume):
        player = music_player.voice_client

        if not player:
            return

        volume = max(0, min(volume, 200))

        music_player.volume = volume

        await player.set_volume(volume)
