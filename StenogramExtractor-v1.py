from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
import sys
import os
import re

month_dict = { "януари": 1, "февруари": 2,  "март": 3, "април": 4, "май": 5, "юни": 6,
               "юли": 7, "август": 8, "септември": 9, "октомври": 10, "ноември": 11, "декември": 12}  

def StenogramExtractorMain(yearToQuery):
    # Initiate Edge Webdriver and navigate to stenogram page
    driver = webdriver.Edge()
    driver.get('https://www.parliament.bg/bg/plenaryst')
    wait = WebDriverWait(driver, 15)

    if not os.path.exists(f"{yearToQuery}"):
        os.makedirs(f"{yearToQuery}")

    # Get available months for given year
    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), {yearToQuery})]")))
    monthLinks = GetAvailableMonths(driver, yearToQuery)

    # Itterate through all months and extract all stenograms
    for month in monthLinks:
        monthName = month.find_element(By.XPATH, ".//span").get_attribute("title")
        monthNum = month_dict[monthName]

        print("Month + MonthNum: ", monthName, monthNum)
        if not os.path.exists(f"{yearToQuery}/{monthNum}"):
            os.makedirs(f"{yearToQuery}/{monthNum}")

        month.click()

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), 'Стенограма от пленарно')]")))
            wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{monthName} {yearToQuery}')]")))
        except TimeoutException:
            print("Timed out, trying to find month link again...")
            monthLink = driver.find_element(By.XPATH, f"//span[contains(text(), {monthName})]")
            print("Found link with text: ", monthLink.text)
            monthLink.click()
            wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), 'Стенограма от пленарно')]")))
            wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{monthName} {yearToQuery}')]")))

        stenogramList = GetAllMonthStenograms(driver)

        filePath = f"{yearToQuery}/{monthNum}"
        for stenogram in stenogramList:
            print("Stenogram name: ", stenogram.text)
            try:
                stenogram.click()
                wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "mb-3"), "Открито"))
            except:
                print("Searching for stenogram: ", stenogram.text)
                stenogramLink = driver.find_element(By.XPATH, f"//a[contains(text(), '{stenogram.text}')]")
                print("Result found: ", stenogramLink.text)
                stenogramLink.click()
                wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "mb-3"), "Открито"))

            
            SaveStenogramText(driver, filePath)
            driver.back()


def SaveStenogramText(driver, filePath):
    """
    Parameters: web driver, file path; 
    Saves the current stenogram as a textfile (named steno-DD-MM-YYYY) under a given path
    """
    stenogramDateElement = driver.find_element(By.CLASS_NAME, "mb-3").text
    stenogramDatePattern = r"(\d{2})/(\d{2})/(\d{4})"
    stenogramDateMatch = re.search(stenogramDatePattern, stenogramDateElement)
    stenogramDate = f"{stenogramDateMatch[1]}-{stenogramDateMatch[2]}-{stenogramDateMatch[3]}"
    stenogramText = driver.find_element(By.CLASS_NAME, "mt-4")

    print(f"Saving stenogram under: {filePath}/steno-{stenogramDate}.txt")
    with open(f"{filePath}/steno-{stenogramDate}.txt", "w", encoding="utf-8") as wFile:
        wFile.write(stenogramText.get_attribute('innerHTML'))

def GetAllMonthStenograms(driver):
    """
    Parameters: web driver; 
    Returns an array of all stenograms for a month
    """
    stenogramLinks = driver.find_elements(By.XPATH, f"//a[contains(text(), 'Стенограма от пленарно')]")

    return stenogramLinks

def GetAvailableMonths(driver, year):
    """
    Parameters web driver and year; 
    Returns an array of month links
    """
    yearDiv = driver.find_element(By.XPATH, f"//div[contains(text(), {year})]")
    yearParent = yearDiv.find_element(By.XPATH, "..")
    availableMonths = yearParent.find_elements(By.XPATH, ".//li")

    return availableMonths

if __name__ == "__main__":
    yearToQuery = sys.argv[1] if len(sys.argv)>1 else datetime.now().year
    StenogramExtractorMain(yearToQuery)