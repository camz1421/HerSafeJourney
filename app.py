from flask import Flask
import requests

# the app is created here:
app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello girlies! Welcome to Her Safe Journey! A Women Safe Event Finder Bot!'

# user feedback
@app.route('/feedback/<concert>')
def report_feedback(concert):
	return f"These are the concerts you have been to: {concert}. Enter in your rating for {concert} from 1 - 5"
	
@app.route('/popular_events/<city>')
def popular_events(city):
	return f"Here is the list of the popular events in {city}"

@app.route('/events/<city>')
def get_events(city):
    return f"Showing events for {city}"

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

	