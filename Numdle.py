"""
Numdle
 Inspired by wordle/termo
"""
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from PIL import Image, ImageTk
import sqlite3
import numpy as np
from numpy import random as rd


def generate_number() -> np.ndarray:
    """Generates a array with 5 random numbers from 0 to 9
    
    Returns:
    random_number(np.ndarray): An array with 5 digits, each ranging from 0 to 9
    """
    random_number = np.array(rd.randint(1, 10, 1))
    random_number = np.append(random_number, rd.randint(0, 10, 4))
    # print(random_number)  # Used for testing ONLY
    return random_number


def create_leaderboard(connection: sqlite3.Connection):
    """Creates the table of the leaderboard if it doesn't exist
    
    Parameters:
    connection(sqlite3.Connection): Connection to the database
    """
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS leaderboard (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   player VARCHAR NOT NULL UNIQUE,
                   score INTEGER NOT NULL,
                   consecutive_wins INTEGER NOT NULL
                   )""")
    cursor.close()


class GuessingNumberGame(tk.Tk):
    """Window of the game"""
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Numdle (Guest)")
        self.geometry("360x360")
        self.resizable(False, False)
        self.eval("tk::PlaceWindow . center")
        self.iconbitmap("assets/Numdle.ico")

        leaderboard = sqlite3.connect("assets/Leaderboard.db")
        create_leaderboard(leaderboard)

        frames_holder = tk.Frame(self)
        frames_holder.pack(anchor = "center",
                           fill = "both",
                           expand = "True")

        self.frames = {}
        leaderboard_frame = Leaderboard(leaderboard, frames_holder, self)
        leaderboard_frame.grid(row = 0,
                               column = 0,
                               sticky = "nsew")
        self.frames[Leaderboard.__name__] = leaderboard_frame

        game_frame = Game(leaderboard, frames_holder, leaderboard_frame, self)
        game_frame.grid(row = 0,
                        column = 0,
                        sticky = "nsew")
        self.frames[Game.__name__] = game_frame

        frames_holder.columnconfigure(0, weight=1)
        frames_holder.rowconfigure(0, weight=1)

        self.change_frame("Game")

        self.mainloop()
        
    def change_frame(self, selected_frame: tk.Frame):
        """Changes to the next selected frame
        
        Parameters:
        selected_frame(tk.Frame): Frame that will be raised
        """
        next_frame = self.frames[selected_frame]
        next_frame.tkraise()
        

class Game(tk.Frame):
    """Frame where you can play the game"""
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, leaderboard: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = "#6e5c62")
        window.protocol("WM_DELETE_WINDOW", lambda: self._on_closing(leaderboard, connection, window))

        header_holder = tk.Frame(self,
                                 bg = "#6e5c62")
        header_holder.pack(anchor = "center",
                           fill = "x",
                           pady = 5)
        
        leaderboard_profile = tk.Frame(header_holder,
                                       bg = "#6e5c62")
        leaderboard_profile.grid(row = 0,
                                 column = 0,
                                 sticky = "w")

        profile_image = Image.open("assets/ProfileWhite.png")
        profile_image.thumbnail((30, 30))
        profile_image = ImageTk.PhotoImage(profile_image)

        self.player = [None, "Guest", 0, 0]
        self.score = 0
        self.win_streak = 0
        profile = tk.Label(leaderboard_profile,
                           image = profile_image,
                           bg = "#6e5c62")
        profile.image = profile_image
        profile.grid(row = 0,
                     column = 1,
                     sticky = "e")
        profile.bind("<Button-1>", lambda event: self._change_player(rows, leaderboard, connection, window))

        leaderboard_image = Image.open("assets/LeaderboardWhite.png")
        leaderboard_image.thumbnail((30, 30))
        leaderboard_image = ImageTk.PhotoImage(leaderboard_image)

        open_leaderboard = tk.Label(leaderboard_profile,
                                    image = leaderboard_image,
                                    bg = "#6e5c62")
        open_leaderboard.image = leaderboard_image
        open_leaderboard.grid(row = 0,
                              column = 0,
                              sticky = "w")
        open_leaderboard.bind("<Button-1>", lambda event: window.change_frame("Leaderboard"))

        header = tk.Label(header_holder,
                          text = "Numdle",
                          font = ("Arial", 16, "bold"),
                          fg = "White",
                          bg = "#6e5c62")
        header.grid(row = 0,
                    column = 1,
                    padx = 65,
                    sticky = "nsew")
        
        self.player_score = tk.Label(header_holder,
                                      text = f"Score: {self.player[2]}",
                                      font = ("Arial", 12, "bold"),
                                      fg = "White",
                                      bg = "#6e5c62")
        self.player_score.grid(row = 0,
                                column = 2,
                                sticky = "e")

        self.info = tk.Label(self,
                             text = "",
                             font = ("Arial", 12),
                             fg = "White",
                             bg = "#6e5c62")
        self.info.pack(anchor = "center")

        random_number = generate_number()
        rows = self._create_boxes(master)

        self.guess_row = 0
        self.guess_button = tk.Button(self,
                                      text = "Guess",
                                      font = ("Arial", 14, "bold"),
                                      fg = "White",
                                      bg = "#6e5c62",
                                      width = 8,
                                      height = 1,
                                      command = lambda: self._check_guess(rows, random_number, leaderboard, connection))
        self.guess_button.pack(anchor = "n",
                               pady = 10)

    def _check_guess(self, rows: list, random_number: np.ndarray, leaderboard: tk.Frame, connection: sqlite3.Connection):
        """Checks the player guess
        
        Parameters:
        rows(list): List of rows with the boxes from the player guess
        random_number(np.ndarray): Array representing the random number generated
        leaderboard(tk.Frame): Frame holding the leaderboard
        connection(sqlite3.Connection): Connection to the database
        """
        for box in rows[self.guess_row]:
            if box.get() == "":
                messagebox.showwarning(title = "Fill the Boxes",
                                       message = "You have to fill all the\nboxes to make a guess!")
                return
        _found = -1

        target = np.copy(random_number)
        for i, box in enumerate(rows[self.guess_row]):
            if int(box.get()) == target[i]:
                target[i] = _found
                box.configure(bg = "#3aa394",
                              highlightbackground = "#3aa394")
            else:
                box.configure(bg = "#312a2c",
                              highlightbackground = "#312a2c")
        
        # If every number is correct
        if np.all(target == _found):
            self.guess_button.config(text = "Play Again",
                                     command = lambda: self._clear_ui(rows, leaderboard, connection))
            self.info.configure(text = "Nice, you got it!")
            self.win_streak += 1

            if self.guess_row == 0:
                self.score += 5
            elif self.guess_row == 1:
                self.score += 4
            elif self.guess_row == 2:
                self.score += 3
            elif self.guess_row == 3:
                self.score += 2
            elif self.guess_row == 4:
                self.score += 1

            self.player_score.configure(text = f"Score: {self.score}")
            self._update_boxes(rows, False)
            return

        for box in rows[self.guess_row]:
            for i, number in enumerate(target):
                if int(box.get()) == number and box["bg"] != "#3aa394":
                    target[i] = _found
                    box.configure(bg = "#d3ad69",
                                  highlightbackground = "#d3ad69")
                    break
        
        # If the player used it's last guess
        if self.guess_row > 4:
            self.guess_button.config(text = "Try Again",
                                     command = lambda: self._clear_ui(rows, leaderboard, connection))
            self.info.configure(text = f"The number was {''.join(map(str, random_number))}")

            self._update_status(leaderboard, connection)
            self._update_boxes(rows, False)

            self.win_streak = 0
            self.score = 0
        else:
            self._update_boxes(rows)

    def _update_boxes(self, rows: list, next_row: None = True):
        """Disables the boxes in the guess row and unlocks the boxes in the next if the number wasn't guessed
        
        Parameters:
        rows(list): List of rows with the boxes from the player guess
        next_row(bool): Tells the function if the next row should or not be unlocked
        """
        for box in rows[self.guess_row]:
            box.configure(disabledbackground = box["bg"],
                          state = "disable")
            
        self.guess_row += 1
        if next_row == True:
            for box in rows[self.guess_row]:
                box.configure(state = "normal",
                              bg = "#6e5c62",
                              highlightbackground = "#4c4347",
                              highlightcolor = "#4c4347")
    
    def _clear_ui(self, rows: list, leaderboard: tk.Frame, connection: sqlite3.Connection, changing_player = False):
        """Clears the UI from the game frame
        
        Parameters:
        rows(list): List of rows with the boxes from the player guess
        leaderboard(tk.Frame): Frame holding the leaderboard
        connection(sqlite3.Connection): Connection to the database
        changing_player(bool): Tells the function if the player is being changed
        """
        for boxes in rows:
            for box in boxes:
                box.configure(state = "normal",
                              bg = "#615458",
                              highlightbackground = "#615458")
                box.delete(0, tk.END)
                box.configure(disabledbackground = box["bg"],
                              state = "disable")

        for box in rows[0]:
            box.configure(state = "normal",
                          bg = "#6e5c62",
                          highlightbackground = "#4c4347",
                          highlightcolor = "#4c4347")

        self.guess_row = 0
        if not changing_player and self.win_streak >= 1:
            self.info.configure(text = f"Win Streak: {self.win_streak}")
        else:
            self.info.configure(text = "")
        self.player_score.configure(text = f"Score: {self.score}")

        random_number = generate_number()
        self.guess_button.configure(text = "Guess",
                                    command = lambda: self._check_guess(rows, random_number, leaderboard, connection))

    def _create_boxes(self, app_window: tk.Tk) -> list:
        """Creates the boxes for the user to guess the number
        
        Parameters:
        app_window(tk.Tk): Window holding the frame

        Returns:
        rows(list): List containing the boxes created
        """
        boxes_holder = tk.Label(self,
                                bg = "#6e5c62")
        boxes_holder.pack(anchor = "n")

        validation_command = app_window.register(self._validate_entry)

        rows = [[] for _ in range(6)]
        for i in range(6):
            for j in range(5):
                box = tk.Entry(boxes_holder,
                               font = ("Arial", 14),
                               justify = "center",
                               fg = "White",
                               bg = "#615458",
                               width = 3,
                               border = 0,
                               highlightthickness = 4,
                               highlightbackground = "#615458",
                               state = "disabled",
                               validate = "key",
                               validatecommand=(validation_command, '%P'))
                box.configure(disabledforeground = box["fg"],
                              disabledbackground = box["bg"])
                box.grid(padx = 2,
                         pady = 3,
                         row = i+1,
                         column = j,
                         sticky = "ns")
                rows[i].append(box)

        for boxes in rows:
            for box in boxes:
                box.bind("<KeyPress>", self._focus_next_box)

        for box in rows[0]:
            box.configure(state = "normal",
                          bg = "#6e5c62",
                          highlightbackground = "#4c4347",
                          highlightcolor = "#4c4347")

        return rows
    
    def _focus_next_box(self, event: tk.Event):
        """Focus on the next entry
        
        Parameters:
        event(tk.Event): Event that called the function
        """
        if event.char.isdigit():
            event.widget.tk_focusNext().focus()

    def _validate_entry(self, entry_text: str) -> bool:
        """Validates that each box can only have 1 digit
        
        Parameters:
        entry_text (string): Full text inside the entry after the button press

        Retuns:
        True: If the box is empty and the pressed button is a digit
        False: If the box already has something in it or the button pressed isn't a digit
        """
        if entry_text == "":
            return True
        
        elif entry_text.isdigit() and len(entry_text) == 1:
            return True
        
        return False

    def _change_player(self, rows: list, leaderboard: tk.Frame, connection: sqlite3.Connection, window: tk.Tk):
        """Changes the current player
        
        Parameters:
        rows(list): List of rows with the boxes from the player guess
        leaderboard(tk.Frame): Frame holding the leaderboard
        connection(sqlite3.Connection): Connection to the database
        window(tk.Tk): Window of the game
        """
        player = simpledialog.askstring("Who are you?", f"Currently playing as: {self.player[1]}\nType a different nickname to\nchange player (Limit of 7 characters):")
        # If the user didn't type a player
        if player == None or player == "":
            return
        
        # If the user typed a player nick that is too long
        if len(player) > 7:
            messagebox.showerror("Too Big!", "The nickname you tried is too big!")
            return
        
        self._update_status(leaderboard, connection, True)
        # Turns the player into a guest
        if player == "Guest" or player == "guest":
            self.player = [None, "Guest", 0, 0]
        # Gets the player from the database
        else:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM leaderboard WHERE player = ?""", (player,))
            result = cursor.fetchone()
            
            # Creates the player if he doesn't exist yet
            if result == None:
                self._create_player(player, connection)
                cursor.execute("""SELECT * FROM leaderboard WHERE player = ?""", (player,))
                result = cursor.fetchone()
            
            cursor.close()
            self.player = list(result)

        # Resets the score and win streak
        self.score = 0
        self.win_streak = 0

        # Updates the UI
        window.title(f"Numdle ({self.player[1]})")
        self._clear_ui(rows, leaderboard, connection, True)

        # Reloads the leaderboard
        leaderboard.reload_leaderboard(connection, self.player)
        leaderboard.reload_player(self.player)

    def _create_player(self, player: str, connection: sqlite3.Connection):
        """Creates a player on the database
        
        Parameters:
        player(str): Nickname of the player that will be created
        connection(connection: sqlite3.Connection): Connection to the database
        """
        cursor = connection.cursor()

        cursor.execute("INSERT INTO leaderboard (player, score, consecutive_wins) VALUES (?, ?, ?)", (player, 0, 0))
        connection.commit()

        cursor.close()

    def _update_status(self, leaderboard: tk.Frame, connection: sqlite3.Connection, changing_player: bool = False):
        """Updates the current player status
        
        Parameters:
        leaderboard(tk.Frame): Frame holding the leaderboard
        connection(sqlite3.Connection): Connection to the database
        changing_player(bool): Tells the function if the player is being changed
        """
        # If the current player is a guest
        if self.player[1] == "Guest" or self.player[1] == "guest":
            return

        cursor = connection.cursor()

        update = False  # For keeping track if the player got a new record
        if self.player[2] < self.score and self.player[3] < self.win_streak:
            cursor.execute("""UPDATE leaderboard SET score = ?, consecutive_wins = ?  WHERE id = ?""", (self.score, self.win_streak, self.player[0]))
            self.player[2] = self.score
            self.player[3] = self.win_streak
            update = True

        elif self.player[2] < self.score:
            cursor.execute("""UPDATE leaderboard SET score = ?  WHERE id = ?""", (self.score, self.player[0]))
            self.player[2] = self.score
            update = True

        elif self.player[3] < self.win_streak:
            cursor.execute("""UPDATE leaderboard SET consecutive_wins = ?  WHERE id = ?""", (self.win_streak, self.player[0]))
            self.player[3] = self.win_streak
            update = True

        connection.commit()
        cursor.close()

        if not changing_player:
            # Updates the leaderboard if the player got a rank
            if (leaderboard.on_top_players and update) or (leaderboard.last_rank_score <= self.score):
                leaderboard.reload_leaderboard(connection, self.player)
                was_updated = True

            if update or was_updated:
                leaderboard.reload_player(self.player)

    def _on_closing(self, leaderboard: tk.Frame, connection: sqlite3.Connection, window: tk.Tk):
        """Updates the current player status before closing the app
        
        Parameters:
        leaderboard(tk.Frame): Frame holding the leaderboard
        connection(sqlite3.Connection): Connection to the database
        window(tk.Tk): Window of the game
        """
        self._update_status(leaderboard, connection)
        window.destroy()


