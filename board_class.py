import os
class board:
    
    def clear_console(): #clears the console
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
          
            
    def __init__(self, grid = None):
        if grid == None:
            self.grid = [[" " for j in range(7)] for i in range(6)]
        else:
            self.grid = grid
        
        
    def ret_grid(self): #returns grid
        return self.grid
    
    
    def ret_grid_copy(self): #returns a deep copy of grid
        ret_grid = [row[:] for row in self.grid]

            
        return ret_grid
    
    
    def remove_peice(self, col): #removes the top peice from a chosen column
        
        for i in range(len(self.grid)):
            
            if self.grid[i][col] != " ":
                self.grid[i][col] = " "
                break
            
    
    def print_grid(self): #prints the grid only
        for row in self.grid:
            print(row)
            
            
    def clear_board(self): #resets the board to blank
        
        self.grid = [[" " for j in range(7)] for i in range(6)]
        
        
    def update_grid(self, new_grid): #updates the grid to an inputed grid
        self.grid = new_grid
        
    #returns the chosen_column now
    #places a peice on the board with the selected column
    def place_peice(self, is_player_x, chosen_column, print_error = True):

        
        valid_move = True
        
        if is_player_x:
            player_peice = "x"
        else:
            player_peice = "o"

        if chosen_column < 0 or chosen_column > 6: #checks for a valid column number
            valid_move = False
            if print_error:
                print(f"column must be in the range 0 to 6; you chose {chosen_column}")
            return (valid_move, chosen_column) #ending
        
        if self.grid[0][chosen_column] != " ": #if column is full send a error message and od nothing
            valid_move = False
            if print_error:
                print(f"chosen column is full, select a column different than {chosen_column}")
            return (valid_move, chosen_column) #ending
        
        #updating board
        for i in range(len(self.grid) - 1, -1, -1):
            if self.grid[i][chosen_column] == " ":
                self.grid[i][chosen_column] = player_peice
                
                break
        
        return (valid_move, chosen_column)

    
        
    
    
        
        #checks for a win for a player
        #inputs: is_player_x - boolean, true for x, false for o
        #outputs: win - is there a win for this player ; location - grid cords to the connection
    def check_for_win(self, is_player_x, chosen_column, connection_length = 4):
        
        win = False
        location = []
        
        if is_player_x:
            player_peice = "x"
        else:
            player_peice = "o"
                
         
        
        
        
        draw = self.check_for_draw()
        
        while True:
            win, location = self.vertical_wins(chosen_column, player_peice)
            if win:
                break
            win, location = self.horizontal_wins(chosen_column, player_peice)
            if win:
                break
            win, location = self.diagonal_left_wins(chosen_column, player_peice)
            if win:
                break
            win, location = self.diagonal_right_wins(chosen_column, player_peice)
            break
        
        
        
        return win, location, draw
        
          
          
            
    #checks the column for wins
    def vertical_wins(self, chosen_column, player_peice):
        
        current_connection = 0 #connection length
        location = [] #location of win
        for outer, rows in enumerate(self.grid):
            peice = self.grid[outer][chosen_column] #current peice
            
                
            if peice == player_peice: #add 1 to the connection if its the players peice
                current_connection += 1 
                location.append((outer, chosen_column))
            else: #reset if its not the players peice
                current_connection = 0 
                location = []
            
            if current_connection >= 4:
                return (True, location)
            
        return (False, location)




    #checks for player wins on the horizontal row
    def horizontal_wins(self, chosen_column, player_peice):
        
        #finds the row of the peice played
        chosen_row = 0
        for chosen_row, rows in enumerate(self.grid):
            if self.grid[chosen_row][chosen_column] == player_peice:
                break

        
        
        
        current_connection = 0  #connection length
        location = [] #location of the wins
        
        for outer, cols in enumerate(self.grid[chosen_row]): #starts at col 0 and counts along the row
            peice = self.grid[chosen_row][outer] #peice 
            
                
            if peice == player_peice: #if a peice = player peice add 1
                current_connection += 1
                location.append((chosen_row, outer))
            else: #otherwise reset
                current_connection = 0
                location = []
            
            if current_connection >= 4: #4 in a row return true
                return (True, location)
            
        return (False, location)
        
    
    #finds diagonal wins in the direction of the left side (col 0)
    def diagonal_left_wins(self, chosen_column, player_peice):
        
        
        chosen_row = 0
        for chosen_row, rows in enumerate(self.grid):
            if self.grid[chosen_row][chosen_column] == player_peice: #finds the row of the peice
                break
        
        col_dist = chosen_column #distance from chosen_col to col 0  (left side)
        row_dist = chosen_row #distance from chosen_row to row 0 (top)
        if row_dist - col_dist < 0: starting_row = 0 #uses formula to determine the starting row of the diagonal
        else: starting_row = row_dist - col_dist
        
        if col_dist - row_dist < 0: starting_column = 0 #uses formula  to determine the starting col of the diagonal
        else: starting_column = col_dist - row_dist
        #determines how many loops based on which one has the shortest distance from their respective side
        if len(self.grid) - starting_row < len(self.grid[0]) - starting_column: loop = len(self.grid) - starting_row  
        else: loop = len(self.grid[0]) - starting_column
        
        
        current_connection = 0
        location = []
        
        for i in range(loop):
            
            peice = self.grid[starting_row + i][starting_column + i] #from the starting point add one to both to move down diagonaly
            
            
            if peice == player_peice:
                current_connection += 1 
                location.append((starting_row + i, starting_column + i))
            else:
                current_connection = 0
                location = []
            
            if current_connection >= 4:
                return (True, location)
                
        location = []
        return (False, location)
        
        
    #finds diagonal wins in the direction of the right wall (col 6)
    def diagonal_right_wins(self, chosen_column, player_peice):
        
        
        chosen_row = 0
        for chosen_row, rows in enumerate(self.grid):
            if self.grid[chosen_row][chosen_column] == player_peice: #finds row
                break
        
        col_dist = len(self.grid[0]) - chosen_column #distance of chosen column from col 6 (right side)
        row_dist = chosen_row + 1 #distance of chosen row from row 0 (the top)
        if row_dist - col_dist < 0: starting_row = 0
        else: starting_row = row_dist - col_dist
        
        if col_dist - row_dist < 0: starting_column = 6
        else: starting_column = 6 - (col_dist - row_dist)
        #finds the loop amount
        if len(self.grid) - starting_row < starting_column + 1: loop = len(self.grid) - starting_row 
        else: loop = starting_column + 1
        
        
        current_connection = 0
        location = []
        
        for i in range(loop):
            
            peice = self.grid[starting_row + i][starting_column - i]
            
            
            if peice == player_peice:
                current_connection += 1
                location.append((starting_row + i, starting_column - i))
            else:
                
                current_connection = 0
                location = []
            
            if current_connection >= 4:
                return (True, location)
                
        location = []
        return (False, location)
        
        



    #returns a boolean, if the game is in a draw
    def check_for_draw(self):
        #loops the top row
        for peice in self.grid[0]:
            if peice == " ":
                return False
        return True
    
    
    
    
    
    
    def __str__(self):
        retStr = "  " + "-----" * 6 + "-  Row\n" #adds the top line to the board
        
        for index, row in enumerate(self.grid):
            
            rowStr = "| " + " | ".join(row) + " |" #temp string, joined each together with | on each side
            retStr += " | " + rowStr + f" | [{index}]\n" #combine to finish the row and add to ret_string; adds the row number in brackets at the end

                
            #len(self.grid) - 1 - index down to up
            #prints the inbetween spaces. Does not print on the final iteration
            if index < len(self.grid) - 1:
                retStr += " |-" + "-----" * 6 + "|\n"
            
            
        retStr += "  " + "-----" * 6 + "-\n" #adds the bottom line to the board
        
        retStr += "Col " 
        for i in range(len(self.grid[0])):
            #adds the bottom numbers for each column
            retStr += f"[{i}] "
        
        
        
        
        return retStr
        
    def __repr__(self):
        return self.__str__()
