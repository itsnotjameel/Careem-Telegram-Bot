<div align="center"><a href="https://ibb.co/Yf30fNt"><img src="https://i.ibb.co/Yf30fNt/careembotlogo.png" alt="careembotlogo" border="0"></a></div>

<h3 align="center">This is a Telegram Bot made with Python that mainly initiates a conversation to order a Careem Taxi through Telegram, by logging in to the user's Careem account and ordering it.</h3>

<h4>It uses python-telegram-bot, Selenium, threading, SQLite, PyAutoGUI, Matplotlib, and PIL Pillow to aid with the ordering process.</h4>

- python-telegram-bot is used to listen to the commands and messages that are sent to the bot through Telegram, and to neatly order the conversation without excessive use of commands.
- Selenium WebDriver is used to click buttons on Careem's webpage, and send keys to fill the forms using the data the user sent. 
- threading is used to start the startAdminCountdown function in parallel to limit an admin session's time based on the length specified by the user.
- SQLite is used to save the data the user has sent in case the user wanted the sent data to be saved for later use. 
- PyAutoGUI is used to take screenshots, I'm using this instead of ImageGrab from PIL because it is compatible for most operating systems
- Matplotlib is used to process screenshots from PyAutoGUI, add grids onto them, and draw a dot at the user's requested coordinates (should a user request so)
- PIL Pillow is used to take the images produced by Matplotlib and crop them automatically to make the most out of their resolution

<h3 align="center"><b>INSTRUCTIONS:</b></h3>

1. Create a Telegram bot, and get the bot token.
2. Create a secret_tokens.py file in the same folder, use the ideal file below, or define your own `bot_token, commandPassword, clickPassword, deletePassword, dbName, screenshotFileName.`
3. Execute `careem-telegram-bot.py`

<h5>Ideal secret_tokens.py file:</h5>

```python
from datetime import datetime
my_bot_token = "Bot Token Here" # Telegram Bot Token
dbName = "telegram_bot_users.db" # Database Name
screenshotFolderName = "Careem-Bot-Screenshots" # Screenshot Folder Name
screenshotFileName = screenshotFolderName + "/screengrab-" + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".png" # Screenshot File Name
commandPassword = "System Commands Password Here"
clickPassword = "GUI Control (Coords, Click, Doubleclick, Keyboard) Password Here"
deletePassword = "DB Deletion Password Here"
adminSessionLength = 900 # length of time a person has the admin attribute (isAdmin), in seconds
```

Only things you need to change here are `my_bot_token`, `commandPassword`, `clickPassword`, `deletePassword`. `screenshotFileName` has a timestamp on it.

<h3 align="center"> FUNCTIONS INCLUDED: </h3>

- `hasNumbers`: checks for numbers in string and returns them in order. Mainly used to get the verification code. You could probably replace this with a simple for loop.

- `start`: Gives introductory message. Also collects user ID, which is necessary for the /careem function database. So it must be triggered before /careem.

- `careem`: Is the main ordering process, launches Firefox with Selenium Webdriver, (unnecessary, remove it on your own computer) starts VPN, opens Careem page. Checks if user is registered within database:
    * -> if so, it asks the user if they want to use the registered info 
    * -> if user doesn't have info, it asks for phone number

- `startAdminCountdown`: Starts a timer in parallel when triggered in the passwordprocess function, length on default is 900 seconds (15 minutes). Sleeps with the specified length, then redefines isAdmin as false, so the user has to reenter the password.

- `passwordprocess`: Function that has a wrapper inside a decorator, takes the required password as an argument and checks if it's included in update.message.text (the user's latest message). 
    
    If user is not admin:
    * -> try checking if password is included
        * -> if a password is included but it's not the password required, send user message indicating it's the wrong password and return None. 
        -> If exception happened (user hasn't entered a password or any arguments), send message indicating user is using wrong syntax and return None. 
    * -> If the function the password is being checked on is /admin -> Activate isAdmin status and trigger startAdminCountdown.

    Else if user is admin:
    * -> Add the required password automatically as the second word of user's message to be passed onto the function the user needs. (For example, normal /click function trigger is /click PASSWORD x y, user will only enter /click x y as an admin, and PASSWORD will be added from the function if user is admin).

- `phone`: 

    If user has saved info: 
    * -> Checks if user wants to use it 
        * -> If user has it but doesn't want to use 
            * -> checks for number in message. 
        * -> Else if user doesn't have saved info 
            * -> Checks for number

- ask_about_phone: Asks if user is sure about phone number if they doesn't use saved info.

- `verify`: User sends verification code: 
    * If it has numbers: 
        * -> enters it, then asks for password from user.   
    * If there is no number:
        * -> send user error message and repeat process when user sends another message

- `password`: 

    * If user wants to use saved info:
        * -> enter saved number, ask for verification code from user, enter it, put in saved password, ordering page loads. 

    * Else if user does not have saved password:
        * -> take password from text, put it in, ordering page loads. 
    
    * If user didn't want saved info (meaning they didn't have it or don't want to use same details):
        * if all details are the same and they have registered info in database
            * -> Send message saying they could use their saved info next time. 
            
        * Else if they don't want saved info and have saved info but it's not the same:
            * -> Ask if they want to overwrite their old info. 
        
        * -> Else if they don't want saved info and don't have save info:
            * -> ask if they want to save their info. 
        
    * Else if they wanted saved info:
        * -> do nothing and continue.

- `saveinfo`: If user wants to save info:
    * -> Check if user has already registered with different info:
        * -> if yes:
            * -> only replace the data 
        * -> if no and user doesn't have registered info:
            * -> make new data. 
        
    Send message asking user to send pickup point. 

    The pickup point: 
    1. must be in saved locations 
    2. is case sensitive 
    3. word must be unique to saved location user wants

- `pickup`: Takes pickup point from user message, asks for dropoff

- `dropoff`: Takes dropoff from user message, continues through page, chooses cash as payment method, takes a screenshot and sends it to user. Asks user if they are sure about ordering: 
    * -> if yes:
        * -> they should send the command /confirm. Ends conversation in the conversationhandler.

- `confirm`: Once command is received, it clicks on confirm button and sends user a message saying it's ordering.

- `cancel`: Can cancel conversation midway, unstable at the moment.

- `restart`: Restarts entire machine with sudo reboot, only works with Linux.

- `command`: Takes command from message, returns terminal output, cannot be used as Python terminal at the moment.

- `showcoords`: Exists in `showcoords.py`. Defines mouseclickfile which is the full path of the screenshot PyAutoGUI takes, and mousechartfile, which is where the matplotlib figure is saved. Defines grid separation amount, puts text, grids, major ticks, saves figure to mousechartfile, opens image with PIL, defines trim function (which automatically crops image and trims whitespace to make the most out of resolution), trims image, and overwrites it to mousechartfile.

- `coords`: Triggers showcoords() function and sends image to user with a grid on top of a screenshot with coordinates

- `showdot`: Does everything coords does, and adds a dot to where the user wants the dot's coordinates to be.

- `click`: Clicks based on user's coordinates with PyAutoGUI.

- `doubleclick`: Clicks based on user's coordinates with PyAutoGUI.

- `keyboard`: Writes with PyAutoGUI the string a user sends.

- `main`: Starts up all handlers, and connects with bot through token.

<h3> DISCLAIMER: </h3>
<p> This has really bad code written all across it, but it should give you an idea about the XPATH's, ID's, and CSS Selectors for the Careem ordering UI. </p> 


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
