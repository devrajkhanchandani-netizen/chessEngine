import random

PIECE_SCORE = {"K": 0, "Q": 900, "R": 500, "B": 300, "N": 300, "P": 100}

def findBestMove(gs, valid_moves):
    best_move = None
    random.shuffle(valid_moves)
    
    if gs.whiteToMove:
        best_score = -float('inf')
        for move in valid_moves:
            gs.makeMove(move)
            score = bruteForceSearch(gs, 1)
            if score > best_score:
                best_score = score
                best_move = move
            gs.undoMove()
    else:
        best_score = float('inf')
        for move in valid_moves:
            gs.makeMove(move)
            score = bruteForceSearch(gs, 1)
            if score < best_score:
                best_score = score
                best_move = move
            gs.undoMove()
            
    return best_move

def bruteForceSearch(gs, depth_current):
    if depth_current == 2:
        return scoreBoard(gs)
        
    valid_moves = gs.getValidMoves()
    if len(valid_moves) == 0:
        return scoreBoard(gs)
        
    scores = []
    for move in valid_moves:
        gs.makeMove(move)
        score = bruteForceSearch(gs, depth_current + 1)
        scores.append(score)
        gs.undoMove()
        
    if gs.whiteToMove:
        return max(scores)
    else:
        return min(scores)

def scoreBoard(gs):
    score = 0
    for row in gs.board:
        for square in row:
            if square != "--":
                val = PIECE_SCORE[square[1]]
                if square[0] == 'w':
                    score += val
                else:
                    score -= val
    return score