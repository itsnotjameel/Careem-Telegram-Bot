import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import replymarkup, replykeyboardmarkup, replykeyboardremove
import sqlite3
import logging
import re
import code
from datetime import datetime
import random
import os
from sys import platform
import requests
from back_or_forward_slash import back_or_forward_slash
from secret_tokens import my_bot_token, commandpassword, screenshotfilename, screenshotpath
from sqlitedb import checkifsamedetails, checkifregistered, replacedata, enternewdata, deleteeverything

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

CAREEM, PHONE, ASK_ABOUT_PHONE, PHONECONFIRM, VERIFY, PASSWORD, SAVEINFO, PICKUP, DROPOFF = range(9)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

startcommandused = False
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                 text=f'Welcome to CareeemBot!\n Use /careem to start the ordering process \n To restart the machine, use /restart \n To take a screenshot, use /screenshot \n To give system commands, use /command [password] [command] \n Your User ID is: {update.effective_user.id}', 
                 reply_markup = ReplyKeyboardMarkup([["/careem", "/restart", "/screenshot"]], one_time_keyboard=True))
    global theuserid
    theuserid = update.effective_chat.id

    global startcommandused
    startcommandused = True

def careem(update, context):
    
    if startcommandused != True:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "You need to use the /start command first to register the User ID, try again")
        return
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Note: You can use the /cancel command to cancel the ordering process at any time. \nLoading the Careem webpage, please wait...")
    global driver
    driver = webdriver.Firefox()
    # VPN PROCESS BELOW, MIGHT NOT BE NEEDED IF YOU'RE IN A CAREEM-SUPPORTED COUNTRY
    # -----------------------------------------------------------------------------
    
    
    extension_dir = '/root/.mozilla/firefox/siro1t0y.default-release/extensions/' 
    extensions = [
        '{fca67f41-776b-438a-9382-662171858615}.xpi'
    ]
    for extension in extensions:
        driver.install_addon(extension_dir + extension, temporary=True)
    time.sleep(10)
    pyautogui.click(1220, 110) #extension icon
    time.sleep(3)
    pyautogui.click(1080, 570) #thanks
    time.sleep(3)
    pyautogui.click(1145,445) #agree
    time.sleep(3)
    pyautogui.click(1010,240) #us
    time.sleep(3)
    pyautogui.click(1035, 310) #algeria
    time.sleep(10)
    pyautogui.hotkey('ctrl', 'w')



    # -------------------------------------------------------------------
    # VPN PROCESS DONE

    driver.get("https://app.careem.com/rides")
    wait(
        driver, 30).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "selected-dial-code"))).click()
    wait(
        driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='+964']"))).click()
    global user
    user = driver.find_element_by_id('mobileNumber')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Careem page loaded! Send your phone number, using plain text.", reply_markup = ReplyKeyboardMarkup([["/cancel", "/restart", "/screenshot"]], one_time_keyboard=True))
    if checkifregistered(theuserid) == True:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You have saved info, would you like to use it? Type 'use' if you want to, or carry on like usual.", reply_markup = ReplyKeyboardMarkup([["use", "/cancel", "/restart", "/screenshot"]], one_time_keyboard=True))
    return PHONE
    

def restart(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Restarting, please wait for 30 seconds")
    time.sleep(5)
    os.system("sudo reboot")

def command(update, context):
    if commandpassword in update.message.text:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Correct password, executing")
        actualcommand = update.message.text.split(" ", 2)[2]
        command_output = os.popen(actualcommand).read()
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Output: \n {command_output}")

    elif commandpassword not in update.message.text:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Incorrect password, try using /command again")

def phone(update, context):
    if "use" in update.message.text.lower() and checkifregistered(theuserid) == True:
        global wantsavedinfo
        wantsavedinfo = True
        checkifregistered(theuserid)
        from sqlitedb import savednumber
        
        user.send_keys(str(savednumber))
        time.sleep(random.randint(3,10))
        wait(
        driver, 20).until(
        EC.element_to_be_clickable(
            (By.ID, "login-btn"))).click()
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Send me the code, use text")
        return VERIFY
    else:
        wantsavedinfo = False
        context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Please type anything and send it to pass to the next process", reply_markup = ReplyKeyboardMarkup([["okay"]], one_time_keyboard=True))
        
    phonenumberarray = []
    for i in update.message.text:
            if i in "0123456789":
                phonenumberarray.append(i)
    global goodphonenum
    goodphonenum = "".join(phonenumberarray)
    return ASK_ABOUT_PHONE


def ask_about_phone(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Are you sure? Send 'yes' if you are, or send 'no' if you want to use another number",
        reply_markup = ReplyKeyboardMarkup([["yes", "no", "/cancel", "/screenshot"]], one_time_keyboard=True))
    return PHONECONFIRM
    

def phoneconfirm(update, context):
    if "no" in update.message.text:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Okay, send me the correct number")
        return ASK_ABOUT_PHONE
    elif "yes" in update.message.text.lower():
        user.send_keys(str(goodphonenum))
        wait(
        driver, 20).until(
        EC.element_to_be_clickable(
            (By.ID, "login-btn"))).click()
        time.sleep(random.randint(3,10))
        wait(
            driver, 20).until(
            EC.element_to_be_clickable(
                (By.ID, "login-btn"))).click()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Send me the code, use text")
        return VERIFY
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I didn't get that, send me your correct phone number in plain text.")


numbers = []

if not os.path.exists(screenshotpath):
    if platform == "Windows":
        os.makedirs(screenshotpath.split("\\")[-1])
    else:
        os.makedirs(screenshotpath.split("/")[-1])

def screenshot(update, context):
    scr1 = pyautogui.screenshot()
    dt = back_or_forward_slash(screenshotpath, screenshotfilename)
    scr1.save(dt)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(
            dt,
            'rb'))


