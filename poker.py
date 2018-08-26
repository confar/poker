
maps = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    ranks = list(map(key, iterable))
    d1 = zip(iterable, ranks)
    return [k for k, v in d1 if v == max(ranks)]

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = [maps.get(r) if r.isalpha() else int(r) for r,s in cards]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    return len(set(s for r, s in hand)) == 1

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return ranks == list(range(max(ranks), min(ranks) - 1, -1))

def kind(n, ranks):
    """Return the first rank that this hand has exactly n-of-a-kind of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None


def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    filtered_pairs = []
    [filtered_pairs.append(r) for r in ranks if r not in filtered_pairs if ranks.count(r) == 2]
    if filtered_pairs:
        return tuple(filtered_pairs)
    return None

def test():
    "Test cases for the functions in poker program."
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "TD 9H TH 7C 9S".split()  # Two Pair
    tp1 = "JD 9H JH 7C 9S".split()  # Two Pair
    fkranks = card_ranks(fk)

    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert poker([sf1, sf2, fk, fh, tp]) == [sf1, sf2]
    assert poker([tp, tp1]) == [tp1]
    return 'tests pass'

test()