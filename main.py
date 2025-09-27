# main.py
import discord
from discord.ext import commands
from config import TOKEN
import os
import importlib

bot = commands.Bot(command_prefix='_', self_bot=True)

# commands 폴더 내 모든 파일 setup 호출
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        module_name = f"commands.{filename[:-3]}"
        module = importlib.import_module(module_name)
        if hasattr(module, "setup"):
            module.setup(bot)

bot.run(TOKEN, bot=False)
