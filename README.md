 
# ISS BOT
Telegram bot to find when iss will pass over your location. Uses skyfield todo calculations and matplotlib to plot graphs.sends image showing where on sky iss will be visible and rise/set time

# Documentation
requires python 3.6+

**bot.py :** Is the bot and will reply to /allpasses and /visible

**send_times.py:** checks whether a visble pass is found for todayif found will send about it to a selected chatid. Can be setup as a cronjob to run everyday 



# Setup

Add token  to bot.py and send_times.py
change coords to your location in bot.py and send_times.py

```
pip install -r requirements.txt
python bot.py

```


# TODO
use enviroments variables to store location and token 
