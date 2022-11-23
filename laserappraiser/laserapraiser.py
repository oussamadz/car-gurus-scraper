#!/usr/bin/python3
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

URL = "https://laserappraiser.com/login"
USERNAME = "jbachynski2"
PASSWORD = "ytkauto"
DATA = pd.read_csv("result.csv")

options = Options()
options.add_argument("start-maximized")
options.add_argument("--headless")

with open('progress', 'r') as f:
    PROGRESS = f.readline()

def save_data(line):
    with open("apraisal_data.csv", 'a') as f:
        f.write(line + '\n')

def save_progress(progress):
    with open("progress", 'w') as f:
        f.write(str(progress))

def convert(val):
    js = float(val)
    return js*1.30


#br = webdriver.Firefox(options=options)
br = webdriver.Firefox(options=options)
br.get(URL) 
br.find_element(By.ID, "username").send_keys(USERNAME)
br.find_element(By.ID, "password").send_keys(PASSWORD)
br.find_element(By.ID, "submit_btn").click()
WebDriverWait(br, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[3]/img")))
br.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[3]/img").click()

for index, row in DATA.iterrows():
    if index <= int(PROGRESS):
        continue
    vin = row['vin']
    trim = row['trim']
    if "N/A" in vin:
        continue
    if str(trim) == 'nan':
        continue
    print(f"index: {index} | vin: {row['vin']}")
    mileage = row['mileage']
    if str(mileage) == 'nan':
        continue
    print("clicked")
    WebDriverWait(br, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "vl-table")))
    #br.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[3]/ul/li[4]/a/span").click()
    br.execute_script("showNewAppraisalWizard({},true);")
    WebDriverWait(br, 30).until(EC.presence_of_element_located((By.ID, "newAppraisalVin")))
    br.find_element(By.ID, "newAppraisalVin").send_keys(vin)
    br.find_element(By.ID, "newAppraisalOdometer").send_keys(str(mileage))
    br.find_element(By.ID, "newAppraisalSubmit").click()
    try:
        WebDriverWait(br, 60).until(EC.presence_of_element_located((By.ID, "vin")))
    except:
        try:
            WebDriverWait(br, 60).until(EC.presence_of_element_located((By.ID, "vin")))
        except:
            continue
    try:
        select = Select(br.find_element(By.ID, "trim_select"))
        select_options = select.options
        for opt in select_options:
            if opt.text == "Please Select":
                continue
            else:
                select.select_by_visible_text(opt.text)
                #WebDriverWait(br, 15).until(EC.presence_of_element_located((By.ID, "newAppraisalVin")))
                time.sleep(1)
                WebDriverWait(br, 30).until(EC.presence_of_element_located((By.ID, "sum_bookPrice_table")))
                time.sleep(1)
                table = br.find_element(By.ID, "sum_bookPrice_table")
                trs = table.find_elements(By.TAG_NAME, "tr")
                RM = 0
                JDP = 0
                MMR = 0
                KBB = 0
                for tr in trs:
                    if "Retail Market" in tr.text:
                        RM = tr.find_elements(By.TAG_NAME, "td")[1].text
                    elif "KBB" in tr.text:
                        KBB = tr.find_elements(By.TAG_NAME, "td")[1].text
                    elif "J. D. Power" in tr.text:
                        JDP = tr.find_elements(By.TAG_NAME, "td")[1].text
                    elif "MMR" in tr.text:
                        MMR = tr.find_elements(By.TAG_NAME, "td")[1].text
                RM = convert(RM)
                JDP = convert(JDP)
                MMR = convert(MMR)
                KBB = convert(KBB)
                print("first worked")
                save_data(f"{vin},{mileage},{opt.text},{RM},{JDP},{MMR},{KBB}")
    except:
        try:
            trim = br.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div/div/form/fieldset[1]/p[7]/input").get_attribute("value")
            table = br.find_element(By.ID, "sum_bookPrice_table")
            trs = table.find_elements(By.TAG_NAME, "tr")
            RM = 0
            JDP = 0
            MMR = 0
            KBB = 0
            for tr in trs:
                if "Retail Market" in tr.text:
                    RM = tr.find_elements(By.TAG_NAME, "td")[1].text
                elif "KBB" in tr.text:
                    KBB = tr.find_elements(By.TAG_NAME, "td")[1].text
                elif "J. D. Power" in tr.text:
                    JDP = tr.find_elements(By.TAG_NAME, "td")[1].text
                elif "MMR" in tr.text:
                    MMR = tr.find_elements(By.TAG_NAME, "td")[1].text
            RM = convert(RM)
            JDP = convert(JDP)
            MMR = convert(MMR)
            KBB = convert(KBB)
            save_data(f"{vin},{mileage},{trim},{RM},{JDP},{MMR},{KBB}")
            print("second worked")
        except NoSuchElementException:
            print("trim not found")
        except Exception as e:
            print(f"error: {e}")
    save_progress(index)
    br.get("https://mvs.laserappraiserservices.com/mvs/vehicleList")
    #br.find_element(By.XPATH, "/html/body/nav/div[2]/div/div[2]/a[1]").click()
