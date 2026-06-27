import pygame as p
import chessengine as eng
import sys
import chessbrain as brain

BOARD_SIZE = 512
DIMENSIONS = 8
SQ_SIZE = BOARD_SIZE // DIMENSIONS
MAX_FPS = 60

LEFT_PADDING = 30
TOP_PANEL_HEIGHT = 80    
BOTTOM_PANEL_HEIGHT = 60 

SIDEBAR_WIDTH = 280
SIDEBAR_PADDING = 20

WIDTH = BOARD_SIZE + LEFT_PADDING + SIDEBAR_WIDTH + SIDEBAR_PADDING
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

    resign_triggered = False
    winner_text = ""

    running = True
    while running:
        time_passed = clock.tick(MAX_FPS)
        
        if not resign_triggered and winner_text == "":
            if gs.whiteToMove:
                white_time -= time_passed
                if white_time <= 0:
                    white_time = 0
                    winner_text = "Black wins on time!"
            else:
                black_time -= time_passed
                if black_time <= 0:
                    black_time = 0
                    winner_text = "White wins on time!"

        human_turn = (gs.whiteToMove and player_one_human) or (not gs.whiteToMove and not player_two_bot) and not resign_triggered and winner_text == ""

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                
                undo_rect, resign_rect = get_control_buttons_rects()
                if undo_rect.collidepoint(location):
                    gs.undoMove()
                    if player_two_bot:
                        gs.undoMove()
                    selected_sq = ()
                    player_clicks = []
                    resign_triggered = False
                    winner_text = ""
                    continue
                
                if resign_rect.collidepoint(location) and not resign_triggered and winner_text == "":
                    resign_triggered = True
                    winner_text = "Black wins by resignation" if gs.whiteToMove else "White wins by resignation"
                    continue

                if human_turn:
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

        if not human_turn and running and not resign_triggered and winner_text == "":
            valid_moves = gs.getValidMoves()
            bot_move = brain.findBestMove(gs, valid_moves)
            if bot_move is not None:
                gs.makeMove(bot_move, 'Q') 
            else:
                if gs.inCheck():
                    winner_text = "Black wins by checkmate" if gs.whiteToMove else "White wins by checkmate"
                else:
                    winner_text = "Stalemate!"

        drawGameState(screen, gs, white_time, black_time, winner_text)
        p.display.flip()
    p.quit()

def get_control_buttons_rects():
    sidebar_x = LEFT_PADDING + BOARD_SIZE + 15
    buttons_y = HEIGHT - BOTTOM_PANEL_HEIGHT - 10
    undo_rect = p.Rect(sidebar_x + 140, buttons_y, 110, 40)
    resign_rect = p.Rect(sidebar_x + 10, buttons_y, 110, 40)
    return undo_rect, resign_rect

def get_promotion_choice(screen, is_white):
    font = p.font.SysFont("Arial", 22, bold=True)
    options = ['Q', 'R', 'B', 'N']
    color_prefix = 'w' if is_white else 'b'
    
    panel_w = 320
    panel_h = 80
    panel_x = (BOARD_SIZE + LEFT_PADDING - panel_w) // 2 + LEFT_PADDING
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

def drawGameState(screen, gs, w_time, b_time, winner_text):
    screen.fill(p.Color("#1e1e1e")) 
    drawBoard(screen)
    drawCoordinates(screen)
    drawPiecesText(screen, gs.board)
    drawDashboard(screen, gs, w_time, b_time, winner_text)

def drawBoard(screen):
    colors = [p.Color("#eeeed2"), p.Color("#5E615B")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE + LEFT_PADDING, r * SQ_SIZE + TOP_PANEL_HEIGHT, SQ_SIZE, SQ_SIZE))

