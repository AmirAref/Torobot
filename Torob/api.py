import requests

class Card:
    def __init__(self, **kwargs) -> None:
        """ this object store the information of a Shoping Item """
        self.name1 = kwargs['name1']
        self.name2 = kwargs['name2']
        self.price = kwargs['price']
        self.image = kwargs['image_url']
        self.product_page = "https://torob.com" + kwargs['web_client_absolute_url']
        self.info_url = kwargs['more_info_url']
        self.shop_text = kwargs['shop_text']
    
    def __str__(self) -> str:
        return f"{self.name1} ({self.name2}) : {self.price}"
        
class Torob:
    def __init__(self, query: str) -> None:
        """ a module to extract data from torob.com """
        self.query = query
        self._next = False # store the next page url

    def get_result(self, count=24) -> list[Card]:
        """ this method will extracts data from torob.com by the query"""
        if self._next:
            # has next link as before
            response = requests.get(self._next)
        else:
        # request arguments
            url = "https://api.torob.com/v4/base-product/search/"
            json_data = {
                'q' : self.query,
                'page' : 1,
                'size' : count,
            }
            headers = {'Content-Type': 'application/json'}
            # send request and get response
            response = requests.get(url, params=json_data, headers=headers )
        # parse data
        data = response.json()
        self._next = data['next']
        cards = [Card(**item) for item in data['results']]
        # out
        return cards