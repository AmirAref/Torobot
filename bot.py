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
from Torob.api import get_torob_cards
from utils import create_info_message
import messages
from os import getenv

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
# load environment variables

gif_file_id = None


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
        caption=messages.START_MESSAGE,
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
    try:
        cards = get_torob_cards(query=query, count=20)
    except Exception:
        logger.exception("get cards data from torob failed : ")
        # TODO: import messages from another module
        return await update.inline_query.answer(
            [
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=messages.ERROR_RAISED_MESSAGE,
                    # description="",
                    input_message_content=InputTextMessageContent(
                        messages.ERROR_RAISED_MESSAGE,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True,
                    ),
                )
            ]
        )
    logger.info(f"i've got these cards : {cards}")

    # create the InlineRsult list
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=card.name1,
            thumbnail_url=card.image,
            thumbnail_width=80,
            url=card.product_page,
            # TODO: convert numbers to latin digit from persian digit
            description=card.price_text,
            input_message_content=InputTextMessageContent(
                create_info_message(card=card),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            ),
        )
        for card in cards
    ]

    # send results as answer
    try:
        await update.inline_query.answer(results)
    except error.BadRequest:
        logger.exception("send inline query results raised an error :")


# footer


def main() -> None:
    """Run the bot."""

    # Create the Application and pass it your bot's token.
    PROXY = getenv("PROXY")
    TOKEN = getenv("TOKEN")

    if not TOKEN:
        raise ValueError("TOKEN field can't be empty !")

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
