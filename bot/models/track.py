class Track:
    def __init__(
        self,
        *,
        title,
        url,
        duration,
        author,
        thumbnail,
        requester,
        raw
    ):
        self.title = title
        self.url = url
        self.duration = duration
        self.author = author
        self.thumbnail = thumbnail
        self.requester = requester

        self.raw = raw