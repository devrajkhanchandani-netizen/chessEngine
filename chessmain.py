import pygame as p
import chessengine as eng
import sys
import chessbrain as brain

BOARD_SIZE = 512
DIMENSIONS = 8
SQ_SIZE = BOARD_SIZE // DIMENSIONS
MAX_FPS = 60

LEFT_PADDING = 50
RIGHT_PADDING = 50
TOP_PANEL_HEIGHT = 100    
BOTTOM_PANEL_HEIGHT = 100 

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

    white_time = 600 * 1000 
    black_time = 600 * 1000

    player_one_human = True
    player_two_bot = True

    running = True
    while running:
        time_passed = clock.tick(MAX_FPS)
        
        if gs.whiteToMove:
            white_time -= time_passed
            if white_time <= 0:
                white_time = 0
                print("Black wins on time!")
                running = False
        else:
            black_time -= time_passed
            if black_time <= 0:
                black_time = 0
                print("White wins on time!")
                running = False

        human_turn = (gs.whiteToMove and player_one_human) or (not gs.whiteToMove and not player_two_bot)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN and human_turn:
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
                        valid_moves = gs.getValidMoves()
                        
                        for v_move in valid_moves:
                            if player_clicks[0] == (v_move.startRow, v_move.startCol) and \
                               player_clicks[1] == (v_move.endRow, v_move.endCol):
                                if v_move.isPawnPromotion:
                                    choice = get_promotion_choice(screen, gs.whiteToMove)
                                    gs.makeMove(v_move, choice)
                                else:
                                    gs.makeMove(v_move)
                                break
                            
                        selected_sq = ()
                        player_clicks = []

        if not human_turn and running:
            valid_moves = gs.getValidMoves()
            bot_move = brain.findRandomMove(valid_moves)
            if bot_move is not None:
                gs.makeMove(bot_move, 'Q') 
            else:
                running = False

        drawGameState(screen, gs, white_time, black_time)
        p.display.flip()
    p.quit()

def get_promotion_choice(screen, is_white):
    font = p.font.SysFont("Arial", 22, bold=True)
    options = ['Q', 'R', 'B', 'N']
    color_prefix = 'w' if is_white else 'b'
    
    panel_w = 320
    panel_h = 80
    panel_x = (WIDTH - panel_w) // 2
    panel_y = (HEIGHT - panel_h) // 2
    
    button_w = 60
    button_h = 50
    spacing = 15
    
    buttons = []
    for i, opt in enumerate(options):
        bx = panel_x + 20 + i * (button_w + spacing)
        by = panel_y + 15
        buttons.append((p.Rect(bx, by, button_w, button_h), opt))
        
    choosing = True
    while choosing:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mx, my = p.mouse.get_pos()
                for rect, opt in buttons:
                    if rect.collidepoint(mx, my):
                        return opt
                        
        p.draw.rect(screen, p.Color("#1e1e1e"), (panel_x, panel_y, panel_w, panel_h))
        p.draw.rect(screen, p.Color("#989795"), (panel_x, panel_y, panel_w, panel_h), 3)
        
        for rect, opt in buttons:
            p.draw.rect(screen, p.Color("#3c3c3c"), rect)
            p.draw.rect(screen, p.Color("#989795"), rect, 1)
            
            label = font.render(color_prefix + opt, True, p.Color("#FFFFFF") if is_white else p.Color("#000000"))
            l_rect = label.get_rect(center=rect.center)
            screen.blit(label, l_rect)
            
        p.display.flip()

def drawGameState(screen, gs, w_time, b_time):
    screen.fill(p.Color("#262522")) 
    drawBoard(screen)
    drawCoordinates(screen)
    drawPiecesText(screen, gs.board)
    drawDashboard(screen, gs, w_time, b_time)

def drawBoard(screen):
    colors = [p.Color("#eeeed2"), p.Color("#5E615B")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE + LEFT_PADDING, r * SQ_SIZE + TOP_PANEL_HEIGHT, SQ_SIZE, SQ_SIZE))

