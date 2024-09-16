from datetime import datetime, timedelta
import os
import traceback
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import aiohttp
import asyncio
import pyautogui

BASE_DIR = r"C:\Users\Administrator\Desktop\sporty-1.2_every_sec"


def login(driver, phone, paswd):
    try:
        mobile_input = driver.find_element(By.CSS_SELECTOR, 'input[type="tel"].m-input-wap')
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"].m-input-wap')

        # Perform actions with the element if needed
        mobile_input.send_keys(phone)
        password_input.send_keys(paswd)
        
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[data-op="login-btn"]')
        login_button.click() 

        time.sleep(2)
    except :
        print('couldnt log in')



def make_sure_website_up(driver):
    try: 
        disconnect_message = driver.find_element(By.CSS_SELECTOR, "app-disconnect-message")
        driver.refresh()
        if(disconnect_message):
            driver.refresh()
    except: 
        pass



def get_multipliers(driver):
    multiplier_list = []

    multipliers = driver.find_elements(By.CSS_SELECTOR, "div.payouts-block app-bubble-multiplier")[:2]
    for e in multipliers:
        text_num = e.text.split('x')[0]
        if text_num != "":
            multiplier_list.append(text_num)

    return multiplier_list


async def send_telegram_msg(msg):
    token = "7383529443:AAHztCuaDFvQ2_KU9Vl7dqsQ82E-6jLsqq4"
    # gc_id = '-1002160352322'
    gc_id = '6966902490'
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={gc_id}&text={msg}&allow_sending_without_reply=True"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def send_telegram_msg_2(msg):
    token = "7383529443:AAHztCuaDFvQ2_KU9Vl7dqsQ82E-6jLsqq4"
    # gc_id = '6966902490'
    gc_id = '6966902490'
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={gc_id}&text={msg}&allow_sending_without_reply=True"

    requests.get(url)

   
   



def input_stake(driver, num):
    try:
        stake_input = driver.find_element(By.CSS_SELECTOR, "app-spinner input")
        driver.execute_script("arguments[0].select();", stake_input)
        stake_input.send_keys(f"{num}")
    except Exception as e:
        # print(traceback.format_exc())
        print(f"error from input_stake")

def make_sure_auto_close(driver, sl=1.5):
    try:
        auto_element = driver.find_element(By.XPATH, "//button[contains(text(), 'Auto')]")
        class_attribute = auto_element.get_attribute("class")
        # print(f"class attribut is {class_attribute}")
        if "active" not in class_attribute.split():
            # screenshot = pyautogui.screenshot()
            # # Save the screenshot to a file
            # screenshot_path = os.path.join(BASE_DIR, "AutoClose.png")
            # screenshot.save(screenshot_path)
            auto_element.click()
            auto_element_switcher = driver.find_element(By.CSS_SELECTOR, "div.cash-out-switcher div.input-switch")
            class_atrr = auto_element_switcher.get_attribute("class")
            if "off" in class_atrr.split():
                auto_element_switcher.click()
        
        auto_element_input = driver.find_element(By.CSS_SELECTOR, "div.spinner.small input")
        driver.execute_script("arguments[0].select();", auto_element_input)
        auto_element_input.send_keys(f"{sl}")
    except Exception as e:
        print(traceback.format_exc())
        print("error from make_sure_auto_close")
        # send_telegram_msg_2(f"Auto CLose Error \n\n\n {traceback.format_exc()}")
        error_message = str(type(e).__name__)
        send_telegram_msg_2(f"Bot Error \n\n {error_message}")

    
        
        
    
def click_bet_button(driver):
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.btn-success.bet.ng-star-inserted")
        if len(buttons)==2:
            buttons[0].click()
            return True
        else:
            return False
    except Exception as e:
        # print(traceback.format_exc())
        print("error from click_bet_button")

    
def click_cancel_button(driver):
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.btn-danger.bet.height-70.ng-star-inserted")
        buttons[0].click()
        return True
    except Exception as e:
        # print(traceback.format_exc())
        print("error from click_cancel_button")
        return False


def check_for_invalid_input_stake(driver, correct_stake):
    try:
        stake_input = driver.find_element(By.CSS_SELECTOR, "app-spinner input")
        print(f"current stake value is {stake_input.get_property('value')}")
        if int(float(stake_input.get_property('value'))) != int(correct_stake):
            click_cancel_button(driver)
    except Exception as e:
        print(f"Error from input_stake: {e}")


