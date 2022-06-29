# Torobot
a telegram bot to crawl and scrape data from [torob.com](https://torob.com) and display them in the telegram.

## Installation
clone the repository and go to the repo directory, then do as following : 
  
install the requirements :  
```bash
pip install -r requirements.txt
```

### Bot Token
get your robot token from [BotFather](https://t.me/BotFather) (or if you don't have, make one there) then put it in the `bot.py` in main function `TOKEN = 'token'`.


finally run the program :
```bash
python bot.py
```

### proxy
if you want to use proxy to connect to the telegram, you have to make `use_proxy = True` and put your proxy url in `PROXY = '...'` in `bot.py` in main function
