from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import json
import time

# Load credentials
with open('credentials.json') as f:
    credentials = json.load(f)

# Selenium WebDriver setup
driver = webdriver.Chrome('path/to/chromedriver')  # Update with your ChromeDriver path

# Fetch Current Period ID
def get_current_period_id():
    driver.get("https://tc9987.win/")
    driver.find_element(By.ID, "username").send_keys(credentials["username"])
    driver.find_element(By.ID, "password").send_keys(credentials["password"])
    driver.find_element(By.ID, "login-button").click()
    time.sleep(5)  # Wait for login to complete

    driver.find_element(By.ID, "wingo-game").click()
    time.sleep(2)  # Allow page to load

    period_id_element = driver.find_element(By.CLASS_NAME, "period-id-class")  # Replace with actual selector
    return period_id_element.text

# Generate prediction
def generate_prediction():
    return random.choice(["GREEN", "RED"])

# Track wins and losses
loss_streak = 0

# Start predictions
def start(update: Update, context: CallbackContext):
    global loss_streak
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hello {user.first_name}, starting Wingo predictions with skip logic...")

    while True:
        try:
            # Check if we need to skip 2 minutes due to losses
            if loss_streak >= 3:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="3 losses in a row detected. Skipping 2 minutes...")
                time.sleep(120)  # Skip 2 minutes
                loss_streak = 0  # Reset loss streak after skip

            # Fetch the current Period ID
            period_id = get_current_period_id()

            # Generate a prediction
            prediction = generate_prediction()
            message = f"""TC LOTTERY 1 MINUTE WINGO

PERIOD ID: {period_id}
PREDICTION: {prediction}

MAINTAIN FUND UPTO LEVEL 8"""
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)

            # Simulate the game result (for example purposes; replace with actual result checking logic)
            game_result = random.choice(["WIN", "LOSS"])
            if game_result == "LOSS":
                loss_streak += 1
            else:
                loss_streak = 0  # Reset streak on a win

            # Notify result
            result_message = f"PERIOD ID: {period_id}\nRESULT: {game_result} 🎉🎉🎉" if game_result == "WIN" else f"PERIOD ID: {period_id}\nRESULT: LOSS 😔"
            context.bot.send_message(chat_id=update.effective_chat.id, text=result_message)

            # Wait 1 minute before the next prediction
            time.sleep(60)

        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Error occurred: {e}")
            break  # Stop the loop in case of a critical error

# Main function
def main():
    TOKEN = credentials['telegram_bot_token']
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
