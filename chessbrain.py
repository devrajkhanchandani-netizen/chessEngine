import random

def findRandomMove(valid_moves):
    if len(valid_moves) == 0:
        return None
    return random.choice(valid_moves)