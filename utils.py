from Torob.api import Card
import messages


def create_info_message(card: Card):
    # get stock status message
    if card.stock_status is None:
        stock_status_msg = ""
    else:
        stock_status_msg = messages.STOCK_STATUS_MESSAGE.format(
            stock_status=card.stock_status
        )
    # create message
    message = messages.SEARCH_RESULT_MESSAGE.format(
        name=card.name1.strip(),
        price=card.price_text,
        link=card.product_page,
        shop=card.shop_text.strip(),
        stock_status_m=stock_status_msg,
    )

    return message