def drawCoordinates(screen):
    font = p.font.SysFont("Helvetica", 16, bold=True)
    text_color = p.Color("#989795")
    
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    
    for c in range(DIMENSIONS):
        x_pos = c * SQ_SIZE + LEFT_PADDING + SQ_SIZE // 2
        text_surface = font.render(files[c], True, text_color)
        
        text_rect = text_surface.get_rect(center=(x_pos, TOP_PANEL_HEIGHT - 15))
        screen.blit(text_surface, text_rect)
        
        text_rect = text_surface.get_rect(center=(x_pos, TOP_PANEL_HEIGHT + BOARD_SIZE + 15))
        screen.blit(text_surface, text_rect)
        
    for r in range(DIMENSIONS):
        y_pos = r * SQ_SIZE + TOP_PANEL_HEIGHT + SQ_SIZE // 2
        text_surface = font.render(ranks[r], True, text_color)
        
        text_rect = text_surface.get_rect(center=(LEFT_PADDING - 20, y_pos))
        screen.blit(text_surface, text_rect)
        
        text_rect = text_surface.get_rect(center=(LEFT_PADDING + BOARD_SIZE + 20, y_pos))
        screen.blit(text_surface, text_rect)

def drawPiecesText(screen, board):
    font = p.font.SysFont("Arial", 28, bold=True)
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                text_color = p.Color("#FFFFFF") if piece[0] == 'w' else p.Color("#000000")
                shadow_surface = font.render(piece, True, p.Color("#454545") if piece[0] == 'w' else p.Color("#888888"))
                text_surface = font.render(piece, True, text_color)
                
                x = c * SQ_SIZE + LEFT_PADDING + SQ_SIZE // 2
                y = r * SQ_SIZE + TOP_PANEL_HEIGHT + SQ_SIZE // 2
                
                screen.blit(shadow_surface, shadow_surface.get_rect(center=(x+1, y+1)))
                screen.blit(text_surface, text_surface.get_rect(center=(x, y)))

def format_time(ms):
    seconds = int(ms // 1000)
    minutes = seconds // 60
    rem_seconds = seconds % 60
    return f"{minutes:02d}:{rem_seconds:02d}"

def drawDashboard(screen, gs, w_time, b_time):
    font_timer = p.font.SysFont("Courier", 32, bold=True)
    font_ui = p.font.SysFont("Arial", 16, bold=True)
    
    b_timer_color = p.Color("#FF5555") if not gs.whiteToMove else p.Color("#AAAAAA")
    b_time_surf = font_timer.render(format_time(b_time), True, b_timer_color)
    screen.blit(b_time_surf, (WIDTH - RIGHT_PADDING - 120, 25))
    
    white_captured_str = " ".join([p[1] for p in gs.captured_by_white])
    cap_w_surf = font_ui.render(f"Captured by White: {white_captured_str}", True, p.Color("#EEEDF2"))
    screen.blit(cap_w_surf, (LEFT_PADDING, 35))
    
    adv_side, adv_score = gs.get_material_advantage()
    if adv_side == 'w':
        adv_surf = font_ui.render(f"+{adv_score}", True, p.Color("#769656"))
        screen.blit(adv_surf, (LEFT_PADDING + 220 + len(white_captured_str)*10, 35))

    w_timer_color = p.Color("#FF5555") if gs.whiteToMove else p.Color("#AAAAAA")
    w_time_surf = font_timer.render(format_time(w_time), True, w_timer_color)
    screen.blit(w_time_surf, (WIDTH - RIGHT_PADDING - 120, HEIGHT - BOTTOM_PANEL_HEIGHT + 25))
    
    black_captured_str = " ".join([p[1] for p in gs.captured_by_black])
    cap_b_surf = font_ui.render(f"Captured by Black: {black_captured_str}", True, p.Color("#111111"))
    screen.blit(cap_b_surf, (LEFT_PADDING, HEIGHT - BOTTOM_PANEL_HEIGHT + 35))
    
    if adv_side == 'b':
        adv_surf = font_ui.render(f"+{adv_score}", True, p.Color("#769656"))
        screen.blit(adv_surf, (LEFT_PADDING + 220 + len(black_captured_str)*10, HEIGHT - BOTTOM_PANEL_HEIGHT + 35))

if __name__ == "__main__":
    main()