from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Edge()
driver.get('https://www.parliament.bg/bg/plenaryst')
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '2023')]")))

yearDiv = driver.find_element(By.XPATH, f"//div[contains(text(), '2023')]")
yearParent = yearDiv.find_element(By.XPATH, "..")

january = yearParent.find_element(By.XPATH, ".//li/span[contains(text(), 'януари')]")
january.click()
wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), 'януари 2023')]")))

february = yearParent.find_element(By.XPATH, ".//li/span[contains(text(), 'февруари')]")
february.click()
wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), 'февруари 2023')]")))

april = yearParent.find_element(By.XPATH, ".//li/span[contains(text(), 'април')]")
april.click()
wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), 'април 2023')]")))

time.sleep(10)