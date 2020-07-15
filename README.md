<a href="https://ibb.co/Yf30fNt"><img src="https://i.ibb.co/Yf30fNt/careembotlogo.png" alt="careembotlogo" border="0"></a>

<h3>This is a Telegram Bot made with Python that mainly initiates a conversation to order a Careem Taxi through Telegram, by logging in to the user's Careem account and ordering it.</h3>

<h4>It uses Selenium, SQLite, python-telegram-bot, among others to aid with the ordering process.</h4>

- python-telegram-bot is used to listen to the commands and messages that are sent to the bot through Telegram, and to neatly order the conversation without excessive use of commands.
- Selenium WebDriver is used to click buttons on Careem's webpage, and send keys to fill the forms using the data the user sent. 
- SQLite is used to save the data the user has sent in case the user wanted the sent data to be saved for later use. 

<h3>INSTRUCTIONS:</h3>

1. Create a Telegram bot, and get the bot token.
2. Create a file wth the name secret_tokens, and define your own bot_token, commandpassword (for commands), deletepassword (for deleting the entire database) variables.

<h3> DISCLAIMER: </h3>
<p> This has really bad code written all across it, but it should give you an idea about the XPATH's, ID's, and CSS Selectors for the Careem ordering UI. </p> 


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
