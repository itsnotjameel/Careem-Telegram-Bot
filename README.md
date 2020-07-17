<a href="https://ibb.co/Yf30fNt"><img src="https://i.ibb.co/Yf30fNt/careembotlogo.png" alt="careembotlogo" border="0"></a>

<h3>This is a Telegram Bot made with Python that mainly initiates a conversation to order a Careem Taxi through Telegram, by logging in to the user's Careem account and ordering it.</h3>

<h4>It uses Selenium, SQLite, python-telegram-bot, among others to aid with the ordering process.</h4>

- python-telegram-bot is used to listen to the commands and messages that are sent to the bot through Telegram, and to neatly order the conversation without excessive use of commands.
- Selenium WebDriver is used to click buttons on Careem's webpage, and send keys to fill the forms using the data the user sent. 
- SQLite is used to save the data the user has sent in case the user wanted the sent data to be saved for later use. 

<h3>INSTRUCTIONS:</h3>

1. Create a Telegram bot, and get the bot token.
2. Create a secret_tokens.py file in the same folder, use the ideal file below, or define your own `bot_token, commandpassword, deletepassword,  dbname, dbpath, screenshotpath, screenshotfilename`

<h5>Ideal secret_tokens.py file:</h5>

```python
from datetime import datetime
from back_or_forward_slash import back_or_forward_slash
import os
my_bot_token = "Bot Token Here"
commandpassword = "Password Here"
deletepassword = "Password Here"
dbname = "databasenamehere.db"
dbpath = r"{path}".format(path=os.getcwd())
screenshotpath = r"{path}".format(path=back_or_forward_slash(os.getcwd(), "Careem-Bot-Screenshots"))
screenshotfilename = "screengrab-" + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".png"
```

<p>Only things you need to change here are my_bot_token, commandpassword, deletepassword, dbname. DBPath, screenshotpath are based on your current working directory, and screenshotfilename has a timestamp on it.</p>

<h3> DISCLAIMER: </h3>
<p> This has really bad code written all across it, but it should give you an idea about the XPATH's, ID's, and CSS Selectors for the Careem ordering UI. </p> 


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
