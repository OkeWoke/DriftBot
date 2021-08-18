import discord
import logging

logging.basicConfig(level=logging.INFO)

SERVER_ID = 798109851263041567
CREW_PLAY_ID = 877089280533594163
CREW_ID = 802825970373492757
REGULAR_PLAY_ID = 877081953864663080
REGULAR_ID = 823126880759578634
PLAY_ID = 805637927190134805
STREAM_ID = 816460684195528777

activities_of_interest = ["Assetto Corsa (CM)", "Assetto Corsa"]

class DriftBot(discord.Client):

    async def on_ready(self):
        print("Logged on as {0}".format(self.user))
        self.server = self.get_guild(SERVER_ID)
        for member in self.server.members:
            is_playing, is_streaming = self.activity_check(member)
            await self.playing_role_update_check(member, is_playing)
            await self.stream_role_update_check(member, is_streaming)
        print("Completed update")

    def activity_check(self, member):
        is_playing = False
        is_streaming = False
        for activity in member.activities:
            if activity.name in activities_of_interest: 
                is_playing = True
            if isinstance(activity, discord.Streaming):
                print("streaming detected")
                if activity.game == "Assetto Corsa":
                    is_streaming = True
                    print("streaming assetto")
        return is_playing, is_streaming

    def get_member_role_ids(self, member):
        return  [role.id for role in member.roles]

    def role_resolve(self, member):
        player_roles_ids = self.get_member_role_ids(member)

        if CREW_ID in player_roles_ids:
            role_to_change = CREW_PLAY_ID
        elif REGULAR_ID in player_roles_ids:
            role_to_change = REGULAR_PLAY_ID
        else:
            role_to_change = PLAY_ID

        role = self.server.get_role(role_to_change)

        return role

    async def playing_role_update_check(self, member, is_playing):
        role = self.role_resolve(member)
        if is_playing and role not in member.roles:
            await member.add_roles(role)
        elif role in member.roles and not is_playing:
            await member.remove_roles(role)

    async def stream_role_update_check(self, member, is_streaming):
        member_roles_by_id = self.get_member_role_ids(member)
        if is_streaming and STREAM_ID not in  member_roles_by_id:
            await member.add_roles(self.server.get_role(STREAM_ID))
        elif not is_streaming and STREAM_ID in  member_roles_by_id:
            await member.remove_roles(self.server.get_role(STREAM_ID))

    async def on_member_update(self, before, after):
        print("activity change found")
        is_playing, is_streaming = self.activity_check(after)
        await self.stream_role_update_check(after, is_streaming)
        await self.playing_role_update_check(after, is_playing)


if __name__ == "__main__":
    token_file = open("token.txt", "r")
    token = token_file.readline()
    token_file.close()

    intents = discord.Intents(guilds=True, messages=True, presences=True, members=True)
    client = DriftBot(intents=intents)
    
    client.run(token)