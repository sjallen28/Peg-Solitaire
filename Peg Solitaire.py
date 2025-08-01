# %% [markdown]
# # User Guide
# ### How to start
# To start the program run all cells in order, the last cell will then display the user interface to play
# 
# ### How to Play
# In peg solitaire the goal is to move the pegs around the board until there is one peg left in the middle
# 
# ### Text commands
# Menu - Returns you to the menu
# Save - Allows you to save your moves as a text file
# Reset - Resets the board to the starting state
# Solve - Tries to automatically solve the game from where you left off
# Undo(opt) - Undoes the last move you made
# Help - Brings up this menu in case you forget
# 
# ### Moving Pegs
# Pegs are selected one at a time, using the coordinate
# system labelled. The coordinates are inputed with the
# LETTER followed by NUMBER (moves are not case sensitive)
# e.g. D2,F7,c3...

# %%
import sys
import random
from tkinter import *
from tkinter import ttk
from IPython.display import clear_output
from pathlib import Path
import time
import numpy as np


# %%
class Peg:
    """
    A class that represents any of the possible coordinates on the board
    
    ...
    
    Attributes
    ----------
    peg_type : str
        Describes what object is occcupying a specific coordinate.
    form : str
        Determines what is printed for each peg_type on the board.
    free : bool
        Determines whether or not a peg can land in this coordinate.
    bin_id : int
        Determines how are peg types represented when converted to binary.      
    
    """
    def __init__(self, peg_type):
        """
        Constructs all attributes for the different objects a coordinate can
        hold.

        Parameters
        ----------
        peg_type : str
            Describes what object is occcupying a specific coordinate.

        Returns
        -------
        None.

        """
        self.peg_type = peg_type

        if self.peg_type == "null" :
            self.form = " "
            self.free = False
            self.bin_id = 0

        elif self.peg_type == "empty":
            self.form = "O"
            self.free = True
            self.bin_id = 0

        elif self.peg_type =="peg":
            self.form = "V"
            self.free = False
            self.bin_id = 1


    def __repr__(self):
        """
        Makes the objects become represented by their form attribute.

        Returns
        -------
        form : str
            Determines what is printed for each peg_type on the board.
        """
        return self.form

# %%
#Creates objects to fill the board with.
n = Peg("null")
e = Peg("empty")
p = Peg("peg")

#Creates list to keep track of what cheats are on/off.
ANY_DIST = 0
UNDO_OPT = 1
ALT_BOARD =2
cheats = np.array([False,False,False])

# %%
class Selected(Exception):
    """
    A class made that can break some while loops if user inputs are
    satisfactory.
        
    """

# %%
def init_board():
    """
    Resets the board to  its initial state

    Returns
    -------
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes

    """

    if cheats[ALT_BOARD] == True:
        board = np.array([
            ["  ","A", "B", "C", "D", "E", "F", "G"],
            [ 1 ,  n ,  n ,  p ,  p ,  p ,  n ,  n ],
            [ 2 ,  n ,  p ,  p ,  p ,  p ,  p ,  n ],
            [ 3 ,  p ,  p ,  p ,  p ,  p ,  p ,  p ],
            [ 4 ,  p ,  p ,  p ,  e ,  p ,  p ,  p ],
            [ 5 ,  p ,  p ,  p ,  p ,  p ,  p ,  p ],
            [ 6 ,  n ,  p ,  p ,  p ,  p ,  p ,  n ],
            [ 7 ,  n ,  n ,  p ,  p ,  p ,  n ,  n ]
            ])
    else:
        board = np.array([
            ["  ","A", "B", "C", "D", "E", "F", "G"],
            [ 1 ,  n ,  n ,  p ,  p ,  p ,  n ,  n ],
            [ 2 ,  n ,  n ,  p ,  p ,  p ,  n ,  n ],
            [ 3 ,  p ,  p ,  p ,  p ,  p ,  p ,  p ],
            [ 4 ,  p ,  p ,  p ,  e ,  p ,  p ,  p ],
            [ 5 ,  p ,  p ,  p ,  p ,  p ,  p ,  p ],
            [ 6 ,  n ,  n ,  p ,  p ,  p ,  n ,  n ],
            [ 7 ,  n ,  n ,  p ,  p ,  p ,  n ,  n ]
            ])

    return board