def get_bet_history_losses(driver):
    bet_history_element = driver.find_element(By.XPATH, "//button[contains(text(), 'My Bets')]")
    bet_history_element.click()
    
    try:
        betHistory = driver.find_element(By.CSS_SELECTOR, "div.h-100.scroll-y")
        betHistory_text = betHistory.text
        betHistory_text = betHistory_text.replace(" ", "").replace("\n", "")
        # print(betHistory_text)
        # input('text is')
        lastbetElement = driver.find_element(By.CSS_SELECTOR, "app-bet-item")
    except:
        betHistory_text = None
        lastbetElement = None
         
    return betHistory_text, lastbetElement




def is_last_2_bet_history_set(list):
     if(len(list) < 2):
        return False
     else:
        time1 = datetime.strptime(list[0], '%H:%M')
        time2 = datetime.strptime(list[1], '%H:%M')
        time_difference = abs((time2 - time1).total_seconds())
        if time_difference <= 300:
            print("The times are less than 5 minutes apart.")
            return True
        else:
            print("The times are more than 5 minutes apart.")
            return False
        
# def old_set(list):
#     time1 = datetime.strptime(list[0], '%H:%M')
#     now = datetime.now().strftime('%H:%M')
#     time_now = datetime.strptime(now, '%H:%M')
#     time_difference = abs(time_now - time1)

#     # Check if the difference is more than 5 minutes
#     if time_difference > timedelta(minutes=30):
#         input_stake(driver, num=stakes[stake_index])
#         make_sure_auto_close(driver)
#         click_bet_button(driver)


def get_money_balance(driver):
    balance = driver.find_element(By.CSS_SELECTOR, "span.amount.font-weight-bold")
    balance_text =balance.text.replace(',', '')
    print(f'balance is {balance_text}')
    return float(balance_text)

                            

# button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-success.bet.ng-star-inserted")
# # class="btn btn-success bet ng-star-inserted"              bet button
# # class="btn btn-warning cashout ng-star-inserted"          cashout button
# # class="btn btn-danger bet height-70 ng-star-inserted"     waiting button 

def get_trade_elements(element, stake_list):
    date_element = element.find_element(By.CLASS_NAME, "date")
    date_text = date_element.text.strip()

    # Extract the bet amount
    bet_amount_element = element.find_element(By.TAG_NAME, "app-bet-amount")
    bet_amount_text = bet_amount_element.text.strip()
    bet_amount_text = float(bet_amount_text.replace(',', ''))

    # Extract the multiplier
    multiplier_element = element.find_element(By.CLASS_NAME, "bubble-multiplier")
    multiplier_text = multiplier_element.text.strip()
    multiplier_text = multiplier_text.split("x")[0]
    multiplier_text = float(multiplier_text)

    # Extract the cash-out amount
    try:
        result = element.find_element(By.CLASS_NAME, "cash-out")
        result = result.text.strip()
        result = float(result.replace(',', ''))
        result = result - bet_amount_text
        
    except:
        result = f"-{bet_amount_text}"
        result = float(result)

    try:
        curr_stk_indx = stake_list.index(bet_amount_text)
    except:
        curr_stk_indx = 0



    bet_item_data = {
            "date": date_text,
            "bet_amount": bet_amount_text,
            "multiplier": multiplier_text,
            "curr_stk_indx":curr_stk_indx,
            "result": result
        }
    
    return bet_item_data
            

def has_mins_passed_for_trade(last_bet_time, check_secs):
    current_time = datetime.now()
    # Check if the current time is more than 2 minutes ahead of the given time
    if current_time > last_bet_time + timedelta(seconds=check_secs):
        print('seconds passed')
        return True
    else:
        print(' seconds havent passed yet')
        return False


def take_screenshot(driver):
        screenshot = driver.get_screenshot_as_png()
        # Save the screenshot to the current working directory
        screenshot_path = os.path.join(os.getcwd(), f"{BASE_DIR}\\screenshot.png")

        with open(screenshot_path, "wb") as file:
            file.write(screenshot)

        print(f"Screenshot saved to: {screenshot_path}")