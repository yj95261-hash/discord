from discord.ext import commands
import discord

voice_client = None
target_channel_id = None

def setup(bot: commands.Bot):
    @bot.command()
    async def call(ctx, channel_id: int):
        """특정 음성 채널에 입장"""
        global voice_client, target_channel_id
        target_channel_id = channel_id
        channel = bot.get_channel(channel_id)
        if not channel:
            await ctx.send("채널을 찾을 수 없습니다.")
            return
        # 이미 연결되어 있으면 끊기
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
        # 채널 연결
        voice_client = await channel.connect()
        await ctx.send(f"{channel.name}에 입장했습니다!")

    @bot.event
    async def on_voice_state_update(member, before, after):
        global voice_client
        # 봇이 나갔다가 다시 들어가기
        if member.id == bot.user.id:
            if before.channel is not None and after.channel is None and target_channel_id is not None:
                channel = bot.get_channel(target_channel_id)
                if channel and (not bot.voice_clients or bot.voice_clients[0].channel != channel):
                    voice_client = await channel.connect()
                    print(f"자동으로 {channel.name}에 재입장했습니다!")