# %%
def show_board(board):
    """
    Prints the board with correct formatting.

    Parameters
    ----------
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes

    Returns
    -------
    None.

    """
    output = str(board[1:]).replace('[','').replace(']','').replace('"','')
    print(*board[0],' ')
    print('',output)

# %%
def menu():
    """
    Displays all options for the user to interact with.

    Returns
    -------
    None.

    """
    #Resets the board,board records and kernel
    board = init_board()
    board_rec= []

    while True:
        clear_output()
        
        print("")
        print("WELCOME TO PEG SOLITAIRE!")
        print("")
        print("1-Play Game")
        print("2-Load in Solution")
        print("3-Cheat menu")
        print("4-Advanced Interface")
        print("5-Autosolve")
        print("6-How to play")
        print("7-Quit")
        print("")
        menu_opt = input("Please select a number from 1-7:")
        print("")

        if menu_opt=="1":
            play_game(board,board_rec)

        elif menu_opt=="2":
            load_sol(board,board_rec)

        elif menu_opt=="3":
            cheat_menu()

        elif menu_opt =="4":
            adv_int(board,board_rec)

        elif menu_opt=="5":
            auto_solve(board,board_rec)

        elif menu_opt=="6":
            how_to(board)

        elif menu_opt=="7":
            sys.exit("Bye")

        else:
            print("Please type the number corresponding to your desired\
choice")
            print("")

# %%
def play_game(board, board_rec, move_rec = []):
    """
    Initiates code that allows the user to manually play peg solitaire.

    Parameters
    ----------
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.

    Returns
    -------
    None.

    """
    clear_output(wait=True)
    show_board(board)
    time.sleep(.2)

    while True:
        #Checks to see if winning condition is fulfilled.
        if np.count_nonzero(board == p)==1 and board[4,4] == p :
            print("Congratulations!! You won!!")
            time.sleep(.2)
            break

        #Only keeps a record of previous board states if undo is on.
        if cheats[UNDO_OPT] == True:
            board_rec.append(np.copy(board))
        
        #Calls functions to select pegs and move them.
        coords_to, coords_from, diff, tot_input = user_input(board,move_rec,
                                                             board_rec)
        movement(coords_to,coords_from,diff,board)
        
        #Keeps a record of all moves for the user to save.
        move_rec.append(tot_input)

        clear_output(wait=True)
        show_board(board)

        #Calculates if losing condition has been fulfilled.
        move_count = moves_left(board)
        print("Moves availiable:", move_count)
        if move_count==0:
            print("Sorry you lost :(")
            break


    
    choice = str(input("Do you want to save your choices before\
returning to the menu? Y/N")).upper()
    print(choice, type(choice))
    time.sleep(3)
    if choice == "Y":
        time.sleep(1)
        save_file = input("Name save file:")
        np.savetxt(save_file+'.txt',move_rec,fmt='%s')
        print(f"{save_file}.txt saved")
        menu()
    else:
        menu()


def user_input(board, move_rec, board_rec):
    """
    Provides interface for user to input coordinates and calls the necessary
    functions to check the input is allowed.

    Parameters
    ----------
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.
    move_rec : list
        A list that keeps contains the coordinates of all successful moves
        taken.
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.

    Returns
    -------
    coords_to : numpy.ndarray
        An array containing the selected destination coordinates for a peg.
    coords_from : numpy.ndarray
        Array containing the coordinates for the selected peg to move
    diff : list
        Contains the distance between coords_from and coords_to.
    tot_input : str
        Provides the string coordinates inputted by the user to be recorded 
        for saving.

    """
    try:
        while True:

            try:
                while True:

                    try:
                        while True:

                            #Asks for user input and checks input is valid.
                            time.sleep(.2)
                            input_from = str(
                            input("What peg do you want to move?")).upper()
                            text_opts(input_from, False,board,
                                      move_rec, board_rec)
                    except Selected:
                        print(f"{input_from} selected")

                    #Asks for where the peg should go and checks if the 
                    #user input is valid again.
                    input_to = str(
                        input("Where do you want to move the peg?")).upper()
                    text_opts(input_to,True,board,move_rec,board_rec)
            except Selected:
                #Converts the string coords into integers for indexing.
                coords_from = np.array([
                    np.where(board == int(input_from[1]))[0][0],
                    np.where(board == input_from[0])[1][0]])
                coords_to = np.array([
                    np.where(board == int(input_to[1]))[0][0],
                    np.where(board == input_to[0])[1][0]])

            diff = (coords_to-coords_from)[coords_to-coords_from != 0]
            move_check(diff)
    except Selected:
        tot_input = input_from+input_to

    return coords_to, coords_from, diff, tot_input

