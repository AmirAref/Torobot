import requests
from pydantic import BaseModel, Field


class Card(BaseModel):
    """this object store the information of a Shoping Item"""

    name1: str
    name2: str
    price: int
    image: str = Field(validation_alias="image_url")
    product_page_slug: str = Field(validation_alias="web_client_absolute_url")
    info_url: str = Field(validation_alias="more_info_url")
    shop_text: str

    @property
    def product_page(self) -> str:
        return f"https://torob.com{self.product_page_slug}"


def get_torob_cards(query: str, count: int = 24) -> list[Card]:
    """this method will extracts data from torob.com by the query"""
    # request arguments
    url = "https://api.torob.com/v4/base-product/search/"
    json_data = {
        "q": query,
        "page": 1,
        "size": count,
    }
    headers = {"Content-Type": "application/json"}
    # send request and get response
    response = requests.get(url, params=json_data, headers=headers)
    # parse data
    data = response.json()
    cards = [Card.model_validate(item) for item in data["results"]]
    # out
    return cards

