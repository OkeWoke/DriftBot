import discord
import logging

logging.basicConfig(level=logging.INFO)

SERVER_ID = 876754249982308413
ROLE_ID = 876771642167136286
activities_of_interest = ["Assetto Corsa (CM)", "Assetto Corsa"]

class DriftBot(discord.Client):

    async def on_ready(self):
        print("Logged on as {0}".format(self.user))
        self.server = self.get_guild(SERVER_ID)
        self.drift_role = self.server.get_role(ROLE_ID)

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))

    async def on_member_update(self, before, after):
        found_activity = False
        for activity in after.activities:
            if activity.name in activities_of_interest:
                found_activity = True
        if found_activity:
            await after.add_roles(self.drift_role)
        else:
            await after.remove_roles(self.drift_role)

    
if __name__ == "__main__":
    token_file = open("token.txt", "r")
    token = token_file.readline()
    token_file.close()

    intents = discord.Intents(guilds=True, messages=True, presences=True, members=True)
    client = DriftBot(intents=intents)
    
    client.run(token)