# %%
def load_sol(board,board_rec):
    """
    Allows user to input a solution text file and carry out the moves provided.
    Once the moves have been undertaken, control is given to the user to keep
    playing.
    
    Parameters
    ----------
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.

    Returns
    -------
    None.

    """
    file = input("What is the name of the soultion file?")
    try:
        solution_arr = np.array([np.loadtxt(f'C:/Users/User/{file}.txt',
                                           dtype = 'str', delimiter=',')])
    except:
        print(f"{file}.txt was not found")
        print("")
        print("Returning to menu...")
        print("")
        print("")
        menu()

    solution = solution_arr[0]

    for i in range(0,np.size(solution)):
        clear_output(wait=True)
        show_board(board)
        time.sleep(.2)
        #Only keeps a record of previous board states if undo is on.
        if cheats[UNDO_OPT] == True:
            board_rec.append(np.copy(board))

        #Checks that each step has a pair of moves
        if len(solution[i])!=4:
            print(f"Step {i+1} was invalid")
            menu()
            print("")
            print("Returning to menu...")
            print("")
            print("")

        
        peg_from = (solution[i][0]+solution[i][1]).upper()
        peg_to = (solution[i][2]+solution[i][3]).upper()

        #This block runs the to and from coordinates through the
        #peg check function, to verify inputs are correct.
        try:
            unselected = peg_check(peg_from,False,board)
            if unselected == True:
                print(f"Step {i+1} was invalid")
                print("")
                print("Returning to menu...")
                print("")
                print("")
                menu()
        except Selected:
            try:
                unselected = peg_check(peg_to,True,board)
                if unselected == True:
                    print(f"Step {i+1} was invalid")
                    print("")
                    print("Returning to menu...")
                    print("")
                    print("")
                    menu()
            except Selected:
                pass

        #Converts the string coords into integers for indexing.
        coords_from = np.array([
            np.where(board == int(peg_from[1]))[0][0],
            np.where(board == peg_from[0])[1][0]])
        coords_to = np.array([
            np.where(board == int(peg_to[1]))[0][0],
            np.where(board == peg_to[0])[1][0]])
        diff = (coords_to-coords_from)[coords_to-coords_from != 0]
        
        #Checks the movement between coordinates follows the rules.
        try:
            if move_check(diff) == True:
                print("Solution file contains invalid moves")
                print("")
                print("Returning to menu...")
                print("")
                print("")
                menu()

        except Selected:
            movement(coords_to,coords_from,diff, board)

    #Allows the user to play from where the file ended.
    play_game(board,board_rec,solution.tolist())

# %%
def cheat_menu():
    """
    Provides a secondary menu for the user to alter the base rules

    Returns
    -------
    None.

    """
    
    while True:
        clear_output()
        print("||Cheat Menu||")
        print("")
        print(f"1-Move pegs any distance - {cheats[ANY_DIST]}")
        print(f"2-Undo - {cheats[UNDO_OPT]}")
        print(f"3-Alternate Board - {cheats[ALT_BOARD]}")
        print("4-Change what the pegs looks like")
        print("5-Return to Main Menu")
        print("")
        cheat_opt = int(input("Select an option here:"))

        if cheat_opt ==5:
            menu()
        elif cheat_opt ==4:
            p.form = input("What character do you want the\
peg to be displayed as? ")

        elif 0<cheat_opt<4:
            #Toggles cheats 1-3 on and off.
            cheats[cheat_opt-1] = not cheats[cheat_opt-1]
            clear_output()
        else:
            print("Invalid choice: please input a number from 1-5")

