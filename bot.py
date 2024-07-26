from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InputMediaAnimation,
    Update,
)
from telegram import error
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
import logging
from uuid import uuid4
from Torob import Torob
from os import getenv

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
# load environment variables
PROXY = getenv("PROXY")
TOKEN = getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN field can't be empty !")

gif_file_id = None
usage_guide_message = """
سلام 👋
برای استفاده از ربات کافیه داخل چت مورد نظرتون آیدی ربات رو بنویسید و بعد از یک فاصله اسم کالایی که میخواید رو تایپ کنید : 

`@Torobibot فلش مموری`
"""

# Define a few command handlers. These usually take the two arguments update and


# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    global gif_file_id

    # upload usage guide file
    if gif_file_id:
        # use the file id
        usage_guide = gif_file_id
    else:
        # upload from file
        usage_guide = InputMediaAnimation(open("usage_torobot.mp4", "rb")).media

    # send usage guide file
    sent_file = await update.message.reply_animation(
        usage_guide,
        caption=usage_guide_message,
        parse_mode=ParseMode.MARKDOWN,
        read_timeout=50,
    )

    # save file id
    gif_file_id = sent_file.animation.file_id


# inline query handler
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""

    query = update.inline_query.query

    if not query:
        return
    # get results from torob.ir by the query
    torob = Torob(query)
    cards = torob.get_result(20)

    # create the InlineRsult list
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=card.name1,
            thumbnail_url=card.image,
            thumbnail_width=80,
            url=card.product_page,
            description=f"{card.price:,} تومان",
            input_message_content=InputTextMessageContent(
                "🛍 **{}**\n💰 {:,} تومان\n🛒 [موجود {}]({})".format(
                    card.name1, card.price, card.shop_text, card.product_page
                ),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            ),
        )
        for card in cards
    ]

    # send results as answer
    try:
        await update.inline_query.answer(results)
    except error.BadRequest as e:
        print(e)


# footer


def main() -> None:
    """Run the bot."""

    # Create the Application and pass it your bot's token.

    if PROXY:
        application = (
            Application.builder()
            .token(TOKEN)
            .proxy(PROXY)
            .get_updates_proxy(PROXY)
            .build()
        )
    else:
        application = Application.builder().token(TOKEN).build()

    # add the handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
