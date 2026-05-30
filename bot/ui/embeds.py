import discord
from bot.utils.formatters import format_duration, format_volume


def music_panel(
    *,
    title: str,
    url: str,
    requested_by: discord.Member,
    duration: int,
    author: str,
    thumbnail_url: str | None = None,
    volume: float,
) -> discord.Embed:

    embed = discord.Embed(
        description=f"[{title}]({url})",
        color=discord.Color.from_rgb(45, 47, 49),
    )

    embed.set_author(name=f"🎵 MUSIC PANEL", icon_url=requested_by.display_avatar.url)

    embed.add_field(
        name="⏱ Music Duration", value=format_duration(duration), inline=True
    )

    embed.add_field(name="🎼 Music Author", value=author, inline=True)

    embed.add_field(name="🔊 Volume", value=format_volume(volume), inline=True)

    # Put the requester in the footer correctly
    embed.set_footer(text=f"👤 Requested By {requested_by.display_name}")

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    return embed


def queue_embed(music_player):
    current = music_player.current_track

    description = ""

    if current:
        description += f"▶ **Agora tocando**\n" f"{current.title}\n\n"

    if not music_player.queue:
        description += "📭 Nenhuma música na fila."

    else:
        description += "─────────────\n\n"

        for index, track in enumerate(
            music_player.queue[:10],
            start=1,
        ):
            description += f"**{index}.** {track.title}\n"

        remaining = len(music_player.queue) - 10

        if remaining > 0:
            description += f"\n... e mais {remaining} músicas"

    return discord.Embed(
        title="🎶 Queue",
        description=description,
        color=discord.Color.from_rgb(45, 47, 49),
    )
