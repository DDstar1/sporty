from datetime import datetime, timedelta
import json
import os
import random
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import db
from utils import BASE_DIR, login, check_for_invalid_input_stake, take_screenshot, click_bet_button, click_cancel_button, get_bet_history_losses, get_multipliers, has_mins_passed_for_trade, input_stake, get_trade_elements, make_sure_auto_close, make_sure_website_up, send_telegram_msg, get_money_balance


import asyncio
import aiohttp

from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC




# Open the website
with open(f'{BASE_DIR}/demo_url.txt', 'r', encoding='utf-8') as file:
    sporty_demo_url = file.read()



def random_60_to_300():
    return random.randint(60, 120)

def get_current_stakes(starting_balance,curr_stake, threshold):
    num_increments = int(starting_balance // threshold)
    if(num_increments > 1):
        adjusted_stakes = [s * num_increments for s in curr_stake]
        return adjusted_stakes
    else: 
        return curr_stake



# with open('main_page.html', 'w', encoding='utf-8') as file:
#     file.write(driver.page_source)

async def main_loop():
    # global frame_switched,skip_until, stale_element_counter, old_multipliers, old_bet_his_text, can_trade, get_next_mutiplier, wait_for_6_losses_to_pass, stake_index, old_last_element_date, old_balance, last_inserted_trade,last_bet_time

    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # To run Chrome in headless mode (no GUI)

    driver = webdriver.Chrome(options=chrome_options)


    # Get the screen width and height
    screen_width = driver.execute_script("return window.screen.width;")
    screen_height = driver.execute_script("return window.screen.height;")
    # Calculate the desired window width (70% of the screen width)
    desired_width = int(screen_width * 0.9)
    # Set the browser window to 70% of the screen's width and full height
    driver.set_window_size(desired_width, screen_height)


 
    driver.get(sporty_demo_url)

    # input("login now ?")
    time.sleep(3)
    login(driver, 8151725194, 'spcapmarvel7S')





    SCRIPT_STARTED = datetime.now()
    Send_update_time= datetime.now()

    skip_until = None
    old_multipliers = []
    old_bet_his_text = None
    can_trade = True
    # stakes = [30,210, 1000, 4200]
    # stakes = [10, 20, 60, 180, 300]
    # stakes = [75, 375, 2250]
    # stakes = [10,10,10,10]

    # stakes = [20,30, 60]
    # stakes = [10,11,22,45]
    initial_stake = [10, 20, 30, 40, 60, 80, 100, 120]
    # stakes = [10,10]
    # stakes = [10, 15, 30, 60, 120, 240, 480, 960, 1200 ]
    # stakes = [10, 20, 30, 40, 60, 90, 140, 210, 310, 470, 700 ]

    # stakes = [10, 12, 25, 53,112,240]

    last_bet_time =datetime.now()
    frame_switched = False
    aux_can_trade = False

    await send_telegram_msg('Server has started')




    while True:
        try:
            try:
                if(frame_switched != True):
                    driver.switch_to.default_content()

                    first_iframe = driver.find_element(By.CSS_SELECTOR, "iframe#turbo-games\/aviator")
                    driver.switch_to.frame(first_iframe)

                    second_iframe = driver.find_element(By.CSS_SELECTOR, "iframe.turbo-games-iframe")
                    driver.switch_to.frame(second_iframe)

                    print(f'iframe is {second_iframe}')
                    frame_switched = True
                    
            except Exception as e:
                print('no frame')
                print(traceback.format_exc())
                continue

        
            try:
                print(f'my money balance is {get_money_balance(driver)}')
            except Exception as e:
                # await send_telegram_msg('Server should be restarted')
                # time.sleep(600)
                if datetime.now() - SCRIPT_STARTED > timedelta(hours=1):
                    await send_telegram_msg('Restarting Script')
                    # os.system('shutdown /r /t 1 /c "System maintenance required"')
                    driver.quit()
                    break


            stakes = get_current_stakes(get_money_balance(driver), initial_stake, 500)
   

            # await asyncio.sleep(0.5)

            print('---------------------1-------------------')


            if old_multipliers == []:
                old_multipliers = get_multipliers(driver)

            try:
                new_multipliers = get_multipliers(driver)              
                
                if new_multipliers[:2] != old_multipliers[:2]:
                    old_multipliers = new_multipliers
                    if len(old_multipliers) > 5:
                        old_multipliers.pop()
                    db.insert_data(date=datetime.now(), number=new_multipliers[0])
                    # await send_telegram_msg('Still inserting in db')
            except:
                print("stale multiplier elements")
                stale_element_counter += 1
                if(stale_element_counter >= 5):
                    stale_element_counter = 0
                    driver.refresh()
                pass

            print('---------------------2-------------------')

            new_bet_his_text, last_element_history = get_bet_history_losses(driver)

            # print(f"balance compare is {old_bet_his_text}  {new_bet_his_text} \n is equal == {old_bet_his_text==new_bet_his_text}")


                

            # if old_bet_his_text != new_bet_his_text and last_element_history is not None:
            #     elements = get_trade_elements(last_element_history, stake_list=stakes)
                    
            #     if(float(elements["result"]) < 0): 
            #         next_stk_indx = int(elements["curr_stk_indx"]) + 1
            #         if(next_stk_indx > len(stakes)-1):
            #             next_stk_indx = 0
                    
            #         # skip_until = skip_until = datetime.now() + timedelta(seconds=7)
            #         skip_until = skip_until = datetime.now() + timedelta(seconds=20)  # Skip next 5 minutes

            #         aux_can_trade = True

            #         # take_screenshot(driver)
            #     else:
            #         next_stk_indx = 0

            #     db.insert_trade(date=datetime.now(), stake=elements["bet_amount"], multiplier=elements["multiplier"], result=elements['result'], curr_stk_indx=elements['curr_stk_indx'],next_stk_indx=next_stk_indx)
            #     old_bet_his_text = new_bet_his_text
                
            #     if datetime.now() > Send_update_time:
            #         await send_telegram_msg(f"Balance = {get_money_balance(driver)}\n Profit = {db.get_results()}")
            #         Send_update_time = datetime.now() + timedelta(hours=5)
                
            
            #     if(float(elements["result"]) > 0):
            #         input_stake(driver, num=stakes[db.get_latest_next_stk_indx()])
            #         make_sure_auto_close(driver)
            #         click_bet_button(driver)
            #         print('button clicked')
            #         last_bet_time = datetime.now()


            # print('---------------------3-------------------')

            # last_stake_and_result = db.get_last_stake_and_result()
            # last_stake = last_stake_and_result['stake']
            # last_result = last_stake_and_result['result']

            # if skip_until and datetime.now() < skip_until:
            #     print('skipping trade cause 2mins havent passed yet')

            #     continue

            # elif(aux_can_trade == True):
            #     input_stake(driver, num=stakes[db.get_latest_next_stk_indx()])
            #     make_sure_auto_close(driver)
            #     click_bet_button(driver)
            #     print('Auxilliary button clicked')
            #     last_bet_time =datetime.now()
            #     aux_can_trade = False
            

            # elif(aux_can_trade == False and has_mins_passed_for_trade(last_bet_time,40 )==True ):
            #     #  and       last_stake != stakes[db.get_latest_next_stk_indx()] ) or( stakes[db.get_latest_next_stk_indx()] == stakes[0]) and last_result>0    
            #     input_stake(driver, num=stakes[db.get_latest_next_stk_indx()])
            #     make_sure_auto_close(driver)
            #     click_bet_button(driver)
            #     last_bet_time =datetime.now()
            #     print('Auxilliary button clicked from staying too long')
 
        

            print('---------------------4-------------------')
        except Exception as e:
            print(f"Error from main.py \n")
            print(traceback.format_exc())
            error_message = str(type(e).__name__)
            await send_telegram_msg(f"Bot Error \n\n {error_message}")


           
        

# Run the main loop
while True:
    asyncio.run(main_loop())
