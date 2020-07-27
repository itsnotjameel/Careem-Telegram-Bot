<a href="https://ibb.co/Yf30fNt"><img src="https://i.ibb.co/Yf30fNt/careembotlogo.png" alt="careembotlogo" border="0"></a>

<h3>This is a Telegram Bot made with Python that mainly initiates a conversation to order a Careem Taxi through Telegram, by logging in to the user's Careem account and ordering it.</h3>

<h4>It uses Selenium, SQLite, python-telegram-bot, Matplotlib, Pillow, PyAutoGUI to aid with the ordering process.</h4>

- python-telegram-bot is used to listen to the commands and messages that are sent to the bot through Telegram, and to neatly order the conversation without excessive use of commands.
- Selenium WebDriver is used to click buttons on Careem's webpage, and send keys to fill the forms using the data the user sent. 
- SQLite is used to save the data the user has sent in case the user wanted the sent data to be saved for later use. 
- PyAutoGUI is used to take screenshots, I'm using this instead of ImageGrab from PIL because it is compatible for most operating systems
- Matplotlib is used to process screenshots from PyAutoGUI, add grids onto them, and draw a dot at the user's requested coordinates (should a user request so)
- PIL Pillow is used to take the images produced by Matplotlib and crop them automatically to make the most out of their resolution

<h3> FUNCTIONS INCLUDED: </h3>

- hasNumbers: checks for numbers in string and returns them in order. Mainly used to get the verification code. You could probably replace this with a simple for loop.
- start: Gives introductory message. Also collects user ID, which is necessary for the /careem function database. So it must be triggered before /careem.
- careem: Is the main ordering process, launches Firefox with Selenium Webdriver, (unnecessary, remove it on your own computer) starts VPN, opens Careem page, checks if user is registered within database, if so, it asks the user if he/she wants to use the registered info, if user doesn't have info, it asks for phone number
- phone: If user has saved info -> Checks if user wants to use it, if user has it but doesn't want to use, checks for number in message. Else if user doesn't have saved info -> Checks for number
- ask_about_phone: Asks if user is sure about phone number if he doesn't use saved info.
- phoneconfirm: Checks if user said they're sure about phone number, if no -> repeat ask_about_phone process, if yes -> continue through site, and ask user for verification code. Else if there isn't phone number in message in first place, sends error message to user and goes back to ask_about_phone once user sends another message
- verify: User sends verification code, if it has numbers -> enters it, then asks for password from user. If there is no number -> send user error message and repeat process when user sends another message
- password: If user wants to use saved info -> enter saved number, ask for verification code from user -> enter it -> put in saved password -> ordering page loads. Else if user does not have saved password -> take password from text, put it in -> ordering page loads. If user didn't want saved info (meaning he doesn't have it or doesn't want to use his same details) -> if all details are the same and they have registered info in database -> Send message saying they could use their saved info next time. Else if they don't want saved info and have saved info but it's not the same -> Ask if they want to overwrite their old info. Else if they don't want saved info and don't have save info -> ask if they want to save their info. Else if they wanted saved info -> do nothing and continue.
- saveinfo: If user wants to save info -> Check if user has already registered with different info, if yes -> only replace the data, if no and user doesn't have registered info -> make new data. Send message asking user to send pickup point. The pickup point: 1. must be in saved locations 2. is case sensitive 3. word must be unique to saved location user wants
- pickup: Takes pickup point from user message, asks for dropoff
- dropoff: Takes dropoff from user message, continues through page, chooses cash as payment method, takes a screenshot and sends it to user. Asks user if they are sure about ordering, if yes they should send the command /confirm. Ends conversation in the conversationhandler.
- confirm: Once command is received, it clicks on confirm button and sends user a message saying it's ordering.
- cancel: Can cancel conversation midway, unstable at the moment.
- restart: Restarts entire machine with sudo reboot, only works with Linux.
- command: Takes command from message, returns terminal output, cannot be used as Python terminal at the moment.
- showcoords: Exists in showcoords.py. Defines mouseclickfullpath which is the full path of the screenshot PyAutoGUI takes, and mousechartfullpath, which is where the matplotlib figure is saved. Defines grid separation amount, puts text, grids, major ticks, saves figure to mousechartfullpath, opens image with PIL, defines trim function (which automatically crops image and trims whitespace to make the most out of resolution), trims image, and overwrites it to mousechartfullpath.
- coords: Triggers showcoords() function and sends image to user with a grid on top of a screenshot with coordinates
- showdot: Does everything coords does, and adds a dot to where the user wants the dot's coordinates to be.
- click: Clicks based on user's coordinates with PyAutoGUI.
- doubleclick: Clicks based on user's coordinates with PyAutoGUI.
- keyboard: Writes with PyAutoGUI the string a user sends.
- main: Starts up all handlers, and connects with bot through token.


<h3>INSTRUCTIONS:</h3>

1. Create a Telegram bot, and get the bot token.
2. Create a secret_tokens.py file in the same folder, use the ideal file below, or define your own `bot_token, commandpassword, clickpassword, deletepassword, dbname, dbpath, screenshotpath, screenshotfilename`

<h5>Ideal secret_tokens.py file:</h5>

```python
from datetime import datetime
from back_or_forward_slash import back_or_forward_slash
import os
my_bot_token = "Bot Token Here"
commandpassword = "Password Here"
clickpassword = "Password Here"
deletepassword = "Password Here"
dbname = "databasenamehere.db"
dbpath = r"{path}".format(path=os.getcwd())
screenshotpath = r"{path}".format(path=back_or_forward_slash(os.getcwd(), "Careem-Bot-Screenshots"))
screenshotfilename = "screengrab-" + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".png"
```

<p>Only things you need to change here are my_bot_token, commandpassword, clickpassword, deletepassword, dbname. DBPath, screenshotpath are based on your current working directory, and screenshotfilename has a timestamp on it.</p>

<h3> DISCLAIMER: </h3>
<p> This has really bad code written all across it, but it should give you an idea about the XPATH's, ID's, and CSS Selectors for the Careem ordering UI. </p> 


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
