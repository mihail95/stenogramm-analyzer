from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import sys
import os
import re

month_dict = { "януари": 1, "февруари": 2,  "март": 3, "април": 4, "май": 5, "юни": 6,
               "юли": 7, "август": 8, "септември": 9, "октомври": 10, "ноември": 11, "декември": 12}  

def StenogramExtractorMain(yearToQuery, monthToQuery):
    driver = webdriver.Edge()
    driver.get('https://www.parliament.bg/bg/plenaryst')
    wait = WebDriverWait(driver, 30)

    if not os.path.exists(f"{yearToQuery}"):
        os.makedirs(f"{yearToQuery}")

    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), {yearToQuery})]")))

    for month in month_dict.keys():
        monthNum = month_dict[month]
        if (monthNum >= int(monthToQuery)):
            monthLink = GetMonthLink(driver, yearToQuery, month)
            
            if monthLink != None:
                print("Month + MonthNum: ", month, monthNum)
                print("Month link text ", monthLink.text)
                if not os.path.exists(f"{yearToQuery}/{monthNum}"):
                    os.makedirs(f"{yearToQuery}/{monthNum}")
                wait.until(EC.element_to_be_clickable(monthLink)).click()
            else: continue

            for date in range(1, 32):
                wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{month} {yearToQuery}')]")))
                wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '/{monthNum:02}/{yearToQuery}')]")))
                
                filePath = f"{yearToQuery}/{monthNum}"
                stenogramLink = GetStenogramLink(driver, yearToQuery, monthNum, date)
                if stenogramLink != None:
                    wait.until(EC.element_to_be_clickable(stenogramLink)).click()
                    wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "mb-3"), f'{date:02}/{monthNum:02}/{yearToQuery}'))
                    SaveStenogramText(driver, filePath)
                    driver.back()
                else: continue


def GetStenogramLink(driver, yearToQuery, monthNum, date):
    """
    Parameters array of stenogram links and  year, month number, and date to find; 
    Returns the stenogram link
    """
    try:
        stenogramLink = driver.find_element(By.XPATH, f"//a[contains(text(), '{date:02}/{monthNum:02}/{yearToQuery}')]")
    except:
        stenogramLink = None

    return stenogramLink

def GetMonthLink(driver, yearToQuery, month):
    """
    Parameters array of month links and month name to find; 
    Returns the month link
    """

    try:
        yearDiv = driver.find_element(By.XPATH, f"//div[contains(text(), {yearToQuery})]")
        yearParent = yearDiv.find_element(By.XPATH, "..")
        availableMonth = yearParent.find_element(By.XPATH, f".//li/span[contains(text(), '{month}')]")
    except:
        availableMonth = None

    return availableMonth

def SaveStenogramText(driver, filePath):
    """
    Parameters: web driver, file path; 
    Saves the current stenogram as a textfile (named steno-DD-MM-YYYY) under a given path
    """
    stenogramDateElement = driver.find_element(By.CLASS_NAME, "mb-3").text
    stenogramDatePattern = r"(\d{2})/(\d{2})/(\d{4})"
    stenogramDateMatch = re.search(stenogramDatePattern, stenogramDateElement)
    if stenogramDateMatch:
        stenogramDate = f"{stenogramDateMatch[1]}-{stenogramDateMatch[2]}-{stenogramDateMatch[3]}"
        stenogramText = driver.find_element(By.CLASS_NAME, "mt-4")

        print(f"Saving stenogram under: {filePath}/steno-{stenogramDate}.txt")
        with open(f"{filePath}/steno-{stenogramDate}.txt", "w", encoding="utf-8") as wFile:
            wFile.write(stenogramText.get_attribute('innerHTML'))

if __name__ == "__main__":
    # Usage: python .\StenogramExtractor.py yearToQuery monthToQuery - year parameter defaults to datetime.now(), month defaults to January
    # example: python .\StenogramExtractor.py 2024 5
    yearToQuery = sys.argv[1] if len(sys.argv)>1 else datetime.now().year
    monthToQuery = sys.argv[2] if len(sys.argv)>2 else 1
    StenogramExtractorMain(yearToQuery, monthToQuery)