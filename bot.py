from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram import error
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
import logging
from uuid import uuid4
from Torob import Torob

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and

# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    await update.message.reply_text("Hello my friend !")


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
            id=str(uuid4()), title=card.name1, thumb_url=card.image,
            thumb_width=80, url=card.product_page, description=f'{card.price:,} تومان',
            input_message_content=InputTextMessageContent('🛍 **{}**\n💰 {:,} تومان\n🛒 [موجود {}]({})'.format(card.name1, card.price, card.shop_text, card.product_page), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True),
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
    use_proxy = False # True if you want to use or False you do not want
    TOKEN = 'token'
    PROXY = 'socks5://127.0.0.1:9050'
    
    if use_proxy:
        application = Application.builder().token(TOKEN).proxy_url(PROXY).get_updates_proxy_url(PROXY).build()
    else:
        application = Application.builder().token(TOKEN).build()
        
    # add the handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))


    # Run the bot until the user presses Ctrl-C
    application.run_polling()



if __name__ == "__main__":
    main()