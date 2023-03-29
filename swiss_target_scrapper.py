from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_csv(smiles):
    print("\n")
    print("+----------------------------------------+")
    print("|Swiss Target Prediction Scrapper Running|")
    print("+----------------------------------------+\n")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 1)

    driver.get("http://www.swisstargetprediction.ch/")

    element = wait.until(EC.visibility_of_element_located((By.ID, "smilesBox")))
    element.click()

    driver.find_element(By.ID, "smilesBox").send_keys(smiles)

    element = wait.until(EC.visibility_of_element_located((By.ID, "submitButton")))
    element.click()
    
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".buttons-csv > img")))
    element.click()
    time.sleep(5)

    print("\n")
    print("+--------------------------------+")
    print("|Swiss Target Prediction Finished|")
    print("+--------------------------------+\n")