# %% [markdown]
# # Preface for using GUI
# #### To use the advanced interface it is important that the Photoimage file directories are altered for wherever you have stored the file

# %%
def adv_int(board,board_rec):
    """
    Constructs a graphical user interface(GUI) representation of the peg
    solitaire board.

    Parameters
    ----------
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.

    Returns
    -------
    None.

    """
    #Creates external window
    root = Tk()
    root.title("Peg Solitaire")
    base_dir = Path(__file__).resolve().parent
    print(base_dir)
    #Loads in all necessary images for the buttons.
    global PEG_IMG
    global EMPTY_IMG
    PEG_IMG = PhotoImage(file = base_dir/'sprites'/'peg.png')
    EMPTY_IMG = PhotoImage(file = base_dir/'sprites'/'empty.png')
    undo_img = PhotoImage(file = base_dir/'sprites'/'undo.png')
    reset_img  = PhotoImage(file = base_dir/'sprites'/'reset.png')
    reset_img  = PhotoImage(file = base_dir/'sprites'/'reset.png')
    menu_img  = PhotoImage(file = base_dir/'sprites'/'menu.png')

    #Creates a frame and grid for buttons to be placed into.
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.iconphoto(False,PEG_IMG)

    buttons = [[],[],[],[],[],[],[]]
    coords = []
    board = init_board()
    board_rec.append(np.copy(board))

    #Runs through the board and adds a button for each peg/empty in it.
    #The buttons are all appended to the list 'Buttons' so they can be
    #modified later on.
    for i in range(7):
        for j in range(7):
            try:
                if board[i+1,j+1] == p:
                    space = ttk.Button(mainframe, image = PEG_IMG,
                                       command=lambda i=i,j=j:
                                           select(i,j,
                                                  board,board_rec,
                                                  buttons,coords))

                    space.grid(column = j, row = i)
                    buttons[i].append(space)

                elif board[i+1,j+1] == e:
                    space = ttk.Button(mainframe, image = EMPTY_IMG,
                                       command=lambda i=i,j=j:
                                           select(i,j,
                                                  board,board_rec,
                                                  buttons,coords))
                    space.grid(column = j, row = i)
                    space.config(state = 'disabled')
                    buttons[i].append(space)

                else:
                    space = 0
                    buttons[i].append(space)
            except:
                pass

    #Creates and places buttons for the undo, reset and menu function.
    undo_butt = ttk.Button(mainframe, image = undo_img, command=lambda:
                           undo(board,coords,board_rec, buttons , vis =True))
    undo_butt.grid(column = 7,row= 0, rowspan = 2)

    reset_butt = ttk.Button(mainframe, image = reset_img, command=lambda:
                            reset_vis(board, board_rec,buttons,coords))
    reset_butt.grid(column = 7,row= 2, rowspan = 2)

    menu_butt = ttk.Button(mainframe, image = menu_img, command=root.destroy)
    menu_butt.grid(column = 7,row=4, rowspan = 2)

    #Keeps the window active
    root.mainloop()

    #Once the window is destroyed, the user is returned to the menu.
    menu()


