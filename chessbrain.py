import random

PIECE_SCORE = {"K": 0, "Q": 900, "R": 500, "B": 300, "N": 300, "P": 100}

def findBestMove(gs, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    orderMoves(valid_moves)
    findMoveAlphaBeta(gs, valid_moves, 4, -float('inf'), float('inf'), gs.whiteToMove)
    return next_move

def orderMoves(moves):
    def move_priority(move):
        score = 0
        if move.pieceCaptured != "--":
            score += PIECE_SCORE[move.pieceCaptured[1]] * 10 - PIECE_SCORE[move.pieceMoved[1]]
        if move.isPawnPromotion:
            score += 900
        if move.isCastleMove:
            score += 50
        return score
    moves.sort(key=move_priority, reverse=True)

def findMoveAlphaBeta(gs, valid_moves, depth, alpha, beta, white_to_move):
    global next_move
    if depth == 0 or len(valid_moves) == 0:
        return scoreBoard(gs)

    if white_to_move:
        max_score = -float('inf')
        for move in valid_moves:
            gs.makeMove(move)
            next_valid_moves = gs.getValidMoves()
            orderMoves(next_valid_moves)
            score = findMoveAlphaBeta(gs, next_valid_moves, depth - 1, alpha, beta, False)
            if score > max_score:
                max_score = score
                if depth == 4:
                    next_move = move
            gs.undoMove()
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return max_score

    else:
        min_score = float('inf')
        for move in valid_moves:
            gs.makeMove(move)
            next_valid_moves = gs.getValidMoves()
            orderMoves(next_valid_moves)
            score = findMoveAlphaBeta(gs, next_valid_moves, depth - 1, alpha, beta, True)
            if score < min_score:
                min_score = score
                if depth == 4:
                    next_move = move
            gs.undoMove()
            beta = min(beta, min_score)
            if alpha >= beta:
                break
        return min_score

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