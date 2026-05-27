# Classe de configuração

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    COMMAND_PREFIX = "!"
    
    # Lavalink
    LAVALINK_HOST = os.getenv("LAVALINK_HOST")
    LAVALINK_PORT = int(os.getenv("LAVALINK_PORT"))
    LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD")