from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from flask import Flask, request
import os
from dotenv import load_dotenv
import requests
import threading

# Create the Flask app
app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
EVENTBRITE_API_TOKEN = os.getenv('EVENTBRITE_API_TOKEN')
HER_SAFE_JOURNEY = os.getenv('HER_SAFE_JOURNEY')

# Initialize the Telegram bot using Application.builder
application = Application.builder().token(HER_SAFE_JOURNEY).build()

# In-memory storage to keep track of events users are going to (using user chat ID)
attended_events = {}

### Flask Endpoints ###

@app.route('/')
def home():
    return 'Hello girlies! Welcome to Her Safe Journey! A Women Safe Event Finder Bot!'

# User feedback on attended concerts
@app.route('/feedback/<concert>')
def report_feedback(concert):
    return f"These are the concerts you have been to: {concert}. Please enter your rating for {concert} from 1 to 5."

# Rating of an event (simplified as an example)
@app.route('/rating/<event>')
def rating(event):
    return f"Here is the rating of {event}"

# List out events in a city using the Ticketmaster API
@app.route('/popular_events/<city>')
def get_ticketmaster_events(city):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    
    params = {
        'apikey': TICKETMASTER_API_KEY,  # API key from .env file
        'city': city  # City the user inputs
    }

    # Send a GET request to the Ticketmaster API
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return f"Error: Could not retrieve events for {city}. Please try again later."

    # Parse the response as JSON
    events_data = response.json()
    
    if '_embedded' in events_data:
        events = events_data['_embedded']['events']
        event_list = [f"{event['name']} on {event['dates']['start']['localDate']}" for event in events]
        return f"Events in {city}:\n" + '\n'.join(event_list)
    else:
        return f"No events found in {city}"

# Attended events tracker
@app.route('/attended_events/<attended>')
def attended_events(attended):
    return f"Showing events you have attended so far: {attended}"

# Subscribe to a city for updates on new events
@app.route('/subscribe/<city>')
def subscribe(city):
    return f"You just subscribed to {city} events. When new and exciting events are posted, we'll let you know!"

# Help user find other women attending the same event in the city
@app.route('/find_girlies/<city>/<event>')
def find_girlies(city, event):
    return f"So excited for {event}! Let's get you connected with some girlies in {city}."


### Telegram Bot Commands ###

# Telegram bot handler that gets events for a city
def bot_events(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide a city name. Usage: /events <city>")
        return
    
    city = context.args[0]
    url = f"http://localhost:5000/popular_events/{city}"
    response = requests.get(url)

    if response.status_code == 200:
        update.message.reply_text(response.text + "\n\nType '/going <event_name>' to add an event to your list of attended events.")
    else:
        update.message.reply_text(f"Could not retrieve events for {city}. Please try again.")

# Command to mark an event as "going"
def going_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide the event name. Usage: /going <event_name>")
        return
    
    event_name = ' '.join(context.args)  # In case the event name has multiple words
    user_id = update.message.chat_id  # Get the user's unique chat ID

    # Add the event to the user's attended events
    if user_id not in attended_events:
        attended_events[user_id] = []
    
    attended_events[user_id].append(event_name)
    update.message.reply_text(f"You've successfully added '{event_name}' to your attended events.")

# Command to get attended events
def attended_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id

    # Retrieve the events the user has marked as "going"
    if user_id in attended_events and attended_events[user_id]:
        attended = attended_events[user_id]
        update.message.reply_text(f"Here are the events you're going to:\n" + '\n'.join(attended))
    else:
        update.message.reply_text("You haven't added any events yet. Use '/going <event_name>' to add events.")

# Define the /start command for the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Her Safe Journey! Use /events <city> to get events in your city.')

# Set up the bot command handlers
def setup_bot_handlers():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("events", bot_events))
    application.add_handler(CommandHandler("going", going_command))
    application.add_handler(CommandHandler("attended", attended_command))

# Run the Flask app and the Telegram bot concurrently
def run_flask():
    app.run(debug=True, use_reloader=False)

def run_telegram_bot():
    setup_bot_handlers()
    application.run_polling()

# This automatically reloads the server when changes are made to the code
if __name__ == '__main__':
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start the Telegram bot
    run_telegram_bot()