def drawCoordinates(screen):
    font = p.font.SysFont("Helvetica", 14, bold=True)
    text_color = p.Color("#757470")
    
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    
    for c in range(DIMENSIONS):
        x_pos = c * SQ_SIZE + LEFT_PADDING + SQ_SIZE // 2
        text_surface = font.render(files[c], True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=(x_pos, TOP_PANEL_HEIGHT - 12)))
        screen.blit(text_surface, text_surface.get_rect(center=(x_pos, TOP_PANEL_HEIGHT + BOARD_SIZE + 12)))
        
    for r in range(DIMENSIONS):
        y_pos = r * SQ_SIZE + TOP_PANEL_HEIGHT + SQ_SIZE // 2
        text_surface = font.render(ranks[r], True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=(LEFT_PADDING - 15, y_pos)))
        screen.blit(text_surface, text_surface.get_rect(center=(LEFT_PADDING + BOARD_SIZE + 15, y_pos)))

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
    total_seconds = int(ms // 1000)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    milliseconds = int(ms % 1000)
    return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def drawDashboard(screen, gs, w_time, b_time, winner_text):
    font_timer = p.font.SysFont("Courier", 22, bold=True)
    font_ui = p.font.SysFont("Arial", 14, bold=True)
    font_history = p.font.SysFont("Arial", 14)
    font_history_bold = p.font.SysFont("Arial", 14, bold=True)
    
    sidebar_x = LEFT_PADDING + BOARD_SIZE + 15
    sidebar_w = SIDEBAR_WIDTH - 10
    sidebar_h = BOARD_SIZE
    
    p.draw.rect(screen, p.Color("#262522"), (sidebar_x, TOP_PANEL_HEIGHT, sidebar_w, sidebar_h))
    p.draw.rect(screen, p.Color("#3c3c3c"), (sidebar_x, TOP_PANEL_HEIGHT, sidebar_w, sidebar_h), 1)

    b_timer_color = p.Color("#FF5555") if not gs.whiteToMove else p.Color("#AAAAAA")
    b_time_surf = font_timer.render(format_time(b_time), True, b_timer_color)
    screen.blit(b_time_surf, (LEFT_PADDING + BOARD_SIZE - 140, 30))
    
    white_captured_str = " ".join([p[1] for p in gs.captured_by_white])
    cap_w_surf = font_ui.render(f"Captured by White: {white_captured_str}", True, p.Color("#EEEDF2"))
    screen.blit(cap_w_surf, (LEFT_PADDING, 35))
    
    adv_side, adv_score = gs.get_material_advantage()
    if adv_side == 'w':
        adv_surf = font_ui.render(f"+{adv_score}", True, p.Color("#769656"))
        screen.blit(adv_surf, (LEFT_PADDING + 140 + len(white_captured_str)*8, 35))

    w_timer_color = p.Color("#FF5555") if gs.whiteToMove else p.Color("#AAAAAA")
    w_time_surf = font_timer.render(format_time(w_time), True, w_timer_color)
    screen.blit(w_time_surf, (LEFT_PADDING + BOARD_SIZE - 140, HEIGHT - BOTTOM_PANEL_HEIGHT + 15))
    
    black_captured_str = " ".join([p[1] for p in gs.captured_by_black])
    cap_b_surf = font_ui.render(f"Captured by Black: {black_captured_str}", True, p.Color("#989795"))
    screen.blit(cap_b_surf, (LEFT_PADDING, HEIGHT - BOTTOM_PANEL_HEIGHT + 15))
    
    if adv_side == 'b':
        adv_surf = font_ui.render(f"+{adv_score}", True, p.Color("#769656"))
        screen.blit(adv_surf, (LEFT_PADDING + 140 + len(black_captured_str)*8, HEIGHT - BOTTOM_PANEL_HEIGHT + 15))

    row_y = TOP_PANEL_HEIGHT + 15
    col1_x = sidebar_x + 15
    col2_x = sidebar_x + 75
    col3_x = sidebar_x + 165
    
    moves_to_render = []
    for i in range(0, len(gs.moveLog), 2):
        w_move = gs.moveLog[i]
        b_move = gs.moveLog[i+1] if i+1 < len(gs.moveLog) else None
        moves_to_render.append((i//2 + 1, w_move.getNotation(), b_move.getNotation() if b_move else ""))

    max_visible_rows = 10
    start_index = max(0, len(moves_to_render) - max_visible_rows)
    visible_moves = moves_to_render[start_index:]

    for index, w_not, b_not in visible_moves:
        num_surf = font_history_bold.render(f"{index}.", True, p.Color("#757470"))
        w_surf = font_history.render(w_not, True, p.Color("#FFFFFF"))
        b_surf = font_history.render(b_not, True, p.Color("#FFFFFF"))
        
        screen.blit(num_surf, (col1_x, row_y))
        screen.blit(w_surf, (col2_x, row_y))
        screen.blit(b_surf, (col3_x, row_y))
        row_y += 28

    undo_rect, resign_rect = get_control_buttons_rects()
    
    p.draw.rect(screen, p.Color("#31302c"), resign_rect)
    p.draw.rect(screen, p.Color("#757470"), resign_rect, 1)
    res_text = font_ui.render("Resign", True, p.Color("#FFFFFF"))
    screen.blit(res_text, res_text.get_rect(center=resign_rect.center))
    
    p.draw.rect(screen, p.Color("#31302c"), undo_rect)
    p.draw.rect(screen, p.Color("#757470"), undo_rect, 1)
    un_text = font_ui.render("Undo", True, p.Color("#FFFFFF"))
    screen.blit(un_text, un_text.get_rect(center=undo_rect.center))

    if winner_text != "":
        font_win = p.font.SysFont("Arial", 18, bold=True)
        text_surf = font_win.render(winner_text, True, p.Color("#FF5555"))
        panel_w = 260
        panel_h = 50
        px = LEFT_PADDING + (BOARD_SIZE - panel_w) // 2
        py = TOP_PANEL_HEIGHT + (BOARD_SIZE - panel_h) // 2
        p.draw.rect(screen, p.Color("#1e1e1e"), (px, py, panel_w, panel_h))
        p.draw.rect(screen, p.Color("#FF5555"), (px, py, panel_w, panel_h), 2)
        screen.blit(text_surf, text_surf.get_rect(center=(px + panel_w//2, py + panel_h//2)))

if __name__ == "__main__":
    main()