def select(i,j ,board, board_rec, buttons, coords):
    """
    When a button is pressed this function highlights any potential moves,
    disables any immovable positions and returns the new board once pegs 
    have been moved.

    Parameters
    ----------
    i : int
        Index of row on the board.
    j : int
        Index of column on the board.
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.
    buttons : list
        A list containing the identification and location of all buttons made.
    coords : list
        A list of the coordinates of all successful moves.

    Returns
    -------
    None.

    """

    coords.append([i+1,j+1])
    move_num = len(coords)/2

    #This block allows the user to click on the button that was just selected
    # to deselect it and remove it from the move records.
    if len(coords)%2 == 0:
        if coords[-1] == coords[-2]:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i,j] == e:
                        buttons[i-1][j-1].config(image = EMPTY_IMG,
                                                 state="disabled")
                    elif board[i,j] == p:
                        buttons[i-1][j-1].config(image = PEG_IMG,
                                                 state="enabled")
            coords[:] = coords[:-2]

            return

    #This runs if there is a full set of coordinates for a peg to be moved
    #from point A to B.
    if move_num%1 == 0:
        coords_from = np.asarray(coords[-2])
        coords_to = np.asarray(coords[-1])

        diff = (coords_to-coords_from)[coords_to-coords_from != 0]
        movement(coords_to,coords_from,diff,board, buttons)
        board_rec.append(np.copy(board))

        #Enables all buttons on the board.
        for butt_row in buttons:
            for button in butt_row:
                if button !=0:
                    button.config(state="enabled")

        #Disables any buttons where there is no peg.
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i,j] == e:
                    buttons[i-1][j-1].config(state="disabled")

    #Runs when a peg has been selected.
    else:
        pos_moves = moves_left(board, find_move=True)

        #Creates a list of all buttons which the selected peg can move to.
        buttons_on = []
        buttons_on.append(buttons[i][j])
        for as_button in pos_moves:
            button_from = buttons[as_button[0][0]-1][as_button[0][1]-1]
            if button_from == buttons[i][j]:
                buttons_on.append(buttons[as_button[1][0]-1]\
                                  [as_button[1][1]-1])

        #Enables only these locations and disables all other buttons.
        for butt_row in buttons:
            for button in butt_row:
                if button in buttons_on:
                    button.config(state="enabled")
                elif button == 0:
                    pass
                else:

                    button.config(state="disabled")


def reset_vis(board, board_rec,buttons,coords):
    """
    Resets the visual element of the board for the advanced user interface.

    Parameters
    ----------
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.
    buttons : list
        A list containing the identification and location of all buttons made.
    coords : list
        A list of the coordinates of all successful moves.

    Returns
    -------
    None.

    """
    board[:,:] = init_board()
    board_rec[:] = []
    coords[:] = []
    
    #Resets the buttons to their original state.
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i,j] == e:
                buttons[i-1][j-1].config(image = EMPTY_IMG, state="disabled")
            elif board[i,j] == p:

                buttons[i-1][j-1].config(image = PEG_IMG, state="enabled")

# %%
def auto_solve(board, move_rec =[]):
    """
    Runs through all potential moves, blacklisting any moves that lead to dead-
    ends or boards that are symmetrically congruent to other deadends.

    Parameters
    ----------
    board : numpy.ndarray
        A 2D array that stores information on each space on the boards status
    move_rec : list, optional.
        A list that keeps contains the coordinates of all successful moves
        taken. The default is [].

    Returns
    -------
    None.

    """
    #Creates an empty lists to store blacklisted moves and binary identifiers
    #for deadend boards.
    bad_moves = []
    dead_ends = []

    #Empty list to store all successful board states and appends the starting
    #board.
    board_rec = []
    board_rec.append(np.copy(board))

    while True:
        #Checks first if the boards has satisfied winning conditions.
        if np.count_nonzero(board == p)==1 and board[4,4] == p :
            for i in range(len(board_rec)):
                clear_output(wait = True)
                print("Solution found:")
                show_board(board_rec[i])
                time.sleep(.5)
            break

        #This block converts the board into a binary sequence for each
        #potential orientation and reflection to account for all symmetrical
        # boards which would also lead to deadends.
        bin_boards = gen_boards(board)
        for binary in range(len(bin_boards)):
            if bin_boards[binary] in dead_ends:
                bad_moves.append([len(board_rec)-1,move_rec[-1]])
                undo(board,move_rec,board_rec)

        #This block sorts through the list of bad_moves and removes any moves
        #that are now inaccessible due to an earlier board being blacklisted.
        if len(bad_moves)>1:
            board_num=[]

            for i in bad_moves:
                board_num.append(i[0])
            while board_num != sorted(board_num):
                board_num=[]
                before = [0]
                for i in bad_moves:
                    board_num.append(i[0])
                    if before[0]>i[0]:
                        bad_moves.remove(before)
                    before = i

        pos_moves = moves_left(board,find_move = True)#Finds all potential moves.

        #This block removes any moves from the possible moves generated that
        #have already been blacklisted by bad_moves.
        to_remove = []
        for move in range(len(pos_moves)):
            if [len(board_rec),pos_moves[move]] in bad_moves:
                to_remove.append(pos_moves[move])
        for remove in to_remove:
            pos_moves.remove(remove)

        #If there are still moves that can be made, the code will then execute
        #necessary functions to modify the board accordingly and recorde the
        #new state of the board
        if len(pos_moves) !=0:

            next_move = random.choice(pos_moves)
            move_rec.append(next_move)
            coords_from  =np.asarray(next_move[0])
            coords_to = np.asarray(next_move[1])

            diff = (coords_to-coords_from)[coords_to-coords_from != 0]
            movement(coords_to,coords_from,diff,board)
            board_rec.append(np.copy(board))

        #If there are no moves left at all then the program tells the user so.
        #This is used for if auto_solve() is called mid game as there will be
        #solutions otherwise.
        elif len(pos_moves) ==0 and len(board_rec)<2:
            print("No possible solution")
            break
        #If there are no possible moves for this board state, the move to reach
        #this board and the boards binary identifier are blacklisted and the
        #board is reverted to the previous step.
        else:
            bad_moves.append([len(board_rec)-1,move_rec[-1]])
            undo(board,move_rec,board_rec)
            dead_ends.append(min(bin_boards))
    play_game(board, board_rec, move_rec)


