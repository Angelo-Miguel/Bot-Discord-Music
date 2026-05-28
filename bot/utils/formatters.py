def format_duration(seconds: int) -> str:
    if seconds <= 0:
        return "Live"

    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}m {seconds:02d}s"


def format_volume(volume: float) -> str:
    return f"{int(volume)}%" if isinstance(volume, (int, float)) else str(volume)
