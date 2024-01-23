import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import dotenv_values

env_variables = dotenv_values('.env')

service_secret = env_variables['service_secret']
license_key = env_variables['license_key']

# Discord Botの設定
DISCORD_TOKEN = env_variables['discord_bot_token']
GPT_CHANNEL_NAME = 'gpt'  # リッスンするチャンネル名

# OpenAI APIの設定
OPENAI_API_KEY = env_variables['openai_api_key']  # OpenAIのAPIキー

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# Botのインスタンスを作成
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

# イベントハンドラ: Botが準備完了
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to the discord server')

# メッセージリッスン
@bot.event
async def on_message(message):
    # 自分自身のメッセージは無視
    if message.author == bot.user:
        return

    # GPTチャンネルからのメッセージのみ処理
    if message.channel.name == GPT_CHANNEL_NAME:
        # OpenAI APIによるレスポンスの取得
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f'"""\n{message.content}\n"""',}],
            temperature=0,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['"""'],
        )

        await message.channel.send(response.choices[0].message.content)

# Botを実行
bot.run(DISCORD_TOKEN)
