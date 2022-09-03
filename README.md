# Torobot
a telegram bot to crawl and scrape data from [torob.com](https://torob.com) and display them in the telegram.

## Installation
clone the repository and go to the repo directory, then do as following : 
  
install the requirements :  
```bash
pip install -r requirements.txt
```
### Configuration :
set the configuration in `config.py`.  
  
- `TOKEN` :  
get your bot token from [BotFather](https://t.me/BotFather) (or if you don't have, make one there).
then put it in the `TOKEN`

- `PROXY` :  
if you want to use proxy to connect to the telegram, put your proxy url like the following :
  - `PROXY = 'socks5://127.0.0.1:9050'` : socks5 proxy
  - `PROXY = None` : non-proxy
  
  
## Run :  
finally run the program :
```bash
python bot.py
```
