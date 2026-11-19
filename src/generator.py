import random
from .cards import Spread, DrawnCard
def generate(pattern, deck):
    count = len(pattern['positions'])
    if count > len(deck):
        raise ValueError('недостаточно карт в колоде')

    rnd_card = random.sample(deck, count)
    result = Spread(pattern['name'])
    for i in range(len(pattern['positions'])):
        is_reversed = random.choice([True, False])
        result.add_card(DrawnCard(rnd_card[i], pattern['positions'][i], is_reversed))
    return result