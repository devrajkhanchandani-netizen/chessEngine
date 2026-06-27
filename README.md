i have just recently learnt DSA and ML and this project is my attempt to test out my skills, all the commits with their history and what they include will be defined below along with the architecture & system design, installation & setup run guide and features roadmap


---


**Module Breakdown**


1. chessmain.py
   
   this is the main entry point of the app. it manages the Pygame event loop, caps the frame rate at 60 FPS, and handles user interactions
   

   how it works: it translates raw screen coordinate clicks into board matrix rows and columns (col = (mx - PADDING) // SQ_SIZE).

   threading architecture: to prevent the OS from thinking the app crashed during heavy calculations, it offloads the deep alpha-beta lookahead search loops to a       background worker thread. this keeps the primary thread free to smoothly render the UI animations, real-time match timers (MM:SS:mmm), and move history sidebars.


2. chessengine.py
   
   this module behaves as the single source of truth for the game state. it knows absolutely nothing about graphics or AI heuristics—it just strictly enforces the laws of chess.

   
   how it works: the board layout is tracked using an internal 8×8 2D matrix array where strings represent pieces (e.g., 'wR' for White Rook, '--' for empty cells).

   state tracking & rollbacks: it contains the move execution loop (makeMove) and the state history stack (undoMove). when a move is rolled back, the engine pops the last transaction off the history stack and re-synchronizes the piece matrices, turn tracking booleans, castling rights logs, and en passant vulnerabilities perfectly.


3. chessbrain.py
   
   this is the heavy-lifting optimization layer where the bot actually figures out what to play. it parses the game tree recursively to uncover the highest-value lines.

   
   how it works: it implements a Minimax tree-traversal structure optimized by an Alpha-Beta pruning loop. it scores the terminal states using a relative material weight lookup dictionary.
   optimization pipeline: to prevent the exponential explosion of checking millions of bad branches, it runs an internal orderMoves method. by sorting moves based on an MVV-LVA (Most Valuable Victim - Least Valuable Attacker) heuristic scale, it pushes high-priority tactical events like captures and pawn promotions to the front of the call stack. this guarantees that the alpha-beta bounds snap shut instantly, keeping the engine lightning fast even at 6 plies deep.


---


**Installation & Quick Start**

to spin up the dashboard and play against the bot locally, clone the repo and run the presentation script

Prerequisites:-
make sure you have python installed along with the pygame framework wrapper

pip install pygame



clone the repository:- 

git clone [https://github.com/devrajkhanchandani-netizen/chessEngine.git](https://github.com/devrajkhanchandani-netizen/chessEngine.git)

cd chessEngine

launch the interactive dashboard

python chessmain.py


---


**Next Steps & Optimization Roadmap**

   the core engine is highly stable, but there are a few advanced algorithmic upgrades i am planning to implement next to push the search depth past 6 plies:

   1. [ ] Quiescence Search: adding an unstable state lookup function at the horizon layer to evaluate trailing captures, permanently killing the Horizon Effect where the bot hangs pieces on deep plies.
   2. [ ] Zobrist Hashing & Transposition Tables: building a custom hashing matrix to assign unique 64-bit keys to board layouts. this lets the engine cache previously evaluated positions in a hash table so it never re-calculates duplicate positions across different branches.
   3. [ ] Bitboards Migration: refactoring the core state manager away from standard 2D Python list arrays into 64-bit primitive integers (2^64 bitmasks) to handle move generation via ultra-fast bitwise operators.


---


**Development Logs**


1. initialize board matrix, translation layout structures and basic move execution:-

   this is the initial version where i have initialized the logical core of the application inside chessengine.py, created a primary "GameState" class containing a 2D matrix array (8×8 string list) to map the coordinate positions of every chess piece on a physical board

   * capabilities introduced - 
     1. built boolean trackers to monitor turn rotations(whiteToMove) and end game triggers(checkmate, stalemate)
     2. created a translation object to encapsulate raw move parameters (handling start positions, target landing coordinates, piece identifications, tracking captured entities)
     3. added the baseline data shift function to modify matrix values, update state history logs and swap player turns
    

2. full visual rendering layer with nested loops and chess piece (notations) rendering:-

   this version deploys the frontend presentation pipeline inside of chessmain.py using Pygame to manage execution frame rates, native layout windows, and graphical text canvas blitting

   * capabilities introduced -
     1. bounded static window dimensions, bounding rectangles and perimeter padding zones to isolate the matrix grid from any menu elements
     2. implemented a nested row column loop parsing parity sums (r+c(mod2)) to colour alternate checked tiles on screen
     3. integrated system font vector engines to scan real time game state strings and map text piece labels precisely to the midpoint of the cells


3. implemented click sequence event tracking and grid cell conversion matrices:-

   this version integrates active mouse event listeners into the core loop, creating a translation layer that maps monitor pixels back into data coordinates

   * capabilities introduced -
     1. deployed pixel to matrix downscaling coordinate matrix
     2. structured a state safety tracking array (player_clicks) to filter out coordinates beyond the board boundaries, engaged same grid double click deselection sequences and stage cell indices
     3. coupled the completed input coordinate pairs directly to the backend execution pipeline to handle piece relocation across the board matrix


4. implemented vector move generation logic for all standard pieces:-

   this version kills the sandbox mode, locked down the actual geometry vectors and hitboxes for the entire piece set

   * capabilities introduced -
     1. initialized a master router loop (getAllPossibleMoves) to scan the given chess grid, check the piece, and pipe the data to its specific validation function
     2. programmed continuous raycasting direction vectors for rooks, bishops, and queens that slide outward until blocked by board boundaries, friendly elements and/or terminal enemy captures
     3. mapped step matrices for kings and knights alongside directional translation paths for W&B pawns to evaluate initial two step sprints and diagonal capture scenarios


5. long/short castling integration:-

   this version adds full move validation for both king-side and queen-side castling, making sure the engine strictly obeys all standard rule constraints and king safety checks

   * capabilities introduced -
     1. implemented path-clearance loops to verify that every square between the king and the target rook is completely empty
     2. integrated active square-attack checks to ensure the king doesn't move out of check, pass through a threatened square, or land in check
     3. deployed persistent boolean tracking flags (hasKingMoved, hasRookMoved) inside the game state class to permanently kill castling rights once a piece moves
     

6. En Passant integration:-

   this version handles the tricky mechanics of en passant captures by tracking temporary pawn vulnerabilities across consecutive game moves

   * capabilities introduced -
     1. engineered a dynamic enPassantPossible tuple tracker to temporarily store the target square coordinates behind any pawn that just pulled a 2-square initial sprint
     2. developed a conditional pop routine to automatically wipe the captured pawn from the board matrix when the attacking pawn moves diagonally into the empty space
     3. updated the engine's undoMove stack to ensure that rolling back an en passant capture perfectly restores both the piece positions and the captured piece list


7. Random move generation:-

   this version sets up a basic automated testing bot that plays random legal moves to stress-test the state stability and catch bugs before building out the search tree
  
   * capabilities introduced -
     1. hooked up a pseudo-random choice selector inside the primary execution loop to pick an arbitrary move out of the filtered valid moves array
     2. built a continuous test-game script to simulate back-to-back bot games, checking for memory leaks or game crashes over hundreds of moves
     3. verified basic piece routing rules by making sure random selections still respect board boundaries and piece-specific move vectors


9. uses recursion to look 2 moves deep:-
  
   this version upgrades the bot from a random picker to a basic lookahead engine by introducing a recursive tree search to evaluate immediate future positions
  
   * capabilities introduced -
     1. developed a recursive search function that executes a move, drills down to check the opponent's responses, and rewinds the board state using undoMove
     2. added a hard-coded depth limit to break the recursive call stack exactly at 2 plies, bouncing the evaluated score back up the tree
     3. mapped a baseline material heuristic to count up and assign static point values to active pieces on the final board layout at the horizon limit


9. uses alpha-beta pruning and minimax algorithm to look 3 moves deep:-
  
   this version optimizes the search framework by pairing the minimax algorithm with alpha-beta bounds to aggressively cut off dead branches early
  
   * capabilities introduced -
     1. structured a standard maximizer/minimizer adversarial loop where the bot optimizes its own score while assuming the opponent will play the absolute best counter-move
     2. introduced dynamic α and β variables to trigger early loop break cutoffs the millisecond a branch proves to be worse than an already evaluated path
     3. successfully pushed the effective calculation depth to 3 plies deep without causing any frame drops or exponential lag in the application loop


10. implemented advanced move ordering and conked up search depth to 6 piles deep:-
  
   this version massively accelerates tree traversal times by sorting the move queue, forcing quick alpha-beta cutoffs and maximizing the overall search depth

   * capabilities introduced -
     1. built a dedicated orderMoves sorting function that pushes high-value tactical moves like captures and promotions to the front of the evaluation queue
     2. applied a MVV-LVA (Most Valuable Victim - Least Valuable Attacker) weight scale to optimize capture sorting, allowing the engine to find refutations instantly
     3. scaled the live processing depth up to a massive 6 plies by ditching millions of dead board branches before wasting CPU cycles searching them


11. added history, undo and resign buttons, changed time format and added threading:-
  
   this version rewrites the Pygame application into a clean, multi-threaded layout complete with interactive dashboard widgets and a high-precision match timer
  
   * capabilities introduced -
     1. offloaded the heavy alpha-beta search logic from the main UI thread onto a background thread, preventing the Pygame window from freezing during deep calculations
     2. mapped precise mouse bounding boxes (p.Rect) over the sidebar layout to build fully functional, clickable Undo and Resign dashboard buttons
     3. updated the match clock rendering pipeline to parse raw millisecond integers into a highly readable, real-time updated MM:SS:mmm string layout
