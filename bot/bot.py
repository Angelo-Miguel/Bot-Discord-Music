import discord
import wavelink
from discord.ext import commands
from bot.managers.music_manager import MusicManager
from bot.ui.player_panel import update_player_panel
from bot.config import Config


class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        intents.message_content = True
        intents.voice_states = True

        super().__init__(command_prefix=Config.COMMAND_PREFIX, intents=intents)

        self.manager = MusicManager(self)

    async def setup_hook(self):
        node = wavelink.Node(
            uri=f"http://{Config.LAVALINK_HOST}:{Config.LAVALINK_PORT}",
            password=Config.LAVALINK_PASSWORD,
        )

        await wavelink.Pool.connect(client=self, nodes=[node])

        await self.load_extension("bot.cogs.music")

        await self.tree.sync()

        print("Bot ready")

    async def on_wavelink_track_end(self, payload):
        music_player = self.manager.get_player_by_voice(payload.player)

        if not music_player:
            return

        # LOOP
        if music_player.loop and music_player.current_track:
            await payload.player.play(music_player.current_track.raw)

            return

        # PRÓXIMA MÚSICA
        next_track = self.manager.queue_service.next(music_player)

        if not next_track:
            music_player.current_track = None
            return

        music_player.current_track = next_track

        await payload.player.play(next_track.raw)
        await update_player_panel(self.manager, music_player)


def run_bot(bot=MusicBot()):
    bot.run(Config.DISCORD_TOKEN)
