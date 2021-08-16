import discord
import logging

logging.basicConfig(level=logging.INFO)

class DriftBot(discord.Client):
    async def on_ready(self):
        print("Logged on as {0}".format(self.user))

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))


if __name__ == "__main__":
    token_file = open("token.txt", "r")
    token = token_file.readline()
    token_file.close()

    intents = discord.Intents(messages=True)
    client = DriftBot(intents=intents)
    client.run(token)