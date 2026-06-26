class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.checkmate = False
        self.stalemate = False
        self.captured_by_white = []
        self.captured_by_black = []
        self.piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
        
        self.wK_moved = False
        self.wR_left_moved = False
        self.wR_right_moved = False
        self.bK_moved = False
        self.bR_left_moved = False
        self.bR_right_moved = False
        
        self.enpassantPossible = ()

    def makeMove(self, move, promo_choice='Q'):
        self.board[move.startRow][move.startCol] = "--"
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promo_choice
        elif move.isCastleMove:
            self.board[move.endRow][move.endCol] = move.pieceMoved
            if move.endCol == 6:
                self.board[move.endRow][5] = self.board[move.endRow][7]
                self.board[move.endRow][7] = "--"
            elif move.endCol == 2:
                self.board[move.endRow][3] = self.board[move.endRow][0]
                self.board[move.endRow][0] = "--"
        elif move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.board[move.startRow][move.endCol] = "--"
        else:
            self.board[move.endRow][move.endCol] = move.pieceMoved

        if move.pieceMoved == 'wK': self.wK_moved = True
        elif move.pieceMoved == 'bK': self.bK_moved = True
        elif move.pieceMoved == 'wR':
            if move.startRow == 7 and move.startCol == 0: self.wR_left_moved = True
            elif move.startRow == 7 and move.startCol == 7: self.wR_right_moved = True
        elif move.pieceMoved == 'bR':
            if move.startRow == 0 and move.startCol == 0: self.bR_left_moved = True
            elif move.startRow == 0 and move.startCol == 7: self.bR_right_moved = True

        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        self.moveLog.append(move)
        if move.pieceCaptured != "--":
            if move.pieceMoved[0] == 'w':
                self.captured_by_white.append(move.pieceCaptured)
            else:
                self.captured_by_black.append(move.pieceCaptured)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            
            if move.pieceCaptured != "--":
                if move.pieceMoved[0] == 'w':
                    self.captured_by_white.pop()
                else:
                    self.captured_by_black.pop()
            
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            
            self.wK_moved = False
            self.bK_moved = False
            self.wR_left_moved = False
            self.wR_right_moved = False
            self.bR_left_moved = False
            self.bR_right_moved = False
            
            for m in self.moveLog:
                if m.pieceMoved == 'wK': self.wK_moved = True
                elif m.pieceMoved == 'bK': self.bK_moved = True
                elif m.pieceMoved == 'wR':
                    if m.startRow == 7 and m.startCol == 0: self.wR_left_moved = True
                    elif m.startRow == 7 and m.startCol == 7: self.wR_right_moved = True
                elif m.pieceMoved == 'bR':
                    if m.startRow == 0 and m.startCol == 0: self.bR_left_moved = True
                    elif m.startRow == 0 and m.startCol == 7: self.bR_right_moved = True

            if len(self.moveLog) > 0:
                last_m = self.moveLog[-1]
                if last_m.pieceMoved[1] == 'P' and abs(last_m.startRow - last_m.endRow) == 2:
                    self.enpassantPossible = ((last_m.startRow + last_m.endRow) // 2, last_m.startCol)
                else:
                    self.enpassantPossible = ()
            else:
                self.enpassantPossible = ()

            if move.isCastleMove:
                if move.endCol == 6:
                    self.board[move.endRow][7] = self.board[move.endRow][5]
                    self.board[move.endRow][5] = "--"
                elif move.endCol == 2:
                    self.board[move.endRow][0] = self.board[move.endRow][3]
                    self.board[move.endRow][3] = "--"

            self.whiteToMove = not self.whiteToMove

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.wK_location()[0], self.wK_location()[1])
        else:
            return self.squareUnderAttack(self.bK_location()[0], self.bK_location()[1])

    def wK_location(self):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == "wK":
                    return (r, c)
        return (7, 4)

    def bK_location(self):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == "bK":
                    return (r, c)
        return (0, 4)

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        opp_moves = self.getAllPossibleMoves(include_castle=False)
        self.whiteToMove = not self.whiteToMove
        for move in opp_moves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getValidMoves(self):
        temp_ep = self.enpassantPossible
        moves = self.getAllPossibleMoves(include_castle=True)
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            self.enpassantPossible = temp_ep
        return moves

    def getAllPossibleMoves(self, include_castle=True):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves, include_castle)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r-1 >= 0:
                if self.board[r-1][c] == "--":
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r, c), (r-2, c), self.board))
                if c-1 >= 0:
                    if self.board[r-1][c-1][0] == 'b':
                        moves.append(Move((r, c), (r-1, c-1), self.board))
                    elif (r-1, c-1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r-1, c-1), self.board, is_ep=True))
                if c+1 < 8:
                    if self.board[r-1][c+1][0] == 'b':
                        moves.append(Move((r, c), (r-1, c+1), self.board))
                    elif (r-1, c+1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r-1, c+1), self.board, is_ep=True))
        else:
            if r+1 < 8:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r, c), (r+2, c), self.board))
                if c-1 >= 0:
                    if self.board[r+1][c-1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                    elif (r+1, c-1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r+1, c-1), self.board, is_ep=True))
                if c+1 < 8:
                    if self.board[r+1][c+1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c+1), self.board))
                    elif (r+1, c+1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r+1, c+1), self.board, is_ep=True))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = "w" if self.whiteToMove else "b"
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves, include_castle=True):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))
        if include_castle:
            self.getCastleMoves(r, c, moves)

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if self.whiteToMove and r == 7 and c == 4:
            if not self.wK_moved:
                if not self.wR_right_moved and self.board[7][5] == "--" and self.board[7][6] == "--":
                    if not self.squareUnderAttack(7, 5) and not self.squareUnderAttack(7, 6):
                        moves.append(Move((7, 4), (7, 6), self.board, is_castle=True))
                if not self.wR_left_moved and self.board[7][3] == "--" and self.board[7][2] == "--" and self.board[7][1] == "--":
                    if not self.squareUnderAttack(7, 3) and not self.squareUnderAttack(7, 2):
                        moves.append(Move((7, 4), (7, 2), self.board, is_castle=True))
        elif not self.whiteToMove and r == 0 and c == 4:
            if not self.bK_moved:
                if not self.bR_right_moved and self.board[0][5] == "--" and self.board[0][6] == "--":
                    if not self.squareUnderAttack(0, 5) and not self.squareUnderAttack(0, 6):
                        moves.append(Move((0, 4), (0, 6), self.board, is_castle=True))
                if not self.bR_left_moved and self.board[0][3] == "--" and self.board[0][2] == "--" and self.board[0][1] == "--":
                    if not self.squareUnderAttack(0, 3) and not self.squareUnderAttack(0, 2):
                        moves.append(Move((0, 4), (0, 2), self.board, is_castle=True))

    def get_material_advantage(self):
        white_score = sum(self.piece_values[p[1]] for p in self.captured_by_white)
        black_score = sum(self.piece_values[p[1]] for p in self.captured_by_black)
        if white_score > black_score:
            return 'w', white_score - black_score
        elif black_score > white_score:
            return 'b', black_score - white_score
        return None, 0


class Move():
    def __init__(self, start_sq, end_sq, board, is_castle=False, is_ep=False):
        self.startRow = start_sq[0]
        self.startCol = start_sq[1]
        self.endRow = end_sq[0]
        self.endCol = end_sq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isCastleMove = is_castle
        self.isEnpassantMove = is_ep
        if not self.isEnpassantMove and self.pieceMoved[1] == 'P' and self.pieceCaptured == '--' and self.startCol != self.endCol:
            self.isEnpassantMove = True
        if self.isEnpassantMove:
            self.pieceCaptured = 'bP' if self.pieceMoved == 'wP' else 'wP'
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True