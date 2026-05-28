class MusicPlayer:
    def __init__(self, guild_id):
        self.guild_id = guild_id

        self.voice_client = None

        self.queue = []

        self.current_track = None

        self.volume = 100

        self.loop = False

        self.shuffle = False

        self.history = []

        self.panel_message = None
