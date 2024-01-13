from flask import Flask, request, jsonify
from fsrs import *
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

def get_data_for_rating(json_data, target_rating):
    # Load JSON data
    data = json.loads(json_data)

    # Get scheduling_cards dictionary
    scheduling_cards = data.get('scheduling_cards', {})

    # Get data for the specified rating
    rating_data = scheduling_cards.get(str(int(target_rating)), None)

    if rating_data:
        card_info = rating_data.get('card', {})
        review_log_info = rating_data.get('review_log', {})

        # Print or use the extracted data as needed
        print("Card Info:")
        print(card_info)
        print("\nReview Log Info:")
        print(review_log_info)

        # Alternatively, you can return the extracted data
        return card_info
    else:
        print(f"No information available for rating {target_rating}")
        return None


def serialize_scheduling_cards(scheduling_cards):
    serialized_cards = {}
    for rating, scheduling_info in scheduling_cards.items():
        serialized_cards[rating] = {
            'card': scheduling_info.card.__dict__,
            'review_log': scheduling_info.review_log.__dict__
        }
    return serialized_cards

def serialize_to_json(scheduling_cards, ivl_history):
    serialized_cards = serialize_scheduling_cards(scheduling_cards)
    
    # Convert datetime objects to strings
    for rating_info in serialized_cards.values():
        rating_info['card']['due'] = rating_info['card']['due'].strftime("%Y-%m-%d %H:%M:%S.%f")
        rating_info['card']['last_review'] = rating_info['card']['last_review'].strftime("%Y-%m-%d %H:%M:%S.%f")
        rating_info['review_log']['review'] = rating_info['review_log']['review'].strftime("%Y-%m-%d %H:%M:%S.%f")
    
    data = {
        'scheduling_cards': serialized_cards,
        'ivl_history': ivl_history
    }
    return json.dumps(data)

@app.route('/schedule', methods=['POST'])
def schedule():
    
    data = request.get_json()
    log_card_data = data.get('log_card', {})
    log_card_id = log_card_data.get('id', '')
    stability = float(log_card_data.get('stability', 0))
    difficulty = float(log_card_data.get('difficulty', 0))
    reps = int(log_card_data.get('reps', 0))
    state = int(log_card_data.get('state', 0))
    last_review_str = log_card_data.get('last_review', '')
    last_review = datetime.strptime(last_review_str, "%Y-%m-%d %H:%M:%S.%f")
    card = Card(log_card_id,stability,difficulty,reps,state,last_review)
    rating_now_data = data.get('rating_now', {})
    rating = rating_now_data.get('rating', '')
    if rating == 'Again':
        rating = Rating.Again
    elif rating == 'Hard':
        rating = Rating.Hard
    elif rating == 'Good':
        rating = Rating.Good
    elif rating == 'Easy':
        rating = Rating.Easy
    rating_time_str = rating_now_data.get('rating_time', '')
    rating_time = datetime.strptime(rating_time_str, "%Y-%m-%d %H:%M:%S.%f")

    
    f = FSRS()
    now = rating_time
    scheduling_cards = f.repeat(card, now)
    card = scheduling_cards[rating].card
    ivl = card.scheduled_days
    json_data = serialize_to_json(scheduling_cards, ivl)
    filtered_json_data = get_data_for_rating(json_data, rating)
    filtered_json_data = json.dumps(filtered_json_data)
    return filtered_json_data

if __name__ == '__main__':
    app.run(debug=True)