def gen_boards(board):
    """
    Generates a lsit of eight binary strings representing the current board
    from all possible rotations and reflections.

    Parameters
    ----------
    board : numpy.ndarray
        A 2D array that stores information on each space on the boards status

    Returns
    -------
    binary : list
        A list containing binary strings representing the board from all
        rotations and reflections.

    """
    binary = []#Create empty list to store all the binary identifiers.
    boards = [board[1:,1:]]#Creates list to store all versions of the board.

    #This loop appends numpy arrays of the same board in different rotations
    #and reflections
    for i in range(6):
        if i ==3:
            boards.append(np.flip(boards[0], axis=1))
        boards.append(np.rot90(boards[-1]))

    #This loop converts each of the boards into binary by accessing each pegs
    #attribute labelling it in binary.
    for board in boards:
        new_bin = []
        list_board = np.concatenate((board))
        for i in list_board:
            new_bin.append(str(getattr(i,"bin_id")))
        new_bin = "".join(new_bin)
        binary.append(new_bin)

    return binary

# %%
def how_to(board):
    """
    Outputs the rules of peg solitaire

    Parameters
    ----------
    board : numpy.ndarray
        A 2D array that stores information on each space on the boards status

    Returns
    -------
    None.

    """
    clear_output()
    goal = np.array([
                ["  ","A", "B", "C", "D", "E", "F", "G"],
                [ 1 ,  n ,  n ,  e ,  e ,  e ,  n ,  n ],
                [ 2 ,  n ,  n ,  e ,  e ,  e ,  n ,  n ],
                [ 3 ,  e ,  e ,  e ,  e ,  e ,  e ,  e ],
                [ 4 ,  e ,  e ,  e ,  p ,  e ,  e ,  e ],
                [ 5 ,  e ,  e ,  e ,  e ,  e ,  e ,  e ],
                [ 6 ,  n ,  n ,  e ,  e ,  e ,  n ,  n ],
                [ 7 ,  n ,  n ,  e ,  e ,  e ,  n ,  n ]
                ])
    print("==================RULES==================")

    print(f"In peg solitaire the goal is to move the pegs, {p.form}")
    print("around the board:")
    show_board(board)
    print("Until there is one peg left in the middle:")
    show_board(goal)
    print("Pegs can only be moved by jumping over another peg and")
    print(f"into an empty space, {e.form}. The peg that is jumped over is")
    print("then removed from the board.")
    print("Pegs are selected one at a time, using the coordinate ")
    print("system labelled. The coordinates are inputed with the")
    print("LETTER followed by NUMBER (moves are not case sensitive)")
    print(" e.g. D2,F7,c3...")
    help_menu()

    
    leave_menu = input("enter anything to return to menu. ")
    menu()


