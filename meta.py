import discord
import subprocess, sys

# get token from token.txt
try:
    with open("token.txt") as file:
        TOKEN = file.read()
except FileNotFoundError:
    print("FileNotFoundError: Store your bot's access token in token.txt")

# make an activity and create the client
client = discord.Client()


async def execute(command, channel):
    # run command and store output in result
    await channel.send("Running command:```" + command + "```")
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    encoding = "cp437"
    if out:
        await channel.send("```" + out.decode(encoding) + "```")
    if err:
        await channel.send("```" + err.decode(encoding) + "```")
    await channel.send("Return code: `" + str(proc.returncode) + "`")


@client.event
async def on_message(message):
    # don't respond to own messages
    if message.author == client.user:
        return

    # if private channel or channel starting with "terminal", execute message
    if isinstance(message.channel, discord.DMChannel) or message.channel.name.lower().startswith("terminal"):
        await execute(message.content, message.channel)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # change activity
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" "))


client.run(TOKEN)
