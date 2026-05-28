from bot.ui.embeds import music_panel


async def update_player_panel(manager, music_player):
    track = music_player.current_track

    if not track:
        return

    # IMPORT LOCAL
    from bot.ui.views import MusicControls

    embed = music_panel(
        title=track.title,
        url=track.url,
        requested_by=track.requester,
        duration=track.duration,
        author=track.author,
        thumbnail_url=track.thumbnail,
        volume=music_player.volume,
    )

    view = MusicControls(manager, music_player.guild_id)

    if music_player.panel_message:
        await music_player.panel_message.edit(embed=embed, view=view)