def verify(update, context):
    if hasNumbers(update.message.text):
        global code
        code = re.findall('\\d+', update.message.text) #get numbers from text
        form = driver.find_element_by_id('otp')
        form.send_keys(code)
        time.sleep(5)
        driver.find_element_by_id('login-btn').click()
        time.sleep(10)
        driver.find_element_by_css_selector('.material-form-field input').click()
        if wantsavedinfo != True:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Great, send your password, use text")
        elif wantsavedinfo == True:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please type anything and send it to pass to the next process", reply_markup = ReplyKeyboardMarkup([["okay"]], one_time_keyboard=True))  ##user needs to send something
            return PASSWORD
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="There isn't a number in the message you sent, try again")
    
    return PASSWORD


def password(update, context):
    
    if wantsavedinfo == True:
        from sqlitedb import savedpassword
        firstpassword = savedpassword
    else:
        firstpassword = update.message.text
    global goodpassword
    goodpassword = firstpassword
    time.sleep(5)
    driver.find_element_by_css_selector(
        '.material-form-field input').send_keys(str(goodpassword))
    time.sleep(5)
    driver.find_element_by_id('login-btn').click()
    time.sleep(30)
    timeout = 300
    try:
        element_present = EC.presence_of_element_located((By.ID, 'pickup_input'))
        wait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")
    time.sleep(30)
    driver.find_element_by_id("pickup_input").click()
    time.sleep(10)
    driver.find_element_by_xpath("//a[@class='savLocLink']").click()
    time.sleep(5)
    if wantsavedinfo != True:
        if  checkifsamedetails(theuserid, goodphonenum, goodpassword) == True:
            context.bot.send_message(chat_id = update.effective_chat.id, text= "The details you entered already exist in our database. You could type 'use' next time.")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please type anything and send it to pass to the next process", 
                reply_markup = ReplyKeyboardMarkup([["okay"]], one_time_keyboard=True))
            
        elif checkifsamedetails(theuserid, goodphonenum, goodpassword) != True:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Do you want me to save/overwrite the phone number and password for future use? Answer with 'yes or 'no' ",
                reply_markup = ReplyKeyboardMarkup([["yes", "no", "/cancel", "/restart", "/screenshot"]], one_time_keyboard=True))
    elif wantsavedinfo == True:
        context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Please type anything and send it to pass to the next process", reply_markup = ReplyKeyboardMarkup([["okay"]], one_time_keyboard=True))
    return SAVEINFO



def saveinfo(update, context):
    if "yes" in update.message.text.lower():
        if checkifregistered(theuserid) == True:
            replacedata(theuserid, goodphonenum, goodpassword)
        else:
            enternewdata(theuserid, goodphonenum, goodpassword)
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Data Saved")
    elif "no" in update.message.text.lower():
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Okay, data not saved")
    else:
        print("nothing happened")
    
    
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Type the pickup point using text, it must be in your saved locations (you can type a word unique to it and the bot will find it) ")
    return PICKUP

def pickup(update, context):

    global goodpickup
    goodpickup = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Tell me the dropoff point using text, it also must be in your saved locations.")
    return DROPOFF

def dropoff(update, context):
    global gooddropoff
    gooddropoff = update.message.text
    all_a = driver.find_elements_by_xpath(
        "//a[@class='locationList ng-binding ng-scope']")
    for a in all_a:
        if str(goodpickup).lower() in a.text.lower():
            a.click()
    time.sleep(5)
    driver.find_element_by_id('userLocation').click()
    time.sleep(6)
    driver.find_element_by_id('dropoff_input').click()
    time.sleep(6)
    driver.find_element_by_xpath(
        "//div[@class='col-sm-10 col-md-8 dropOffInputContainer']//a[contains(.,'Choose saved locations')]").click()
    time.sleep(5)
    all_b = driver.find_elements_by_xpath(
        "//a[@class='locationList ng-binding ng-scope']")
    for b in all_b:
        if str(gooddropoff) in b.text:
            b.click()
    time.sleep(2)
    driver.find_element_by_id('userLocation').click()
    time.sleep(5)
    driver.find_element_by_xpath(
        "//select[@id='paymentOptionsSelector']/option[text()='Cash']").click()
    time.sleep(3)
    dt2 = f"{back_or_forward_slash(screenshotpath, screenshotfilename)}"
    pyautogui.screenshot().save(dt2)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(
            dt2,
            'rb'))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Are you sure you want to order? Type '/confirm' in order to confirm when you want")        
    return ConversationHandler.END

def confirm(update,context):
    driver.find_element_by_class_name("btn actionBtn left-right ng-binding").click()
    context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="Ordering... Use /screenshot to view a screenshot of the status")  

def cancel(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Canceled the ordering process.")  
    return ConversationHandler.END

def main():
    updater = Updater(
        my_bot_token, #sensitive
        use_context=True)
    global dp
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("restart", restart))
    dp.add_handler(CommandHandler("screenshot", screenshot))
    dp.add_handler(CommandHandler("command", command))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('careem', careem)],

        states={
            PHONE: [MessageHandler(Filters.text, phone)],
            ASK_ABOUT_PHONE: [MessageHandler(Filters.text, ask_about_phone)],
            PHONECONFIRM: [MessageHandler(Filters.text, phoneconfirm)],
            VERIFY: [MessageHandler(Filters.text, verify)],
            PASSWORD: [MessageHandler(Filters.text, password)],
            SAVEINFO: [MessageHandler(Filters.text, saveinfo)],
            PICKUP: [MessageHandler(Filters.text, pickup)],
            DROPOFF: [MessageHandler(Filters.text, dropoff)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


main()
