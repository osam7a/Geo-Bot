import datetime


class Log:
    def __init__(self, file, bot):
        self.file = file
        self.bot = bot

    def info(self, message):
        f = open(self.file, "a")
        f.write(f"[{datetime.datetime.now().strftime('%c')}] [INFO] {message}\n")
        f.close()

    def warn(self, message):
        f = open(self.file, "a")
        f.write(f"[{datetime.datetime.now().strftime('%c')}] [WARNING] {message}\n")
        f.close()

    async def error(self, message):
        f = open(self.file, "a")
        f.write(f"[{datetime.datetime.now().strftime('%c')}] ERROR] {message}\n")
        f.close()
        channel = self.bot.get_channel(900564880912953424)
        await channel.send(f"```py\n{message}\n```")

    def handled(self, message):
        f = open(self.file, "a")
        f.write(f"[{datetime.datetime.now().strftime('%c')}] [HANDLED] {message}\n")
        f.close()