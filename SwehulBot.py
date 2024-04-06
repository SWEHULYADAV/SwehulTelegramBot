#7092093044:AAHUQAq7bLReS4EQgQ9UerjcUtN5IzXfo9s
#be6a7a46efd3f9
#IPInfoToken___https://ipinfo.io/account/token


import os
import telebot
import datetime
import csv
import pytz
import requests  # Import the requests library for making HTTP requests

TOKEN = "7092093044:AAHUQAq7bLReS4EQgQ9UerjcUtN5IzXfo9s"
bot = telebot.TeleBot(TOKEN)
access_token = 'be6a7a46efd3f9'  # Get your IPInfo access token from https://ipinfo.io/account/token


# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Define the relative path for the log file
log_file = os.path.join(script_dir, 'bot_logs.csv')

# Field names for CSV file
fieldnames = ['Timestamp', 'User ID', 'User Name', 'Location', 'Question', 'Reply']

# Function to create log file and write headers if it doesn't exist
def initialize_log_file():
    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

# Function to log entries to CSV file
def log_to_csv(log_entry):
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(log_entry)


# Initialize log file (create if it doesn't exist)
initialize_log_file()

# Command handlers
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    location = get_user_location()
    log_entry = {'Timestamp': datetime.datetime.now(pytz.timezone(location['timezone'])).strftime("%Y-%m-%d %H:%M:%S %Z"),
                 'User ID': user_id,
                 'User Name': user_name,
                 'Location': location['city'] + ', ' + location['region'] + ', ' + location['country'],
                 'Question': '/start',
                 'Reply': "Welcome to Swehul Tech Dost!"}
    log_to_csv(log_entry)
    bot.reply_to(message, "Welcome to Swehul Tech Dost!")

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    location = get_user_location()
    log_entry = {'Timestamp': datetime.datetime.now(pytz.timezone(location['timezone'])).strftime("%Y-%m-%d %H:%M:%S %Z"),
                 'User ID': user_id,
                 'User Name': user_name,
                 'Location': location['city'] + ', ' + location['region'] + ', ' + location['country'],
                 'Question': '/help',
                 'Reply': "Showing available commands"}
    log_to_csv(log_entry)
    bot.reply_to(message, "Available commands:\n/start - Greeting\n/help - Show available commands\n/calculate <expression> - Evaluate a mathematical expression")

@bot.message_handler(commands=['calculate'])
def calculate(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    location = get_user_location()
    try:
        expression = message.text.split(maxsplit=1)[1].strip()
        result = eval(expression)
        reply_msg = f"Result: {result}"
    except Exception as e:
        reply_msg = "Error: Invalid expression or operation"
    log_entry = {'Timestamp': datetime.datetime.now(pytz.timezone(location['timezone'])).strftime("%Y-%m-%d %H:%M:%S %Z"),
                 'User ID': user_id,
                 'User Name': user_name,
                 'Location': location['city'] + ', ' + location['region'] + ', ' + location['country'],
                 'Question': f'/calculate {expression}',
                 'Reply': reply_msg}
    log_to_csv(log_entry)
    bot.reply_to(message, reply_msg)

@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    user_id = message.new_chat_members[0].id
    user_name = message.new_chat_members[0].first_name
    location = get_user_location()
    log_entry = {'Timestamp': datetime.datetime.now(pytz.timezone(location['timezone'])).strftime("%Y-%m-%d %H:%M:%S %Z"),
                 'User ID': user_id,
                 'User Name': user_name,
                 'Location': location['city'] + ', ' + location['region'] + ', ' + location['country'],
                 'Question': 'New user joined',
                 'Reply': f"Hello {user_name}! Welcome to the chat."}
    log_to_csv(log_entry)
    for new_member in message.new_chat_members:
        bot.reply_to(message, f"Hello {new_member.first_name}! Welcome to the chat.")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    location = get_user_location()
    log_entry = {'Timestamp': datetime.datetime.now(pytz.timezone(location['timezone'])).strftime("%Y-%m-%d %H:%M:%S %Z"),
                 'User ID': user_id,
                 'User Name': user_name,
                 'Location': location['city'] + ', ' + location['region'] + ', ' + location['country'],
                 'Question': message.text,
                 'Reply': "Your reply here"}
    log_to_csv(log_entry)
    bot.reply_to(message, "Your reply here")

# Helper function to get user location (timezone and approximate location)
def get_user_location():
    response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={access_token}").json()
    if 'timezone' in response:
        return {
            'timezone': response['timezone'],
            'city': response['city'],
            'region': response['region'],
            'country': response['country_name']
        }
    else:
        print("Error: Unable to fetch timezone data from API")
        return {
            'timezone': 'UTC',  # Default to UTC timezone
            'city': 'Unknown',
            'region': 'Unknown',
            'country': 'Unknown'
        }
        

# Start the bot
bot.polling()
