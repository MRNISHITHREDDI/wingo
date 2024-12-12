from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Load settings
with open('settings.json') as f:
    settings = json.load(f)

# Setup Selenium WebDriver
driver = webdriver.Chrome(settings['chrome_driver_path'])
driver.get("https://tc9987.win/")

# Login
driver.find_element(By.ID, "username").send_keys(settings['username'])
driver.find_element(By.ID, "password").send_keys(settings['password'])
driver.find_element(By.ID, "login-button").click()

time.sleep(5)  # Wait for login to complete

# Fetch Current Period ID
def get_current_period_id():
    # Navigate to the Wingo game page
    driver.find_element(By.ID, "wingo-game").click()
    time.sleep(2)  # Allow the page to load
    
    # Find the current Period ID (update selector based on website structure)
    period_id_element = driver.find_element(By.CLASS_NAME, "period-id-class")  # Replace 'period-id-class' with the correct class
    period_id = period_id_element.text
    return period_id

# Example usage
period_id = get_current_period_id()
print(f"Current Period ID: {period_id}")

# You can now use this Period ID in your predictions
