import discord
import logging

logging.basicConfig(level=logging.INFO)

SERVER_ID = 798109851263041567

CREW_PLAY_ID = 877089280533594163
CREW_ID = 802825970373492757
REGULAR_PLAY_ID = 877081953864663080
REGULAR_ID = 823126880759578634
PLAY_ID = 805637927190134805

activities_of_interest = ["Assetto Corsa (CM)", "Assetto Corsa"]

class DriftBot(discord.Client):

    async def on_ready(self):
        print("Logged on as {0}".format(self.user))
        self.server = self.get_guild(SERVER_ID)
        is_playing = False
        for member in self.server.members:
            for activity in activities_of_interest:
                if activity in [b.name for b in member.activities]: is_playing = True
            if is_playing:
                role = self.role_reserve(member)
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))

    def role_resolve(self, member):
        player_roles_ids = [role.id for role in member.roles]

        if CREW_ID in player_roles_ids:
            role_to_change = CREW_PLAY_ID
        elif REGULAR_ID in player_roles_ids:
            role_to_change = REGULAR_PLAY_ID
        else:
            role_to_change = PLAY_ID

        role = self.server.get_role(role_to_change)

        return role

    async def on_member_update(self, before, after):
        was_playing = False
        is_playing = False

        for activity in activities_of_interest:
            if activity in [b.name for b in before.activities]: was_playing = True
            if activity in [a.name for a in after.activities]: is_playing = True

        if (was_playing and is_playing) or (not was_playing and not is_playing):
            #Do nothing
            return

        role = self.role_resolve(after)

        if not was_playing and is_playing:
            await after.add_roles(role)
        elif was_playing and not is_playing:
             await after.remove_roles(role)


if __name__ == "__main__":
    token_file = open("token.txt", "r")
    token = token_file.readline()
    token_file.close()

    intents = discord.Intents(guilds=True, messages=True, presences=True, members=True)
    client = DriftBot(intents=intents)
    
    client.run(token)