def help_menu():
    """
    Prints all available text inputs the user can do.

    Returns
    -------
    None.

    """
    print("")
    print("==============TEXT OPTIONS===============")
    print("Menu - Returns you to the menu")
    print("Save - Allows you to save your moves as a text file")
    print("Reset - Resets the board to the starting state")
    print("Solve - Tries to automatically solve the game from where you left off")
    print("Undo(opt) - Undoes the last move you made")
    print("Help - Brings up this menu in case you forget")
    print("")

# %%
def text_opts(text,destination,board,move_rec, board_rec=[]):
    """
    Checks users input for any of the text based options available.

    Parameters
    ----------
    text : str
        The users input.
    destination : bool
        Determines the output of function based on if the peg is selecting 
        what peg to move or where to move a peg.
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.
    move_rec : list
        A list that keeps contains the coordinates of all successful moves
        taken.
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.

    Returns
    -------
    None.

    """
    if text == "MENU":
        menu()

    elif text == "SAVE":
        print("hey")
        save_file = input("Name save file:")
        np.savetxt(save_file+'.txt',move_rec,fmt='%s')
        print(f"{save_file}.txt saved")
        return

    elif text == "RESET":
        board[:,:] = init_board()
        show_board(board)
        return

    elif text == "SOLVE":
        auto_solve(board, move_rec)

    elif text == "UNDO":
        if cheats[UNDO_OPT] == True:
            undo(board,move_rec,board_rec)
            show_board(board)
            return

        print("Undo is disabled, enable it via the cheats menu")

    elif text == "HELP":
        help_menu()
        return

    else:
        peg_check(text,destination,board)
        return


def peg_check(peg,destination,board):
    """
    Checks users input to make sure that it is in the valid format.

    Parameters
    ----------
    peg : str
        String of the coordinates the user selected
    destination : bool
        Determines the output of function based on if the peg is selecting 
        what peg to move or where to move a peg.
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.

    Raises
    ------
    Selected
        Raised if the input passes the necessary checks

    Returns
    -------
    None.

    """
    if len(peg)>2 or len(peg)<=1 :
        print("Input must be 2 characters long. eg. A3,F6...")
        print("")
        return True

    if ord(peg[0]) < 65 or 71 < ord(peg[0]):
        print("First coordinate must be from A-G")
        print("")
        return True

    if ord(peg[1]) < 49 or 56 < ord(peg[1]):
        print("Second coordinate must be between 1-7")
        print("")
        return  True

    peg_obj = board[np.where(board == int(peg[1]))[0][0],
                    np.where(board == peg[0])[1][0]]

    #Checks to see if the peg check is for the start or end spot.
    if destination == True:
        #Checks that the end spot is empty.
        if peg_obj.free is False:
            print("Cannot jump here")
            print("")
            return True

        raise Selected

    if peg_obj.free is False and peg_obj == p:
        raise Selected

    print("There is no peg here")
    print("")
    return True


def move_check(diff):
    """
    Checks the pegs movement is allowed withing the rules.

    Parameters
    ----------
    diff : list
        Contains the distance between coords_from and coords_to.        

    Raises
    ------
    Selected
        Raised if the input passes the necessary checks

    Returns
    -------
    None.

    """
    #Makes sure the vector is 1-dimensional.
    if len(diff) != 1: 
        print("Pegs cannot move diagonally")
        print("")
        return


    if cheats[ANY_DIST] == False:

        if abs(diff[0]) > 2:
            print("The peg can only jump over 1 peg at a time")
            return

        if abs(diff[0]) < 2:
            print("Pegs must jump over a peg to be moved")
            return


        raise Selected

    raise Selected

