import math
from board_class import board
from ai_class import ai
class game:
    
    def __init__(self):
        self.game_board = board()
    
    def print_game_board(self):
        print(self.game_board)
    
    def clean(self, string):
        return string.strip().lower()
    
    
    
    def start_game(self):
        print(f"---Welcome to connect 4---")
        true_inputs = ["t", "true", "tru", "tr", "yes", "confirm", "yeah", "y", "ye"]
        
        
        x_input = str(input("Enter 't' if you want player X to be ai (press enter for no): "))
        x_ai = self.clean(x_input) in true_inputs
        
        o_input = str(input("Enter 't' if you want player O to be ai (press enter for no): "))
        o_ai = self.clean(o_input) in true_inputs
        

            
        ai_hard_mode = False
        
        if x_ai or o_ai:
            
            diff_input = str(input("Enter 't' if you want ai hardmode activated (press enter for no): "))
            ai_hard_mode = self.clean(diff_input) in true_inputs
 
                    
        input(f"Press enter to Start Game: ")
        board.clear_console()
        self.run_game(x_ai, o_ai, ai_hard_mode)
            
        
        
    def turn(self, is_player_x, chosen_column):
        
        completed_move = self.game_board.place_peice(is_player_x, chosen_column)[0] #trys to place a peice
        win, location, draw = self.game_board.check_for_win(is_player_x, chosen_column) #checks for a win

        return completed_move, win, location, draw #returns if the move is valid, if the player won, and the location of the win
        
    
        #inputs: boolean: is player x an ai, boolean: is player o an ai, boolean: is the ai on hard mode
    def run_game(self, x_ai = False, o_ai = False, ai_hard_mode = False):
        
        if x_ai:
            x_ai_player = ai(True, ai_hard_mode)
        if o_ai:
            o_ai_player = ai(False, ai_hard_mode)
            
            
        
        winning_peice = "" #stores the winning peice
        loop = False #loop varrible
        win = False #did a player win yet
        draw = False
        location = [] #location of the connected peices
        x_turn = True #is it the x player's turn
        while not (loop):
            
            print(self.game_board) #prints the current state of the game board
            print("\n")

            if x_turn: #x_turn
                x_turn = False #set var to false for o turn
                
                
                if x_ai: #if x is an ai
                    sucessful_move = False
                    sucessful_move, win, location, draw  = self.turn(True, x_ai_player.find_move(self.game_board.ret_grid()))
                    
                    if win: #sets the winning peice
                        winning_peice = "x"
                    
                    if draw: #checks for a draw
                        loop = True
                        break
                         
                    loop = win #once a player wins break the loop by setting loop to true                    
                    
                    
                
                else: #human player
                    completed_move = False #loop will continue until the inputed move is valid, or -1 is typed to end the game
                    while not(completed_move):
                        try:
                            #player input, gets a column
                            chosen_column = int(input("Player 1 (x), input a column [0 - 6] "))
                            
                            if chosen_column == -1: #exit, inputed -1
                                loop = True
                                break
                            #finds if the move was executed, if the player won and the location of the win
                            completed_move, win, location, draw = self.turn(True, chosen_column)
                            
                            
                            if draw:
                                loop = True
                                break
                            
                            if win: #sets the winning peice
                                winning_peice = "x"
                                
                            loop = win #sets loop to true once a win to end the loop
                            
                        except ValueError: #prevents an error if the user inputs the incorrect data type
                            
                            print("input must be an interger in the range 0 - 6")
                    
                            
            else: #o turn
                x_turn = True
                
                if o_ai: #if o is an ai
                    sucessful_move = False
                    sucessful_move, win, location, draw = self.turn(False, o_ai_player.find_move(self.game_board.ret_grid()))
                    
                    if win: #sets the winning peice
                        winning_peice = "o"
                    
                    if draw: #checks for a draw
                        loop = True
                        break         
                    
                    loop = win                    

                    
                else: #human player for o
                    completed_move = False
                    while not(completed_move): #continues until the user makes a valid move
                        try:
                            #player input, gets a column
                            chosen_column = int(input("Player 2 (o), input a column [0 - 6]: "))
                            
                            if chosen_column == -1: #exit, inputed -1
                                loop = True
                                break
                            #same as x ^
                            completed_move, win, location, draw = self.turn(False, chosen_column)
                            
                            if draw: #checks for a draw
                                loop = True
                                break                            
                            
                            if win: #sets winning peice
                                winning_peice = "o"
                                
                            loop = win
                            
                        except ValueError: #prevents an error for an incorrect data type
                            print("input must be an interger in the range 0 - 6")
                    
                        
                        
            
            if o_ai and x_ai:
                input("\npress enter to move on to the next move: ")
            board.clear_console() #clears the console
        
        
        board.clear_console()
        print(self.game_board)
        
        if win:
            print(f"\n{winning_peice} wins the game with a connection on [{location[0]}, {location[1]}, {location[2]}, {location[3]}]")
        elif draw:
            print("Tie, no winner")
        else:
            print("Game ended, no winner")



    #pits an ai vs an ai player, alowes user to veiw specific data about the game
    #(number of games = int, x_hard_move = boolean, x_path_len = int, o_hard_mode = boolean, o_path_len = int)
    def ai_game(self, num_of_games = 1,  x_hard_mode = True, x_path_len = 4, o_hard_mode = True, o_path_len = 4):
        #limits path length, so that it doesnt break
        if x_path_len > 6:
            x_path_len = 6
            print("path_len cannot be greater than 6")
        if o_path_len > 6:
            o_path_len = 6
            print("path_len cannot be greater than 6")
        #creates ai objects
        
        
        x_ai_player = ai(True, x_hard_mode, x_path_len)
        o_ai_player = ai(False, o_hard_mode, o_path_len)
        #counts wins for each player
        x_win_count = 0
        o_win_count = 0
        draw_count = 0
        #lists saving the stats for each game
        winning_peice_each_game = [] #saves the winning peice
        final_boards = [] #final board state to load the game back
        locations_of_wins = [] #saves the cords for each win
        amount_of_moves = [] #saves the number of moves for the game
    
        bar_length = 25 #length of the loading bar
        
        for i in range(num_of_games): #main loop 
        
            
            #gets the loading bar
            loading_bar = self.get_bar(bar_length, num_of_games, i)
            print(f"loading - {i}/{num_of_games} finished . . . ")  
            print(loading_bar)
            
            moves = 0
            winning_peice = "" #stores the winning peice
            win = False #did a player win yet
            draw = False
            loop = False
            location = [] #location of the connected peices
            x_turn = True #is it the x player's turn
            while not(loop): #game loop
        
                if x_turn:
                    x_turn = False # alternates
                    sucessful_move, win, location, draw  = self.turn(True, x_ai_player.find_move(self.game_board.ret_grid()))  #ai move from ai object
                    moves += 1
                    
                    
                    if draw: #ends if there is a draw
                        loop = True
                
                    if win: #if there a win end and set winning peice
                        winning_peice = "x"
                        loop = True
                else:
                    x_turn = True #alternates
                    sucessful_move, win, location, draw  = self.turn(False, o_ai_player.find_move(self.game_board.ret_grid())) #ai move from ai object
                    moves += 1

                    if draw: #ends: draw
                        loop = True
        
                    if win:#ends sets winning peice
                        winning_peice = "o"
                        loop = True
            if draw: #adds to draw count
                draw_count += 1
                
            
            if win: #adds to specific peice win count
                if winning_peice == "x":
                    x_win_count += 1  
                else:
                    o_win_count += 1
            #updates the lists: data collection
            winning_peice_each_game.append(winning_peice)
            amount_of_moves.append(moves)
            final_boards.append(board(self.game_board.ret_grid_copy()))
            locations_of_wins.append(location)
            
            self.game_board.clear_board() #clears the board object for the next game
            board.clear_console()
            

            
        
        #analising data
        loading_bar = self.get_bar(bar_length, num_of_games, num_of_games)
        print(f"done loading - {num_of_games}/{num_of_games} finished")
        print(loading_bar)
        print("---All games completed---") 
        while True:
            
            print(f"x/o/d: {x_win_count}/{o_win_count}/{draw_count}")
            selection = input("enter (1) for statistics, enter (2) to look at specific games (-1 to escape): ") #user selects what to veiw
            if selection == "-1":
                break
            
            if selection == "1":
                total_moves, avg_turn_per = self.calc_moves(amount_of_moves, num_of_games)
                print(f"\nOut of {num_of_games} Games;")
                print(f"{(draw_count/num_of_games) * 100}% of games ended in a draw.")
                print(f"X won {self.calc_win_percentage(x_win_count, o_win_count, draw_count)}% of Games.")
                print(f"O won {self.calc_win_percentage(o_win_count, x_win_count, draw_count)}% of Games.")
                print(f"There was an average of {avg_turn_per} turns per game. \n")
                
                input("enter to clear: ")
                board.clear_console()
            
            else:
                board_index = -9999
                while not(board_index >= 0 and board_index < len(final_boards)):
                    try:
                        print("\nTo search indexes for x/o/d enter -1/-2/-3: ")
                        board_index = int(input(f"Enter a index for a specific game in the range [{0}, {len(final_boards) - 1}]: "))
                        
                        
                        
                        
                        if board_index == -3:
                            draw_index = []
                            for index, winner in enumerate(winning_peice_each_game):
                                if winner == "":
                                    draw_index.append(index)
                            print("Index locations for draws: ", draw_index)
                        
                        if board_index == -2:
                            o_index = []
                            for index, winner in enumerate(winning_peice_each_game):
                                if winner == "o":
                                    o_index.append(index)
                            print("Index locations for o wins: ", o_index)
                            
                        if board_index == -1:
                            x_index = []
                            for index, winner in enumerate(winning_peice_each_game):
                                if winner == "x":
                                    x_index.append(index)
                            print("Index locations for x wins: ", x_index)
                        
                                                    
                                                                
                            
                    except ValueError:
                        continue
                print(f"\n-----Game {board_index}-----\n")
                print(final_boards[board_index])
                
                if winning_peice_each_game[board_index] == "":
                    print(f"\nNo winner, Draw")
                    
                else:
                    print(f"\n{winning_peice_each_game[board_index]} won the game at the location ", end = "")
                    print(locations_of_wins[board_index], ".")
                    
                print(f"There was total of {amount_of_moves[board_index]} moves this game.")
                input("enter to clear: ")
                board.clear_console()
    
    
    
    
    
    
    
    def calc_moves(self, total_moves, total_games):
        move_count = 0
        for moves in total_moves:
            move_count += moves
        
        return move_count, (move_count/total_games)
        
    
    
    
        
    def calc_win_percentage(self, player_1_wins, player_2_wins, draws = 0):
        return ((player_1_wins / (player_1_wins + player_2_wins + draws)) * 100)
     
        
    #makes the loading bar based on the progress of the simulation
    def get_bar(self, bar_length, total_games, finished_games):
        
        games_per_bar = total_games / bar_length
        
        
        if total_games == finished_games:
            finished_bars = bar_length
        else:
            finished_bars = math.ceil(finished_games / games_per_bar)
            
            
        loading_bar = "|" + ("=" * finished_bars)
        loading_bar += ("-" * (bar_length - finished_bars)) + "|"
        
        
        return loading_bar
        




#f
