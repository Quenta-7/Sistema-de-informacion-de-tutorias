from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://localhost:5500/frontend/login.html")
time.sleep(2)

driver.quit()