# %%
def movement(coords_to,coords_from,diff,board, buttons = 0):
    """
    Modifys the board to account for the pegs movement.

    Parameters
    ----------
    coords_to : numpy.ndarray
        An array containing the selected destination coordinates for a peg.
    coords_from : numpy.ndarray
        Array containing the coordinates for the selected peg to move.
    diff : list
        Contains the distance between coords_from and coords_to. 
    board : numpy.ndarray
        Numpy array containing coordinates and peg classes.
    buttons : list, optional
        A list containing the identification and location of all buttons made.

    Returns
    -------
    None.

    """
    row = 0
    col = 1

    #Changes the end spot to a peg for the base and advanced interface.
    board[coords_to[row],coords_to[col]] = p
    if isinstance(buttons, list):
        buttons[coords_to[row]-1][coords_to[col]-1].config(image = PEG_IMG)

    #Deteremines if the vector is positive or negative.
    step = diff[0]/abs(diff[0])

    #Removes any pegs that are jumped over if the peg was moved horizontally.
    if coords_from[row] == coords_to[row]:
        for i in range(abs(diff[0])):
            board[coords_from[row],coords_from[col]+int((i*step))] = e
            if isinstance(buttons, list):
                buttons[coords_from[row]-1]\
                [coords_from[col]-1+int((i*step))].config(image = EMPTY_IMG)

    #Removes any pegs that are jumped over if the peg was moved vertically.
    else:
        for i in range(abs(diff[0])):
            board[coords_from[row]+int((i*step)),coords_from[col]] = e
            if isinstance(buttons, list):
                buttons[coords_from[row]-1+int((i*step))]\
                [coords_from[col]-1].config(image = EMPTY_IMG)

# %%
def moves_left(board, find_move=False):
    """
    Calculates all possible moves that can be maode on the current board.

    Parameters
    ----------
    board : numpy.ndarray
        A 2D array that stores information on each space on the boards status.
    find_move : boolean, optional
        Provides an alternative part to the funciton that returns what moves
        can be made, not just how many. The default is False.

    Returns
    -------
    pos_moves: list
        A list containg the start and end coordinates for any potential moves
        for the current board.
    move_count: int
        An integer value of how many potential moves for the current board are
        available.

    """
    row = 0
    col = 1

    move_count = 0#Sets counter to zero.
    pos_moves = []#Creates list to store all possible moves.

    #This loop works through each row of the board
    for row in range(len(board[:])):
        #This loop works through each peg of the row selected
        for col in range(len(board[:,:])):

            #This block identifies any pegs on the board and trys to create
            #a numpy array of any pegs it can jump over. The exceptions account
            #for any pegs on the board that might exceed the index limit, such
            #as pegs in row 7 or column G.
            if board[row,col] == p:
                try:

                    around_peg = np.array([board[row+1,col],
                                           board[row-1,col],
                                           board[row,col+1],
                                           board[row,col-1]])


                except:

                    try:

                        around_peg = np.array([board[row+1,col],
                                               board[row-1,col],
                                               0,
                                               board[row,col-1]])

                    except:


                        around_peg = np.array([0,
                                               board[row-1,col],
                                               board[row,col+1],
                                               board[row,col-1]])

                #This block identifies any directions in which a peg can jump
                #over a peg and if there is an empty space for the peg to land.
                for count, peg_here in enumerate(around_peg==p):
                    dist = [(row+2,col),(row-2,col),(row,col+2),(row,col-2)]
                    if peg_here == True:
                        try:
                            if board[dist[count]] == e:
                                move_count +=1
                                if find_move == True:
                                    pos_moves.append([(row,col),dist[count]])
                        except:
                            pass

    if find_move == True:
        return pos_moves
    return move_count

# %%
def undo(board,move_rec,board_rec,buttons = 0, vis = False):
    """
    Undoes the previous move by removing the last recorded board and move and 
    returning the board to its stae before the last move was made.

    Parameters
    ----------
    board : numpy.ndarray
        A 2D array that stores information on each space on the boards status.
    move_rec : list
        A list that keeps contains the coordinates of all successful moves
        taken.
    board_rec : list
        A list that stores all states of the board chronologically, excluding
        any boards that have been undone.

    Returns
    -------
    None.

    """
    #Reverses the last move, if there is one.
    if len(board_rec)>1:
        board_rec[:] = board_rec[:-1]
        board[:,:] = board_rec[-1]

    #Changes the advanced interface accordingly.
    if vis == True:
        move_rec[:] = move_rec[:-2]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i,j] == e:
                    buttons[i-1][j-1].config(image = EMPTY_IMG, state="disabled")
                elif board[i,j] == p:
                    buttons[i-1][j-1].config(image = PEG_IMG, state="enabled")
    else:
        move_rec[:] = move_rec[:-1]

# %%
time.sleep(.2)
menu()

# %%


# %%


# %%



