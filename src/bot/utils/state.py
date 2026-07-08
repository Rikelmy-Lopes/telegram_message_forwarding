from itertools import count

_counter = count()

def new_state():
    return next(_counter)