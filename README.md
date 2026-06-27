i have just recently learnt DSA and ML and this project is my attempt to test out my skills, all the commits with their history and what they include extra will be defined below


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


5. 