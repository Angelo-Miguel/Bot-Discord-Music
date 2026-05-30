import random


class QueueService:
    def add(self, player, track):
        player.queue.append(track)

    def next(self, player):
        if not player.queue:
            return None

        return player.queue.pop(0)

    def clear(self, player):
        player.queue.clear()

    def shuffle(self, player):
        random.shuffle(player.queue)
