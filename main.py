from credentials import token
import logging
from telegram import ForceReply, Update

from telegram.ext import Application, CommandHandler, ContextTypes

from weather import get_weather

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user

    await update.message.reply_html(

        rf"Hi {user.mention_html()}!",

        reply_markup=ForceReply(selective=True),

    )

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /weather <city> <clock (e.g., 1500)>")
        return

    city = context.args[0]
    clock_str = context.args[1]

    try:
        hour = int(clock_str[:2])
    except ValueError:
        await update.message.reply_text("Invalid clock format. Use HHMM like 1500 for 3 PM.")
        return

    mapping = {
        1: 13, 2: 14, 3: 15, 4: 16, 5: 17, 6: 18,
        10: 22, 12: 24, 13: 1, 14: 2, 15: 3, 16: 4,
        17: 5, 18: 6, 19: 7, 20: 8, 21: 9, 22: 10,
        23: 11, 0: 12
    }

    time = mapping.get(hour)
    if time is None:
        await update.message.reply_text("Unsupported clock hour.")
        return

    weather_info = get_weather(city, time)

    await update.message.reply_text(f"The weather in {city} is {weather_info} at {clock_str}")


def main() -> None:

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("weather", weather_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    main()