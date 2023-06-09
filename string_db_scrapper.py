import time
import shutil
import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

def get_ppi_network(name_list):
    print("\n")
    print("+--------------------------+")
    print("|String DB Scrapper Running|")
    print("+--------------------------+\n")
    driver = webdriver.Chrome()
    vars = {}

    wait = WebDriverWait(driver, 20)

    driver.get("https://string-db.org/")
    driver.find_element(By.CSS_SELECTOR, ".header_div > a").click()
    driver.find_element(By.ID, "multiple_identifiers").click()
    driver.find_element(By.ID, "primary_input:multiple_identifiers").click()
    for names in name_list:
        driver.find_element(By.ID, "primary_input:multiple_identifiers").send_keys(names)
        driver.find_element(By.ID, "primary_input:multiple_identifiers").send_keys(Keys.RETURN)
    driver.find_element(By.CSS_SELECTOR, "#organism_text_input_multiple_identifiers .organism_drop").click()
    dropdown = driver.find_element(By.ID, "speciesList_multiple_identifiers")

    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//option[. = 'Homo sapiens']")))
    dropdown.find_element(By.XPATH, "//option[. = 'Homo sapiens']").click()

    driver.find_element(By.CSS_SELECTOR, "#speciesList_multiple_identifiers > option:nth-child(2)").click()
    driver.find_element(By.CSS_SELECTOR, "#speciesFloatingDiv_multiple_identifiers .minibutton").click()
    driver.find_element(By.CSS_SELECTOR, "#input_form_multiple_identifiers .button").click()

    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".button:nth-child(10)")))
    driver.find_element(By.CSS_SELECTOR, ".button:nth-child(10)").click()

    element = wait.until(EC.visibility_of_element_located((By.ID, "bottom_page_selector_cluster")))
    driver.find_element(By.ID, "bottom_page_selector_cluster").click()

    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(2) > .view_settings_checkbox_wrap:nth-child(1) > label")))
    driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(2) > .view_settings_checkbox_wrap:nth-child(1) > label").click()

    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".box_body > div .button")))
    driver.find_element(By.CSS_SELECTOR, ".box_body > div .button").click()

    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#bottom_page_selector_cluster_container .settings_box_wrap")))
    driver.find_element(By.CSS_SELECTOR, "#bottom_page_selector_cluster_container .settings_box_wrap").click()

    ppi_url = driver.current_url
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S_string.txt")
    new_dir_path = os.path.join(os.getcwd(), date_time_str)
    with open(new_dir_path, 'a') as file:
        file.write(f"Visit this URL for viewing your ppi network: {ppi_url}")

    element_cluster_1 = driver.find_element(By.CSS_SELECTOR, ".clustering_table_row:nth-child(2) > .ct_cluster_protnames")
    list1 = element_cluster_1.text.split(",")

    element_cluster_2 = driver.find_element(By.CSS_SELECTOR, ".clustering_table_row:nth-child(4) > .ct_cluster_protnames")
    list2 = element_cluster_2.text.split(",")

    element_cluster_3 = driver.find_element(By.CSS_SELECTOR, ".clustering_table_row:nth-child(6) > .ct_cluster_protnames")
    list3 = element_cluster_3.text.split(",")

    element = wait.until(EC.visibility_of_element_located((By.ID, "bottom_page_selector_table")))
    driver.find_element(By.ID, "bottom_page_selector_table").click()

    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".row:nth-child(5) .updateNonce")))
    driver.find_element(By.CSS_SELECTOR, ".row:nth-child(5) .updateNonce").click()

    time.sleep(5)
    driver.quit()

    print("+---------------------------+")
    print("|String DB Scrapper Finished|")
    print("+---------------------------+\n")


    print("Moving string_interactions.tsv to root directory....")
    home_dir = os.path.expanduser("~")
    file_path = f"{home_dir}\\Downloads\\string_interactions.tsv"
    shutil.move(file_path, f"{os.getcwd()}\\string_interactions.tsv")

    print("Scanning string_interactions.tsv....")
    df = pd.read_csv('string_interactions.tsv', sep='\t')

    names = df['#node1'].tolist()

    counts_list1 = {}
    genes_list = []

    print("Finding Gene Name with most interaction in cluster 1....")
    for elem in list1:
        count = names.count(elem)
        counts_list1[elem] = count

    max_key = max(counts_list1, key=counts_list1.get)
    genes_list.append(max_key)

    counts_list2 = {}

    print("Finding Gene Name with most interaction in cluster 2....")
    for elem in list2:
        count = names.count(elem)
        counts_list2[elem] = count

    max_key = max(counts_list2, key=counts_list2.get)
    genes_list.append(max_key)

    counts_list3 = {}

    print("Finding Gene Name with most interaction in cluster 3....")
    for elem in list3:
        count = names.count(elem)
        counts_list3[elem] = count

    max_key = max(counts_list3, key=counts_list3.get)
    genes_list.append(max_key)
    
    print(f"Top 3 genes are: {genes_list}")

    return genes_list
