from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time 
# Set up WebDriver using ChromeDriverManager to automatically manage the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open your fitness tracker app
driver.get("http://localhost:3000")  # Or your app's URL

# Example Test: Check if the login page loads
assert "" in driver.title

# Find the username and password fields and interact with them
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")

username_field.send_keys("testuser")
password_field.send_keys("securepassword")

# Find the login button and interact with it
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
time.sleep(10)
login_button.click()

# Wait for the page to load (optional)
time.sleep(10)  # Wait for up to 10 seconds

# Verify if you are on the correct page

# Close the browser once the test is done
driver.quit()
