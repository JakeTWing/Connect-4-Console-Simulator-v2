import random
from board_class import board
class ai:
    
    def __init__(self, is_x, hard_mode = False, path_len = 4):
        if is_x:
            self.ai_peice = "x"
        else:
            self.ai_peice = "o"

        self.is_ai_x = is_x
        self.board_array = []
        self.hard_mode = hard_mode
        self.difficulty = path_len #path length for recursion; used in hard ai
        
        
        
    def update_board_array(self, current_board_array):
        self.board_array = current_board_array
    
 
    
    def ret_ai_peice(self):
        return self.ai_peice
        
        
        
    #finds the columns that arent full
    #returns a list of the indexes of the columns that arent full
    def find_open_columns(self):
        
        if len(self.board_array) == 0: #prevents an error
            print("No board added to ai object")
            return 0
        
        open_columns = [i for i in range(7)] #adds every column value to the open_columns list
        
        
        for index in range(len(self.board_array[0])):  #loops through the top row

            
            if self.board_array[0][index] != " ": #finds full columns by checking the top column
                open_columns.remove(index) #removes the value if the column is full
                
        return open_columns
    
    
    
    #generates a move and updates the board attribute to the one inputed
    #changes depending on if hard_mode is true or false
    def find_move(self, current_board_array):
        
        self.update_board_array(current_board_array)
        

        if self.hard_mode and self.difficulty > 0:
            #selects very good moves
            return(self.find_move_hard(self.difficulty))
            
            
            
        else:
            #selects a random value from the open columns on the grid
            return self.find_move_easy()
            
            



    #chooses a random open column
    def find_move_easy(self):
        
        open_columns = self.find_open_columns() #list of columns that are not full

        if len(open_columns) > 0: 
            ai_move = open_columns[random.randint(0, len(open_columns) - 1)] #choses a random value from the list open_columns
            
        else: #error message if there is no open columns *should never realistly happen*
            print("AI, No move avalible")
            return 0 
            
        return ai_move
        


        
    #calls the simulate method to recurse through board states to find a great move
    #path_len is how deep the recursion goes
    def find_move_hard(self,  path_len = 4):

            
        #creates a board object
        current_board = board(self.board_array)
        results = self.simulate(self.is_ai_x, current_board, path_len) #calls the simulate method
        
        return results[1]
        
        
        

    #More optimised
    #NEW same result but mutates the one board object instead of deep copying
    
    #method will recurse its self with a loop alterating between returning a positive (for its own moves) score and a
    #negitive score(for opponent moves); for each time its called, it recurses 6 more times (unless the collumn is full/invalid move, a win is found)
    #mutates the board object each iteration of the loop, then reverses it for the next iteration
    
    #it then compares the strength of each move in the loop and sets 'best_score' to the highest/lowest score found. 'best_move' is set to the index of that move
    
    #once 'n', number of recursions in current path, reaches 'path_len' the recursion stops. at this point it will call the 'eval_pos' method which analises the final state
    #and returns minor score changes based on the current board state. 'eval_pos' finds positions that will be more benifital to the ai for future moves. does not effect descisions if the ai finds a win within the length of 'path_len'
    
    #closer wins will be selected over farther wins as the score aloted for winning is subtracted/added by 'n'
    
    
    def simulate(self, is_x, board, path_len, n = 0):
        
        ai_turn = is_x == self.is_ai_x #determines if its the ai's turn
        
        best_move = 3 #column of the best move
        best_score = -10000000 #max score for your moves
        
        if not ai_turn: #if opponets move try to find min score
            best_score = 10000000
        
        #Base Case, calls the 'eval_pos' method to find the best position
        if n >= path_len:
            return self.eval_pos(board), -1
            
        
        #main loop, looping through the length of one row
        for i in range(len(board.ret_grid()[0])):

            
        
            
            
            valid_move = board.place_peice(is_x, i, False)[0] #updating the grid; #attempts to place a peice, if the row is full skip this move
            
            
            if not(valid_move):
                continue

            
            
            win, location, draw = board.check_for_win(is_x, i) #after the move is made, check for a win and a draw. *location is not needed in this method but is still part of the 'win' method for other uses*
            
            score = 0 #score for the current move
            

            if win: #if a win is found set score to 5000 - n (reverse for opponent) and stop recursing the path.
                
                if ai_turn:
                    score = 1250 - n 
                    
            
                else:
                    score = -1250 + n
                
                
            elif draw: #if a draw is reached, set  score to 0 and stop recursion
                score = 0
                
            else:
                #if no win or draw continue recursion. *alternate 'is_x' and add 1 to 'n'
                score  = self.simulate(not is_x, board, path_len, n+1)[0] #take only the best score returned from the recursion
            
            board.remove_peice(i) #removes the prev move so the next move is different
                
            #calculating scores    
            if ai_turn: 
                if score > best_score: #Setting 'best_score' to the greatest score
                    best_move = i #updates 'best_move' as 'best_score' is updated
                    best_score = score
                    
                elif score == best_score: #if the scores are a tie, choose a random one as the best *only comes into play if the scores are equal
                    if random.randint(0,1) == 1:
                        best_move = i
                        
            #opponent's turn   
            else:
                if score < best_score: #Setting 'best_score' to the lowest possible score. *finding your opponents best possible move in that position
                    best_move = i #updates 'best_move' alongside
                    best_score = score
                elif score == best_score:
                    if random.randint(0,1) == 1: #if two moves are choose one at random
                        best_move = i
                    
            
                
                

            
            
        
        return best_score, best_move






    #calls mulitple methods to calculate how benifitial a board state is to the ai. 
    def eval_pos(self, prev_board):
        board_state_score = 0 #total score of the board, will never be greater than a win
        
        board_state_score += self.position_scores(prev_board.ret_grid())
        board_state_score += self.vertical_connections(prev_board.ret_grid())
        board_state_score += self.horizontal_connections(prev_board.ret_grid())
        board_state_score += self.diagonal_right_connections(prev_board.ret_grid())
        board_state_score += self.diagonal_left_connections(prev_board.ret_grid())
        
        return board_state_score
        




    #increases score for peices that are lower and closer to the middle. And decreases for peices that are closer to the edge and higher on the board
    #decreases for opponent with the same criterias
    def position_scores(self, grid):
        board_state_score = 0
        
        
        for outer, row in enumerate(grid):
            #closer to the bottom, better score; vis versa
            bottom_row_bonus = 0
            if outer == 5: #bottom
                bottom_row_bonus += 2
            elif outer == 4: #one above the bottom
                bottom_row_bonus += 1
            elif outer <= 2: #above row 3 *no longer can win vertical if peice below is not yours 
                bottom_row_bonus -= 1
                
            
            
            
            for inner, col in enumerate(row):
                
                if col == self.ai_peice: 
                    if inner == 3: #center row
                        board_state_score += 2 + bottom_row_bonus
                        
                    elif inner == 2 or inner == 4: #left and right of the center
                        board_state_score += 1 + bottom_row_bonus
                        
                    elif inner == 0 or inner == 6:#edge rows
                        board_state_score -= 1 + bottom_row_bonus
                
                elif col != " ": #opponents turn, decreases for how strong their board is
                    
                    if inner == 3:
                        board_state_score -= 2 - bottom_row_bonus
                        
                    elif inner == 2 or inner == 4:
                        board_state_score -= 1 - bottom_row_bonus
                        
                    elif inner == 0 or inner == 6:
                        board_state_score += 1 - bottom_row_bonus
        
        #caps the ammount that can be gained from position                
        if board_state_score > 25:
            board_state_score = 25
        elif board_state_score < -25:
            board_state_score = -25
            
        return board_state_score     
        
   



    #checks the board for 3 connections and 2 connections positions with 1 / 2 playable spaces above
    def vertical_connections(self, grid):
        board_state_score = 0
        
        for outer, cols in enumerate(grid[0]): #columns
            
            for i in range(3): #windows of 4 peices in a single collumn (3)
                ai_peice_count = 0 #ai peices in a single window
                opponent_peice_count = 0 #opponent peices in a single window

                
                for j in range(4): #looping window 
                    peice = grid[i + j][outer] #goes down one spot per iteration
                    
                    if peice == self.ai_peice:
                        ai_peice_count += 1
                    elif peice != " ":
                        opponent_peice_count += 1

                #increasing score for the board state
                if opponent_peice_count == 0: #no opponent peices in the window means there is only your peices/blank spaces in the window
                    
                    if ai_peice_count == 3:
                        board_state_score += 20 #score for 3 in a row
                        
                    elif ai_peice_count == 2:
                        board_state_score += 1 #score for 2 in a row
                        
                #decreasing the score for the board state        
                elif ai_peice_count == 0: #same logic applys
                    
                    if opponent_peice_count == 3:
                        board_state_score -= 20 
                        
                    elif opponent_peice_count == 2:
                        board_state_score -= 1
                    
                    
                
                
             
        return board_state_score






    #finds horizontal connections of 3 and 2
    def horizontal_connections(self, grid):
        board_state_score = 0
        
        for outer, row in enumerate(grid):

                
            for i in range(4): #windows per row
                ai_peice_count = 0
                opponent_peice_count = 0
                supported_blanks = 0 #for blank to be counted it must have a peice under it
                
                for j in range(4): #len of windows
                    peice = grid[outer][i+j] #increase col by one
                    
                    #counting peices for the ai and opponent along side valid blank spaces in the window or be in row 5
                        
                    if peice == self.ai_peice:
                        ai_peice_count += 1
                            
                    elif peice != " ":
                        opponent_peice_count += 1
                            
                    else:
                        #finding valid blank spaces
                        if outer == 5:
                            supported_blanks += 1
                            
                        else:
                            if grid[outer + 1][i + j] != " ":
                                supported_blanks += 1
                
                
                #increasing score for the board state
                if opponent_peice_count == 0:
                    
                    if ai_peice_count == 3 and supported_blanks == 1:
                        board_state_score += 20
                        
                    elif ai_peice_count == 2 and supported_blanks == 2:
                        board_state_score += 2
                        
                #decreasing the score for the board state
                elif ai_peice_count == 0:
                    
                    if opponent_peice_count == 3 and supported_blanks == 1:
                        board_state_score -= 20
                        
                    elif opponent_peice_count == 2 and supported_blanks == 2:
                        board_state_score -= 2                               
        
        return board_state_score
        
        
        
        
        
        #finds diagonal connections to the down and right
    def diagonal_right_connections(self, grid):
        board_state_score = 0
        #The only possible spaces with a diagonal down and right connection length of 4 are
        #located in the top left corner bound by row = 2 and col = 3; row <= 2 and col <= 3
        
        for row in range(3): #index for the starting row of the window
        
            for col in range(4): #index for the starting column of the window
                
                ai_peice_count = 0
                opponent_peice_count = 0
                supported_blanks = 0 #for blank to be counted it must have a peice under it or be in row 5
                

                
                for w in range(4):
                    #moves down and to the right one square
                    peice = grid[row + w][col + w]
                    
                    #counting peices and supported blanks
                    if peice == self.ai_peice:
                            ai_peice_count += 1
                            
                    elif peice != " ":
                        opponent_peice_count += 1
                        
                            
                    else:
                            
                        if row + w == 5:
                            supported_blanks += 1
                            
                        else:
                            #adds one to row + w to check the peice under the current peice
                            if grid[row + w + 1][col + w] != " ":
                                supported_blanks += 1
                                
                                
                #increasing score for the board state
                if opponent_peice_count == 0:
                    
                    if ai_peice_count == 3 and supported_blanks == 1:
                        board_state_score += 23
                        
                    elif ai_peice_count == 2 and supported_blanks == 2:
                        board_state_score += 2
                        
                #decreasing the score for the board state
                elif ai_peice_count == 0:
                    
                    if opponent_peice_count == 3 and supported_blanks == 1:
                        board_state_score -= 23
                        
                    elif opponent_peice_count == 2 and supported_blanks == 2:
                        board_state_score -= 2                               
        
        return board_state_score


    #finds diagonal connections to the down and right
    def diagonal_left_connections(self, grid):
        board_state_score = 0
        #The only possible spaces with a diagonal down and left connection with a length of 4 are
        #located in the top right corner bound by row = 2 and col = 3; row <= 2 and col >= 3
        for row in range(3): #index for the starting row of the window
        
            for col in range(4): #index for the starting column of the window
                
                ai_peice_count = 0
                opponent_peice_count = 0
                supported_blanks = 0 #for blank to be counted it must have a peice under it or be in row 5
                

                
                for w in range(4):
                    #row increases by one to move down a row
                    #col starts at 3 (as the starting space must be >= 3 for a window to be possible)
                    #then it decreases down
                    peice = grid[row + w][(3 + col) - w]
                                        
                    #counting peices
                    if peice == self.ai_peice:
                            ai_peice_count += 1
                            
                    elif peice != " ":
                        opponent_peice_count += 1
                        
                            
                    else:
                            
                        if row + w == 5:
                            supported_blanks += 1
                            
                        else:
                            #finds the supported blanks by adding one to the row to check the spot directly under
                            if grid[(row + w) + 1][(3 + col) - w] != " ":
                                supported_blanks += 1
                                
                                
                #increasing score for the board state
                if opponent_peice_count == 0:
                    
                    if ai_peice_count == 3 and supported_blanks == 1:
                        board_state_score += 23
                        
                    elif ai_peice_count == 2 and supported_blanks == 2:
                        board_state_score += 2
                        
                #decreasing the score for the board state
                elif ai_peice_count == 0:
                    
                    if opponent_peice_count == 3 and supported_blanks == 1:
                        board_state_score -= 23
                        
                    elif opponent_peice_count == 2 and supported_blanks == 2:
                        board_state_score -= 2                               
        
        return board_state_score
