from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re
import pandas as pd

#change your personal path
chrome_path=r"/Users/kikkosmac/Desktop/chromedriver"

def get_currencies(assets, start, end):
    frames = []
    for asset in assets:
        m=re.search("\/(.*)",asset)
        name=m.group(1)
        while True:
            try:
                # Opening the connection and grabbing the page
                my_url = f'https://www.investing.com/{asset}-historical-data'
                option = Options()
                option.headless = False
                driver = webdriver.Chrome(chrome_path)
                driver.get(my_url)
                driver.maximize_window()
                
                # Clicking on cookie accept option
                cookie_button=WebDriverWait(driver,20).until(
                            EC.element_to_be_clickable((By.XPATH,
                            "/html/body/div[8]/div[3]/div[1]/div[1]/div[2]/div/div/button")))
                cookie_button.click()
                sleep(5)
                
                # Clicking on the date button
                date_button = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH,
                            "/html/body/div[5]/section/div[8]/div[3]/div/div[2]/span")))
                
                date_button.click()
                
                # Sending the start date
                start_bar = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH,
                            "/html/body/div[7]/div[1]/input[1]")))
                            
                start_bar.clear()
                start_bar.send_keys(start)

                # Sending the end date
                end_bar = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH,
                            "/html/body/div[7]/div[1]/input[2]")))
                            
                end_bar.clear()
                end_bar.send_keys(end)
            
                # Clicking on the apply button
                apply_button = WebDriverWait(driver,20).until(
                        EC.element_to_be_clickable((By.XPATH,
                        "/html/body/div[7]/div[5]/a")))
                
                apply_button.click()
                sleep(5)
                
                # Getting the tables on the page and quiting
                dataframes = pd.read_html(driver.page_source)
                driver.quit()

                #Saving the needed table and export
                df=dataframes[0]
                #change your personal path
                df.to_csv(r'/Users/kikkosmac/Desktop/assignment_PDS/'+name+'.csv', index=False)
                frames.append(df)
                print(f'{asset} scraped.')
                break
    
            except:
                driver.quit()
                print(f'Failed to scrape {asset}. Trying again in 30 seconds.')
                sleep(30)
                continue
    return frames

#Parameters
assets=['funds/amundi-msci-wrld-ae-c','etfs/ishares-global-corporate-bond-$','etfs/db-x-trackers-ii-global-sovereign-5','etfs/spdr-gold-trust','indices/usdollar']
start='01/01/2020'
end='12/31/2020'

#run function
get_currencies(assets,start,end)


