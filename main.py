from fsrs import *
from datetime import datetime
import json

def print_scheduling_cards(scheduling_cards, target_rating):
    rating_mapping = {
        Rating.Again: "Again",
        Rating.Hard: "Hard",
        Rating.Good: "Good",
        Rating.Easy: "Easy",
    }

    target_rating_str = rating_mapping.get(target_rating, "Unknown Rating")

    if target_rating in scheduling_cards:
        print(f"{target_rating_str}.card:", scheduling_cards[target_rating].card.__dict__)
        print()
        print(f"{target_rating_str}.review_log:", scheduling_cards[target_rating].review_log.__dict__)
    else:
        print(f"No information available for {target_rating_str}")

    print()


def test_repeat():
    f = FSRS()
    f.p.w = (1.14, 1.01, 5.44, 14.67, 5.3024, 1.5662, 1.2503, 0.0028, 1.5489, 0.1763, 0.9953, 2.7473, 0.0179, 0.3105, 0.3976, 0.0, 2.0902)
    card = Card("kanji")
    now = datetime.now()
    scheduling_cards = f.repeat(card, now)

    print_scheduling_cards(scheduling_cards, target_rating=Rating.Good)

    ratings = (Rating.Good, Rating.Good, Rating.Good, Rating.Good, Rating.Good, Rating.Good, Rating.Again, Rating.Again, Rating.Good, Rating.Good, Rating.Good, Rating.Good, Rating.Good)
    ivl_history = []

    for rating in ratings:
        card = scheduling_cards[rating].card
        ivl = card.scheduled_days
        ivl_history.append(ivl)
        now = card.due
        scheduling_cards = f.repeat(card, now)
        print_scheduling_cards(scheduling_cards, target_rating=rating)

    print(ivl_history)
    assert ivl_history == [0, 5, 16, 43, 106, 236, 0, 0, 12, 25, 47, 85, 147]

# test_repeat()

def test_2():
    with open('test.json', 'r') as file:
        data = json.load(file)
    # Truy cập và lấy dữ liệu từ dict
    log_card_data = data.get('log_card', {})
    log_card_id = log_card_data.get('id', '')
    stability = float(log_card_data.get('stability', 0))
    difficulty = float(log_card_data.get('difficulty', 0))
    reps = int(log_card_data.get('reps', 0))
    state = int(log_card_data.get('state', 0))
    last_review_str = log_card_data.get('last_review', '')
    last_review = datetime.strptime(last_review_str, "datetime.datetime(%Y,%m,%d,%H,%M,%S,%f)")
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
    rating_time = datetime.strptime(rating_time_str, "datetime.datetime(%Y,%m,%d,%H,%M,%S,%f)")

    
    f = FSRS()
    now = rating_time
    scheduling_cards = f.repeat(card, now)

    ivl_history = []
    card = scheduling_cards[rating].card
    ivl = card.scheduled_days
    ivl_history.append(ivl)
    now = card.due
    scheduling_cards = f.repeat(card, now)
    print_scheduling_cards(scheduling_cards, target_rating=rating)

test_2()

