import discord
import wavelink
from discord.ext import commands
from bot.config import Config


class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        intents.message_content = True
        intents.voice_states = True

        super().__init__(command_prefix=Config.COMMAND_PREFIX, intents=intents)

    async def setup_hook(self):
        node = wavelink.Node(
            uri=f"http://{Config.LAVALINK_HOST}:{Config.LAVALINK_PORT}",
            password=Config.LAVALINK_PASSWORD,
        )

        await wavelink.Pool.connect(client=self, nodes=[node])

        print("Lavalink connected")


def run_bot(bot=MusicBot()):
    bot.run(Config.DISCORD_TOKEN)
