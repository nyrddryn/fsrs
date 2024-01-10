from fsrs import *
from datetime import datetime


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

test_repeat()