from flask import Flask # builds backend and helps you create routes (URLs) that users call
import os # helps us interact with environment variables
from dotenv import load_dotenv # loads environment variables from .env file
import requests # package allows HTTP requests to external APIs

# the app is created here:
app = Flask(__name__)

# loads environemnt variables from the .env file
load_dotenv()

TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
EVENTBRITE_API_TOKEN = os.getenv('EVENTBRITE_API_TOKEN')
HER_SAFE_JOURNEY = os.getenv('HER_SAFE_JOURNEY')

@app.route('/')
def home():
	return 'Hello girlies! Welcome to Her Safe Journey! A Women Safe Event Finder Bot!'

# user feedback
@app.route('/feedback/<concert>')
def report_feedback(concert):
	return f"These are the concerts you have been to: {concert}. Enter in your rating for {concert} from 1 - 5"
	
@app.route('/rating')
def rating(event):
		return f"Here is the rating of {event}"

@app.route('/popular_events/<city>')
def popular_events(city):
	return f"Here is the list of the popular events in {city}"

@app.route('/attended_events')
def attended_events(attended):
    return f"Showing events you have attended so far: {attended}"

@app.route('/subscribe/<city>')
def subscribe(city):
	return f"You just subscribed to {city} events. When new and exciting events are posted we'll let you know!"

@app.route('/find_girlies/<city>/<event>')
def find_girlies(city, event):
	return f"So excited for {event}! Let's get you connected with some girlies in {city}."

# this automatically reloads the server when 
# changes are made to the code
if __name__ == '__main__':
	app.run(debug=True)

# rebecca's initial commit 

	