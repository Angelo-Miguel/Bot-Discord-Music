import discord
from bot.ui.embeds import music_panel


async def update_player_panel(manager, music_player):
    if not music_player.panel_message:
        return

    if not music_player.current_track:
        embed = discord.Embed(
            title="🎵 Music Player",
            description="📭 Nenhuma música tocando.",
            color=discord.Color.from_rgb(45, 47, 49),
        )

        await music_player.panel_message.edit(embed=embed, view=None)
        return

    from bot.ui.views import MusicControls

    embed = music_panel(
        title=music_player.current_track.title,
        url=music_player.current_track.url,
        requested_by=music_player.current_track.requester,
        duration=music_player.current_track.duration,
        author=music_player.current_track.author,
        thumbnail_url=music_player.current_track.thumbnail,
        volume=music_player.volume,
    )

    view = MusicControls(manager, music_player.guild_id)
    await music_player.panel_message.edit(embed=embed, view=view)
