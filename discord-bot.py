import json
import interactions
from randomancer import parse_roll, init_tables
import logging

logging.basicConfig(
    filename="discord_bot.log",
    level="DEBUG"
)

permissions_level = "2048"
invite_url = ''

with open("secrets.json") as file:
    secrets = json.load(file)

bot = interactions.Client(
    token=secrets["bot_token"]
    )

@bot.command(
    name="generate",
    description="Generate a result with the given roll string.",
    options = [
        interactions.Option(
            name="roll_string",
            description="string to feed into the generator",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],

)
async def generate(ctx: interactions.CommandContext, roll_string: str):
    logging.debug(roll_string)
    try:
        result = parse_roll(roll_string)
    except:
        result = "Sorry, this command encountered an error and could not be completed!"
    await ctx.send(result)



@bot.command(
    name="list",
    description="List all available tables."
)
async def generate(ctx: interactions.CommandContext):
    result = ""
    try:
        tables = init_tables()
        for key in tables.keys():
            result += "{key}" + "\n"
    except:
        result = "Sorry, this command encountered an error and could not be completed!"
    await ctx.send(result)

bot.start()