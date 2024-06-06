import discord
import requests
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Configuration using environment variables
DISCORD_BOT_TOKEN = str(os.getenv("DISCORD_BOT_TOKEN"))
FLOWISE_API_KEY = str(os.getenv("FLOWISE_API_KEY"))
FLOWISE_API_URL = str(os.getenv("FLOWISE_API_URL"))
FLOWISE_API_ENDPOINT = str(os.getenv("FLOWISE_API_ENDPOINT"))
CHAT_FLOW_ID = str(os.getenv("CHAT_FLOW_ID"))

# Validate configuration
required_env_vars = [
    "DISCORD_BOT_TOKEN",
    "FLOWISE_API_KEY",
    "FLOWISE_API_URL",
    "FLOWISE_API_ENDPOINT",
    "CHAT_FLOW_ID",
]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
API = (
    f"{FLOWISE_API_URL}{FLOWISE_API_ENDPOINT}{CHAT_FLOW_ID}"
    if FLOWISE_API_URL and FLOWISE_API_ENDPOINT
    else None
)
if API is None:
    raise ValueError("FLOWISE_API_URL and FLOWISE_API_ENDPOINT must be provided.")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="echo", description="Say hello to the bot")
async def echo(ctx):
    print("[echo triggered]")
    await ctx.respond("delta")

def query(payload):
    response = requests.post(
        API,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {FLOWISE_API_KEY}",
        },
    )
    return response.json()

@bot.slash_command(name="ask", description="Ask a question, reply with model response")
async def ask(ctx, question: str):
    await ctx.defer()
    print(f"[ace triggered] Question: {question}")
    try:
        data = query({"question": f"{str(question)}"})
        print(f"{data}")
        if "text" in data:
            print("[text found] in data")
            await ctx.respond(str(data["text"]))
        else:
            logging.error(f"Unexpected response format: {data}")
            await ctx.followup.send("Received unexpected response format from server.")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        await ctx.respond(
            "Failed to communicate with Flowise API due to an HTTP error."
        )
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error occurred during request: {req_err}")
        await ctx.respond("An error occurred while processing your request.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await ctx.respond("An unexpected error occurred.")

bot.run(DISCORD_BOT_TOKEN)
