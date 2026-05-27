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

    async def play(self, interaction, query: str):
        await interaction.response.defer()
        if not interaction.user.voice:
            await interaction.followup.send(
                "❌ Você precisa entrar em um canal de voz.", ephemeral=True
            )
            return

        player = await self.get_player(interaction)

        tracks = await wavelink.Playable.search(
            query, source=wavelink.TrackSource.YouTubeMusic
        )

        if not tracks:
            await interaction.followup.send("❌ Música não encontrada.", ephemeral=True)
            return

        track = tracks[0]

        await player.play(track)

        await interaction.followup.send(f"▶️ Tocando: {track.title}")

    async def pause(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = interaction.guild.voice_client

        if player:
            await player.pause(True)

            await interaction.followup.send("⏸️ Música pausada.")

    async def resume(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = interaction.guild.voice_client

        if player:
            await player.pause(False)

            await interaction.followup.send("▶️ Música retomada.")

    async def skip(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = interaction.guild.voice_client

        if player:
            await player.skip()

            await interaction.followup.send("⏭️ Música pulada.")

    async def stop(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = interaction.guild.voice_client

        if player:
            await player.disconnect()

            await interaction.followup.send("⏹️ Reprodução encerrada.")
