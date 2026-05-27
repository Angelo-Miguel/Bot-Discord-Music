import wavelink


class PlayerService:
    def __init__(self, bot):
        self.bot = bot

    async def get_player(self, interaction):
        guild = interaction.guild

        player: wavelink.Player = guild.voice_client

        if not player:
            player = await interaction.user.voice.channel.connect(cls=wavelink.Player)

        return player

    async def play(self, interaction, music_player, query: str):
        await interaction.response.defer()

        if not interaction.user.voice:
            await interaction.followup.send(
                "❌ Entre em um canal de voz.", ephemeral=True
            )
            return

        if not music_player.voice_client:
            music_player.voice_client = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )

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

        if music_player.voice_client.playing:
            music_player.queue.append(track)

            await interaction.followup.send(f"➕ Adicionado à fila: {track.title}")

            return

        music_player.current_track = track

        await music_player.voice_client.play(track.raw)

        await interaction.followup.send(f"▶️ Tocando: {track.title}")

    async def pause(self, interaction, music_player):
        await interaction.response.defer()
        player = music_player.voice_client

        if player:
            await player.pause(True)

            await interaction.followup.send("⏸️ Música pausada.")

    async def resume(self, interaction, music_player):
        await interaction.response.defer()
        player = music_player.voice_client

        if player:
            await player.pause(False)

            await interaction.followup.send("▶️ Música retomada.")

    async def skip(self, interaction, music_player):
        await interaction.response.defer()

        player = music_player.voice_client

        if not player:
            await interaction.followup.send("❌ Nenhum player ativo.", ephemeral=True)
            return

        next_track = music_player.queue.pop(0) if music_player.queue else None

        if not next_track:
            await player.skip()

            music_player.current_track = None

            await interaction.followup.send("⏭️ Música pulada. Fila vazia.")

            return

        music_player.current_track = next_track

        await player.play(next_track.raw)

        await interaction.followup.send(f"⏭️ Tocando agora: {next_track.title}")

    async def stop(self, interaction, music_player):
        await interaction.response.defer()
        player = music_player.voice_client

        if player:
            await player.disconnect()

            await interaction.followup.send("⏹️ Reprodução encerrada.")