class Leaderboard(tk.Frame):
    """Frame for displaying the top 10 best players and the current player best score"""
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = "#6e5c62")

        header_holder= tk.Frame(self,
                                bg = "#6e5c62")
        header_holder.pack(anchor = "center",
                           fill = "x",
                           pady = 5)
        
        back_image = Image.open("assets/BackWhite.png")
        back_image.thumbnail((30, 30))
        back_image = ImageTk.PhotoImage(back_image)

        back = tk.Label(header_holder,
                        image = back_image,
                        bg = "#6e5c62")
        back.image = back_image
        back.pack(side = "left")
        back.bind("<Button-1>", lambda event: window.change_frame("Game"))

        header = tk.Label(header_holder,
                          text = "Leaderboard",
                          font = ("Arial", 16, "bold"),
                          fg = "White",
                          bg = "#6e5c62")
        header.pack(side = "left",
                    padx = 70)

        self._build_leaderboard(connection)
        self._display_player()

    def _build_leaderboard(self, connection: sqlite3.Connection, current_player: list = None):
        """Builds the leaderboard heads
        
        Parameters:
        connection(sqlite3.Connection): Connection to the database
        current_player(list): List with the data of the current player
        """
        self.leaderboard_holder = tk.Frame(self,
                                           bg = "#6e5c62")
        self.leaderboard_holder.pack(anchor = "center",
                                     fill = "both",
                                     pady = 10)
        
        self.leaderboard_holder.grid_columnconfigure(0, minsize = 50)
        self.leaderboard_holder.grid_columnconfigure(1, minsize = 113)
        self.leaderboard_holder.grid_columnconfigure(list(range(2, 4)), minsize = 100)

        rank_column = tk.Label(self.leaderboard_holder,
                               text = "Rank",
                               font = ("Arial", 12, "bold"),
                               fg = "White",
                               bg = "#4c4347",
                               border = 1,
                               relief = "solid")
        rank_column.grid(row = 0,
                         column = 0,
                         sticky = "nsew")

        player_column = tk.Label(self.leaderboard_holder,
                                 text = "Player",
                                 font = ("Arial", 12, "bold"),
                                 fg = "White",
                                 bg = "#6e5c62",
                                 border = 1,
                                 relief = "solid")
        player_column.grid(row = 0,
                           column = 1,
                           sticky = "nsew")
        
        consecutive_wins_column = tk.Label(self.leaderboard_holder,
                                           text = "Win Streak",
                                           font = ("Arial", 12, "bold"),
                                           fg = "White",
                                           bg = "#4c4347",
                                           border = 1,
                                           relief = "solid")
        consecutive_wins_column.grid(row = 0,
                                     column = 2,
                                     sticky = "nsew")
        
        score_column = tk.Label(self.leaderboard_holder,
                                text = "Score",
                                font = ("Arial", 12, "bold"),
                                fg = "White",
                                bg = "#6e5c62",
                                border = 1,
                                relief = "solid")
        score_column.grid(row = 0,
                          column = 3,
                          sticky = "nsew")
        
        top_players = self._get_top_ten(connection)
        self._populate_leaderboard(self.leaderboard_holder, top_players, current_player)
        
    def _get_top_ten(self, connection: sqlite3.Connection) -> list:
        """Gets the top 10 players from the database, based on score

        Parameters:
        connection(sqlite3.Connection): Connection to the database

        Returns:
        results(list): List of tuples containing the players data
        """
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM Leaderboard ORDER BY score DESC LIMIT 10""")
        results = cursor.fetchall()
        
        cursor.close()
        return results

    def _populate_leaderboard(self, master: tk.Frame, top_players: list, current_player: list):
        """Populate the leaderboard with the top 10 players
        
        Parameters:
        master(tk.Frame): Frame that holds the leaderboard
        top_players(list): List of 10 tuples conteining the players data
        current_player(list): List with the current player data
        """
        self.top_players_ids = []
        for i in range(1, 11):
            # Makes fillers for the leaderboard if there aren't enough data
            try:
                player_id, player, score, consecutive_wins = top_players[i-1]
            except IndexError:
                player_id, player, score, consecutive_wins = [None, "None", 0, 0]

            self.top_players_ids.append(player_id)
            medal = self._check_medal(i)

            # Check if the current player is part of the top players
            is_current = False
            try:
                if current_player[0] == player_id and current_player[1] != "Guest":
                    is_current = True
            except TypeError:
                pass

            rank_column = tk.Label(master,
                                   text = i,
                                   font = ("Arial", 12, "bold"),
                                   fg = medal,
                                   bg = "#4c4347",
                                   border = 1,
                                   relief = "solid")
            rank_column.grid(row = i,
                             column = 0,
                             sticky = "nsew")

            player_column = tk.Label(master,
                                     text = "You" if is_current else player,
                                     font = ("Arial", 12, "bold"),
                                     fg = "Blue" if is_current else "White",
                                     bg = "#6e5c62",
                                     border = 1,
                                     relief = "solid")
            player_column.grid(row = i,
                               column = 1,
                               sticky = "nsew")
            
            consecutive_wins_column = tk.Label(master,
                                               text = consecutive_wins,
                                               font = ("Arial", 12, "bold"),
                                               fg = "White",
                                               bg = "#4c4347",
                                               border = 1,
                                               relief = "solid")
            consecutive_wins_column.grid(row = i,
                                         column = 2,
                                         sticky = "nsew")
            
            score_column = tk.Label(master,
                                    text = score,
                                    font = ("Arial", 12, "bold"),
                                    fg = "White",
                                    bg = "#6e5c62",
                                    border = 1,
                                    relief = "solid")
            score_column.grid(row = i,
                              column = 3,
                              sticky = "nsew")
        self.last_rank_score = score

    def reload_leaderboard(self, connection: sqlite3.Connection, current_player: list):
        """Reloads the leaderboard
        
        Parameters:
        connection(sqlite3.Connection): Connection to the database
        current_player(list): List with the current player data
        """        
        self.leaderboard_holder.destroy()
        self._build_leaderboard(connection, current_player)

    def _display_player(self, current_player: list = None):
        """Displays the current player status below the leaderboard
        
        Parameters:
        current_player(list): List with the current player data
        """
        self.player_holder = tk.Frame(self)
        self.player_holder.pack(anchor = "center",
                                pady = 5)
        self.player_holder.grid_columnconfigure(0, minsize = 50)
        self.player_holder.grid_columnconfigure(1, minsize = 113)
        self.player_holder.grid_columnconfigure(list(range(2, 4)), minsize = 100)

        self.on_top_players = False
        # If the current player is a guest
        if current_player == None or current_player[1] == "Guest":
            not_saved = tk.Label(self.player_holder,
                                 text = "Guests Scores are not Tracked!",
                                 font = ("Arial", 12, "bold"),
                                 fg = "White",
                                 bg = "#4c4347",
                                 relief = "solid")
            not_saved.grid(row = 0,
                           column = 0, columnspan = 4,
                           sticky = "nsew")
            return
        else:
            player_id, player_nick, player_score, player_consecutive_wins = current_player
            rank, medal = self._check_rank(player_id)

        rank = tk.Label(self.player_holder,
                        text = "#" if rank == None else rank,
                        font = ("Arial", 12, "bold"),
                        fg = medal,
                        bg = "#4c4347",
                        border = 1,
                        relief = "solid")
        rank.grid(row = 0,
                  column = 0,
                  sticky = "nsew")

        player = tk.Label(self.player_holder,
                          text = player_nick,
                          font = ("Arial", 12, "bold"),
                          fg = "White",
                          bg = "#6e5c62",
                          border = 1,
                          relief = "solid")
        player.grid(row = 0,
                    column = 1,
                    sticky = "nsew")
        
        consecutive_wins = tk.Label(self.player_holder,
                                    text = player_consecutive_wins,
                                    font = ("Arial", 12, "bold"),
                                    fg = "White",
                                    bg = "#4c4347",
                                    border = 1,
                                    relief = "solid")
        consecutive_wins.grid(row = 0,
                              column = 2,
                              sticky = "nsew")
        
        score = tk.Label(self.player_holder,
                         text = player_score,
                         font = ("Arial", 12, "bold"),
                         fg = "White",
                         bg = "#6e5c62",
                         border = 1,
                         relief = "solid")
        score.grid(row = 0,
                   column = 3,
                   sticky = "nsew")

    def reload_player(self, current_player: list):
        """Realoads the player display
        
        Parameters:
        current_player(list): List with the current player data
        """
        self.player_holder.destroy()
        self._display_player(current_player)

    def _check_rank(self, player_id: int):
        """Checks if the current player is in the top 10 players
        
        Parameters:
        rank(int|None): Rank of the current player
        medal(str): Hex of the player's medal
        """
        rank = None
        for i, id in enumerate(self.top_players_ids):
            if player_id == id:
                rank = i+1
                self.on_top_players = True
                break

            elif id == None:
                break
        
        medal = self._check_medal(rank)
        return rank, medal

    def _check_medal(self, rank: int) -> str:
        """Checks if the current player is in the top 3 players
        
        Parameters:
        rank(int): Rank of the current player

        Returns:
        medal(str): Hex code of the color of his medal if he has one
        """
        if rank == 1:
            medal = "Yellow"
        elif rank == 2:
            medal = "#C0C0C0"
        elif rank == 3:
            medal = "#cd7f32"
        else:
            medal = "White"
        return medal


if __name__ == "__main__":
    GuessingNumberGame()
