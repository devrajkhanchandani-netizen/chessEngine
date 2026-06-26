import pygame as p
import chessengine as eng

BOARD_SIZE = 512
DIMENSIONS = 8
SQ_SIZE = BOARD_SIZE // DIMENSIONS
MAX_FPS = 15

LEFT_PADDING = 40
RIGHT_PADDING = 40
TOP_PANEL_HEIGHT = 80    
BOTTOM_PANEL_HEIGHT = 80 

WIDTH = BOARD_SIZE + LEFT_PADDING + RIGHT_PADDING
HEIGHT = BOARD_SIZE + TOP_PANEL_HEIGHT + BOTTOM_PANEL_HEIGHT

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess Engine - Dashboard Mode")
    clock = p.time.Clock()
    gs = eng.GameState()

    selected_sq = ()  
    player_clicks = []  

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                
                col = (location[0] - LEFT_PADDING) // SQ_SIZE
                row = (location[1] - TOP_PANEL_HEIGHT) // SQ_SIZE
                
                if 0 <= row < 8 and 0 <= col < 8:
                    if selected_sq == (row, col):
                        selected_sq = ()
                        player_clicks = []
                    else:
                        selected_sq = (row, col)
                        player_clicks.append(selected_sq)
                    
                    if len(player_clicks) == 2:
                        move = eng.Move(player_clicks[0], player_clicks[1], gs.board)
                        valid_moves = gs.getValidMoves()
                        
                        for v_move in valid_moves:
                            if move.startRow == v_move.startRow and move.startCol == v_move.startCol and \
                               move.endRow == v_move.endRow and move.endCol == v_move.endCol:
                                gs.makeMove(v_move)
                                break
                            
                        selected_sq = ()
                        player_clicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()

def drawGameState(screen, gs):
    screen.fill(p.Color("white"))
    drawBoard(screen)
    drawPiecesText(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE + LEFT_PADDING, r * SQ_SIZE + TOP_PANEL_HEIGHT, SQ_SIZE, SQ_SIZE))

def drawPiecesText(screen, board):
    font = p.font.SysFont("Arial", 24, bold=True)
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                text_color = p.Color("darkblue") if piece[0] == 'w' else p.Color("black")
                text_surface = font.render(piece, True, text_color)
                text_rect = text_surface.get_rect()
                text_rect.center = (c * SQ_SIZE + LEFT_PADDING + SQ_SIZE // 2, r * SQ_SIZE + TOP_PANEL_HEIGHT + SQ_SIZE // 2)
                screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    main()