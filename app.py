from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

# Telegram Bot credentials
TELEGRAM_BOT_TOKEN = '7692840933:AAH2VczNvfH68Q_NgSLXzcIloHYITeSqY8A'
TELEGRAM_CHAT_ID = '-4776470301'  # Use correct ID from getUpdates response

# List of URLs to check
URLS = [
    'https://visaslots.info/details/46',
    'https://visaslots.info/details/47'
]

# Function to send Telegram alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Telegram message sent successfully!")
        else:
            print(f"❌ Failed to send message. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❗ Error sending message: {e}")


def get_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        slots_element = driver.find_element(By.XPATH, "/html/body/main/details[1]/figure/table/tbody/tr/td[1]")
        visa_type_element = driver.find_element(By.XPATH, "/html/body/main/details[1]/figure/table/tbody/tr/td[3]")
        month_element = driver.find_element(By.XPATH, "/html/body/main/details[1]/figure/table/tbody/tr/td[4]")
        date_element = driver.find_element(By.XPATH, "/html/body/main/details[1]/figure/table/tbody/tr/td[5]")
        location_element = driver.find_element(By.XPATH, "/html/body/main/details[1]/figure/table/tbody/tr/td[2]")

        slots = slots_element.text.strip()
        visa_type = visa_type_element.text.strip()
        month_val = month_element.text.strip()
        date_val = date_element.text.strip()
        location_val = location_element.text.strip()

        print(f"[{url}] Visa Type: {visa_type}, Location: {location_val}, Slots: {slots}, Month: {month_val}, Dates: {date_val}")

        if int(slots) == 0:
            send_telegram_alert(
                f"🟢 {location_val} - {slots} slots available for {visa_type} in {month_val} on {date_val}"
            )
            
    except Exception as e:
        print(f"❌ [{url}] Failed to retrieve data. Error: {e}")
    finally:
        driver.quit()

# Main logic
def main():
    for url in URLS:
        get_data(url)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(30)  # Check every 5 minutes
