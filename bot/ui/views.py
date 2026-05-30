import discord
from bot.ui.player_panel import update_player_panel
from bot.ui.embeds import queue_embed


class MusicControls(discord.ui.View):
    def __init__(self, manager, guild_id):
        super().__init__(timeout=None)
        self.manager = manager
        self.guild_id = guild_id
        self.update_pause_resume_button()

    def get_player(self):
        return self.manager.get_player(self.guild_id)

    def update_pause_resume_button(self):
        button = self.pause_resume

        music_player = self.get_player()

        if (
            music_player
            and music_player.voice_client
            and music_player.voice_client.paused
        ):
            button.label = "▶️ Resume"
        else:
            button.label = "⏸️ Pause"

    @discord.ui.button(label="🔈 Down", style=discord.ButtonStyle.secondary)
    async def decrease_volume(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        await interaction.response.defer()

        new_volume = max(0, music_player.volume - 10)

        await self.manager.set_volume(self.guild_id, new_volume)

        await update_player_panel(self.manager, music_player)

    @discord.ui.button(label="⏮️ Back", style=discord.ButtonStyle.secondary)
    async def back(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.defer()

    @discord.ui.button(
        label="⏸️ Pause",
        style=discord.ButtonStyle.secondary,
        custom_id="pause_resume",
    )
    async def pause_resume(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        if not music_player.voice_client:
            await interaction.response.send_message(
                "❌ Nenhum player ativo.", ephemeral=True
            )
            return

        await interaction.response.defer()

        if music_player.voice_client.paused:
            await self.manager.resume(self.guild_id)
        else:
            await self.manager.pause(self.guild_id)

        self.update_pause_resume_button()

        await update_player_panel(self.manager, music_player)

    @discord.ui.button(label="⏭️ Skip", style=discord.ButtonStyle.secondary)
    async def skip(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        await interaction.response.defer()

        await self.manager.skip(self.guild_id)

        self.update_pause_resume_button()

        await update_player_panel(self.manager, music_player)

    @discord.ui.button(label="🔊 Up", style=discord.ButtonStyle.secondary)
    async def increase_volume(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        await interaction.response.defer()

        new_volume = min(200, music_player.volume + 10)

        await self.manager.set_volume(self.guild_id, new_volume)

        await update_player_panel(self.manager, music_player)

    @discord.ui.button(label="🔀 Shuffle", style=discord.ButtonStyle.secondary)
    async def shuffle(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        self.manager.queue_service.shuffle(music_player)
        await update_player_panel(self.manager, music_player)

        await interaction.response.send_message("🔀 Queue embaralhada.", ephemeral=True)

    @discord.ui.button(label="🔁 Loop", style=discord.ButtonStyle.secondary)
    async def loop(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        music_player.loop = not music_player.loop

        # Altera a cor do botão
        button.style = (
            discord.ButtonStyle.success
            if music_player.loop
            else discord.ButtonStyle.secondary
        )

        await update_player_panel(self.manager, music_player)

        await interaction.response.send_message(
            f"🔁 Loop {'ativado' if music_player.loop else 'desativado'}.",
            ephemeral=True,
        )

    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
    async def stop(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        await interaction.response.defer()

        await self.manager.stop(self.guild_id)

        embed = discord.Embed(
            description="⏹️ Playback stopped.",
            color=discord.Color.from_rgb(45, 47, 49),
        )

        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label="Autoplay", style=discord.ButtonStyle.secondary)
    async def autoplay(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            "🚧 Autoplay ainda não implementado.", ephemeral=True
        )

    @discord.ui.button(label="Playlist", style=discord.ButtonStyle.secondary)
    async def playlist(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        music_player = self.get_player()

        if not music_player.queue:
            await interaction.response.send_message("📭 Queue vazia.", ephemeral=True)
            return

        embed = queue_embed(music_player)

        await interaction.response.send_message(embed=embed, ephemeral=True)
