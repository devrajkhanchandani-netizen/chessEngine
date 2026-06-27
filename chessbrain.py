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

def findMoveAlphaBeta(gs, moves, depth, alpha, beta, white_to_move):
    global next_move
    if depth == 0 or len(moves) == 0:
        return scoreBoard(gs)

    if white_to_move:
        max_score = -float('inf')
        legal_move_count = 0
        for move in moves:
            gs.makeMove(move)
            gs.whiteToMove = not gs.whiteToMove
            if gs.inCheck():
                gs.whiteToMove = not gs.whiteToMove
                gs.undoMove()
                continue
            gs.whiteToMove = not gs.whiteToMove
            legal_move_count += 1
            
            next_moves = gs.getAllPossibleMoves(include_castle=True)
            orderMoves(next_moves)
            score = findMoveAlphaBeta(gs, next_moves, depth - 1, alpha, beta, False)
            gs.undoMove()
            
            if score > max_score:
                max_score = score
                if depth == 4:
                    next_move = move
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        if legal_move_count == 0:
            if gs.inCheck():
                return -100000 + (4 - depth)
            return 0
        return max_score

    else:
        min_score = float('inf')
        legal_move_count = 0
        for move in moves:
            gs.makeMove(move)
            gs.whiteToMove = not gs.whiteToMove
            if gs.inCheck():
                gs.whiteToMove = not gs.whiteToMove
                gs.undoMove()
                continue
            gs.whiteToMove = not gs.whiteToMove
            legal_move_count += 1
            
            next_moves = gs.getAllPossibleMoves(include_castle=True)
            orderMoves(next_moves)
            score = findMoveAlphaBeta(gs, next_moves, depth - 1, alpha, beta, True)
            gs.undoMove()
            
            if score < min_score:
                min_score = score
                if depth == 4:
                    next_move = move
            beta = min(beta, min_score)
            if alpha >= beta:
                break
        if legal_move_count == 0:
            if gs.inCheck():
                return 100000 - (4 - depth)
            return 0
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