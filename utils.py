from Torob.api import Card
import messages
import re


def escape_markdown(text: str) -> str:
    # Define the special characters to escape in Markdown
    special_characters = r"([_*{}\[\]()#+.!|-])"

    # Use a regular expression to find all special characters and escape them
    escaped_text = re.sub(special_characters, r"\\\1", text)

    return escaped_text


def create_info_message(card: Card):
    # get stock status message
    if card.stock_status is None:
        stock_status_msg = ""
    else:
        stock_status_msg = messages.STOCK_STATUS_MESSAGE.format(
            stock_status=card.stock_status
        )

    # set shop_text based on available
    if card.is_available:
        shop_text = messages.EXISTS_IN_SHOP
    else:
        shop_text = messages.SHOW_IN_SHOP

    # create message
    message = messages.SEARCH_RESULT_MESSAGE.format(
        name=escape_markdown(card.name1.strip()),
        price=card.price_text,
        link=card.product_page,
        shop_text=shop_text,
        shop=card.shop_text.strip(),
        stock_status_m=stock_status_msg,
    )

    return message
