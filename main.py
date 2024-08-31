import os
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdfkit
import shutil
from bs4 import BeautifulSoup


def downloadFile(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)


browser = webdriver.Firefox()
# change the url to the one that you need to download
browser.get('https://www.ncsl.org/technology-and-communication/broadband-2022-legislation')
browser.maximize_window()
time.sleep(3)
# change the directory name to the required one
dir_name = "Broadband 2022 Legislation"
if os.path.exists(dir_name):
    shutil.rmtree(dir_name)
else:
    os.mkdir(dir_name)
wrapper = browser.find_element(By.CLASS_NAME, "table-wrapper")
table = browser.find_element(By.TAG_NAME, "table")
table_rows = table.find_elements(By.TAG_NAME, "tr")
for ele in table_rows:
    row_elements = ele.find_elements(By.TAG_NAME, "td")
    if row_elements:
        state = row_elements[0].get_attribute("innerHTML")
        hrefs = row_elements[1].get_attribute('innerHTML')
        if "href" in hrefs:
            # links = re.findall(r'href=[\'"]?([^\'" >]+)', hrefs)
            bf_hrefs = BeautifulSoup(hrefs, "html.parser")
            links = bf_hrefs.find_all("a")
            # bill_state = re.findall(r'<p(\s.*?)?>(.*?)</p>', state)[0][-1].replace("&nbsp;", '')
            bf_state = bf = BeautifulSoup(state, "html.parser")
            bill_state = bf_state.text.strip()
            for i in range(len(links)):
                # bill_number = re.findall(r'<a(\s.*?)?>(.*?)</a>', hrefs)[i][-1]
                bill_number = links[i].text
                link = links[i]['href']
                try:
                    if "pdf" in link.lower():
                        downloadFile(link, f"{dir_name}/{bill_state}_{bill_number}.pdf")
                    else:
                        pdfkit.from_url(link, f"{dir_name}/{bill_state}_{bill_number}.pdf")
                        print(f"Successfully Downloaded {bill_state}_{bill_number}")
                except OSError as e:
                    print(e, f"Need to be downloaded manually {bill_state}_{bill_number} : {link}")

browser.quit()
