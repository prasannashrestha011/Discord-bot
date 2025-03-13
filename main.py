import os 
import random
from dotenv import load_dotenv 
import discord
from discord.ext import commands 
import yt_dlp

from api.wheather import get_weather
from responses.greet import hello_responses
from responses.help import help_responses


load_dotenv()
AUTH_TOKEN=os.getenv("DISCORD_TOKEN")

#creating a bot instance
intents=discord.Intents.default()
intents.message_content=True

#bot command for audio 
bot=commands.Bot(command_prefix="!",intents=intents)




@bot.event
async def on_ready()->None:
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message:discord.Message)->str:
    print(f"[{message.channel}] {message.author} : {message.content}")
    if message.author==bot.user:
      return 
    
    if message.content.lower()=="!hello":
       randomized_greet=random.choice(hello_responses)
       greet_user=f"{randomized_greet} {message.author}"
       await message.channel.send(greet_user)
    
    if message.content.split(" ")[0].lower()=="!wheather":
        city=message.content.split(" ")[1]
        wheather_details=await get_weather(city)
        await message.channel.send(wheather_details)
    
    if message.content.lower()=="!help":
        await message.channel.send(help_responses)

    #for handling custom bot commands
    await bot.process_commands(message)

@bot.event
async def on_member_join(member:discord.Member)->str:
    channel=discord.utils.get(member.guild.text_channels,name="general")
    if channel:
        welcome_message = f"🎉 Welcome to the server, {member.mention}! {random.choice(hello_responses)}"
        await channel.send(welcome_message)




#commands for playing yt audios
@bot.command()
async def join(ctx:commands.Context):
    #getting music voice channel
    guild=ctx.guild
    music_channel=discord.utils.get(guild.voice_channels,name="music")
    if music_channel:
        if ctx.voice_client is None:
            await music_channel.connect()
            await ctx.send(
                f"🎶 Joined `{music_channel.name}` 🔊\n"
                "Fetching the music...⌛"
                )
        else:
            await ctx.send("Already in a voice channel, mate")
    else:
        await ctx.send("Channel not found")

FFMPEG_OPTIONS = {
    'options': '-vn'
}
@bot.command()
async def play(ctx: commands.Context, url: str):
    vc:discord.VoiceClient = ctx.voice_client
    if not vc:     
        await join(ctx)
        vc=ctx.voice_client
    
    if not vc:
        await ctx.send("❌ Failed to join a voice channel.")
        return

    if vc.is_playing:
        vc.stop()
    # Get direct audio URL from YouTube
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'default_search': 'ytsearch',  # Enables search functionality
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # 🔴 No download, just get URL
        video = info['entries'][0]  # Get first result
        audio_url = video['url']
        video_title = video['title']

    # Play the audio stream
    vc.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))

    await ctx.send(f"🎶 Now streaming: {video_title}")


@bot.command()
async def resume(ctx:commands.Context):
    vc:discord.VoiceClient=ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("▶️ Music resumed.")
    else:
        await ctx.send("Cant resume")

@bot.command()
async def pause(ctx:commands.Context):
    vc:discord.VoiceClient=ctx.voice_client 
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send("⏹️ Music stopped.")

@bot.command()
async def disconnect(ctx:commands.Context):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

def main():
    bot.run(token=AUTH_TOKEN)

if __name__=="__main__":
    main()


