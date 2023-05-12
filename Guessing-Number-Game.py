"""
Guessing Number Game
 Inspired by wordle/termo
"""
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from PIL import Image, ImageTk
import sqlite3
import numpy as np
from numpy import random as rd


def generate_number():
    """Generates a array with 5 random numbers from 0 to 9"""
    random_number = np.array(rd.randint(1, 10, 1))
    random_number = np.append(random_number, rd.randint(0, 10, 4))
    # print(random_number)  # Used for testing ONLY
    return random_number


def create_leaderboard(connection):
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
        self.iconbitmap("assets/Icon.ico")

        leaderboard = sqlite3.connect("assets/Leaderboard.db")
        create_leaderboard(leaderboard)

        frames_holder = tk.Frame(self)
        frames_holder.pack(anchor = "center")

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

        self.change_frame("Game")
        
    def change_frame(self, selected_frame):
        next_frame = self.frames[selected_frame]
        next_frame.tkraise()
        

class Game(tk.Frame):
    """Frame where you can play and guess"""
    def __init__(self, connection, master, leaderboard, window):
        tk.Frame.__init__(self, master)
        self.window = window
        self.connection = connection
        self.leaderboard = leaderboard 

        header_holder = tk.Frame(self)
        header_holder.pack(anchor = "center",
                           fill = "x",
                           pady = 5)
        
        leaderboard_profile = tk.Frame(header_holder)
        leaderboard_profile.grid(row = 0,
                                 column = 0,
                                 sticky = "w")

        profile_image = Image.open("assets/Profile.png")
        profile_image.thumbnail((30, 30))
        profile_image = ImageTk.PhotoImage(profile_image)

        self.player = [None, "Guest", 0, 0]
        self.score = 0
        self.consecutive_wins = 0
        profile = tk.Label(leaderboard_profile,
                           image = profile_image)
        profile.image = profile_image
        profile.grid(row = 0,
                     column = 1,
                     sticky = "e")
        profile.bind("<Button-1>", lambda event: self._select_player(simpledialog.askstring("Who are you?", f"Currently playing as: {self.player[1]}\nType a different nickname to change player:"), rows))

        leaderboard_image = Image.open("assets/Leaderboard.png")
        leaderboard_image.thumbnail((30, 30))
        leaderboard_image = ImageTk.PhotoImage(leaderboard_image)

        open_leaderboard = tk.Label(leaderboard_profile,
                                    image = leaderboard_image)
        open_leaderboard.image = leaderboard_image
        open_leaderboard.grid(row = 0,
                              column = 0,
                              sticky = "w")
        open_leaderboard.bind("<Button-1>", lambda event: self.window.change_frame("Leaderboard"))

        header = tk.Label(header_holder,
                          text = "Numdle",
                          font = ("Arial", 16, "bold"))
        header.grid(row = 0,
                    column = 1,
                    padx = 65,
                    sticky = "nsew")
        
        self.player_score = tk.Label(header_holder,
                                      text = f"Score: {self.player[2]}",
                                      font = ("Arial", 12, "bold"))
        self.player_score.grid(row = 0,
                                column = 2,
                                sticky = "e")

        self.info = tk.Label(self,
                             text = "Are you a good guesser?",
                             font = ("Arial", 12))
        self.info.pack(anchor = "center")

        random_number = generate_number()
        rows = self._create_boxes(master)

        self.guess_row = 0
        self.guess_button = tk.Button(self,
                                 text = "Guess",
                                 command = lambda: self._check_guess(rows, random_number))
        self.guess_button.pack(anchor = "n")

    def _check_guess(self, rows, random_number):
        """Checks the users guess"""
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
                box.configure(bg = "Green")
            else:
                box.configure(bg = "Gray")
        
        if np.all(target == _found):
            self.guess_button.config(text = "Play Again",
                                     command = lambda: self._clear_boxes(rows))
            self.info.configure(text = "Nice, you got it!")
            self.consecutive_wins += 1

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
                if int(box.get()) == number and box["bg"] != "Green":
                    target[i] = _found
                    box.configure(bg = "Yellow")
                    break
        
        if self.guess_row > 4:
            self.guess_button.config(text = "Try Again",
                                     command = lambda: self._clear_boxes(rows))
            self.info.configure(text = f"The number was {''.join(map(str, random_number))}")
            if self.player[1] != "Guest" and self.player[1] != "guest":
                self._update_status()
            self._update_boxes(rows, False)
            self.consecutive_wins = 0
            self.score = 0
        else:
            self._update_boxes(rows)

    def _update_boxes(self, rows, next_row = True):
        """Disables the boxes in the guess row and unlocks the boxes in the next if the number wasn't guessed"""
        for box in rows[self.guess_row]:
            box.configure(disabledbackground = box["bg"],
                          state = "disable")
            
        self.guess_row += 1
        if next_row == True:
            for box in rows[self.guess_row]:
                box.configure(state = "normal",
                              bg = "White")
    
    def _clear_boxes(self, rows):
        """Clears the guess boxes and resets their colours"""
        for boxes in rows:
            for box in boxes:
                box.configure(state = "normal",
                              bg = "#f0f0f0")
                box.delete(0, tk.END)
                box.configure(disabledbackground = box["bg"],
                              state = "disable")

        for box in rows[0]:
            box.configure(state = "normal",
                          bg = "White")

        self.guess_row = 0
        self.info.configure(text = "")
        self.player_score.configure(text = f"Score: {self.score}")
        random_number = generate_number()
        self.guess_button.configure(text = "Guess",
                                    command = lambda: self._check_guess(rows, random_number))

    def _create_boxes(self, app_window):
        """Creates the boxes for the user to guess the number
        
        Parameters:
        app_window (tk.Tk): Window holding the frame

        Returns:
        Boxes (Array): Array containing the boxes created
        """
        boxes_holder = tk.Label(self)
        boxes_holder.pack(anchor = "n")

        validation_command = app_window.register(self._validate_entry)

        rows = [[] for _ in range(6)]
        for i in range(6):
            for j in range(5):
                box = tk.Entry(boxes_holder,
                               font = ("Arial", 12),
                               justify = "center",
                               fg = "Black",
                               bg = "#f0f0f0",
                               width = 5,
                               state = "disabled",
                               validate = "key",
                               validatecommand=(validation_command, '%P'))
                box.configure(disabledforeground = box["fg"],
                              disabledbackground = box["bg"])
                box.grid(padx = 5,
                         pady = 10,
                         row = i+1,
                         column = j,
                         sticky = "ns")
                rows[i].append(box)

        for boxes in rows:
            for box in boxes:
                box.bind("<KeyPress>", self._focus_next_box)

        for box in rows[0]:
            box.configure(state = "normal",
                          bg = "White")

        return rows
    
    def _focus_next_box(self, event):
        if event.char.isdigit():
            event.widget.tk_focusNext().focus()

    def _validate_entry(self, entry_text):
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

    def _select_player(self, player, rows):
        if player == None or player == "":
            return
        
        self._update_status()
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM leaderboard WHERE player = ?""", (player,))
        result = cursor.fetchone()

        if result == None:
            self._create_player(player)
            cursor.execute("""SELECT * FROM leaderboard WHERE player = ?""", (player,))
            result = cursor.fetchone()
        
        cursor.close()
        self.player = list(result)

        self.window.title(f"Numdle ({self.player[1]})")
        self.player_score.configure(text = "Score: 0")
        self.info.configure(text = "")
        self._clear_boxes(rows)

        self.score = 0
        self.consecutive_wins = 0

        self.leaderboard._reload_player(self.player)

    def _create_player(self, player):
        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO leaderboard (player, score, consecutive_wins) VALUES (?, ?, ?)", (player, 0, 0))
        self.connection.commit()

        cursor.close()

    def _update_status(self):
        cursor = self.connection.cursor()
        update = False

        if self.player[2] < self.score and self.player[3] < self.consecutive_wins:
            cursor.execute("""UPDATE leaderboard SET score = ?, consecutive_wins = ?  WHERE id = ?""", (self.score, self.consecutive_wins, self.player[0]))
            update = True

        elif self.player[2] < self.score:
            cursor.execute("""UPDATE leaderboard SET score = ?  WHERE id = ?""", (self.score, self.player[0]))
            update = True

        elif self.player[3] < self.consecutive_wins:
            cursor.execute("""UPDATE leaderboard SET consecutive_wins = ?  WHERE id = ?""", (self.consecutive_wins, self.player[0]))
            update = True

        self.connection.commit()
        if update:
            self.leaderboard._reload_player(self.player)
        cursor.close()


class Leaderboard (tk.Frame):
    """Frame for displaying the top 10 best plays and a player best score"""
    def __init__(self, connection, master, window):
        tk.Frame.__init__(self, master)
        self.connection = connection

        header_holder= tk.Frame(self)
        header_holder.pack(anchor = "center",
                           fill = "x",
                           pady = 5)
        
        back_image = Image.open("assets/Back.png")
        back_image.thumbnail((30, 30))
        back_image = ImageTk.PhotoImage(back_image)

        back = tk.Label(header_holder,
                        image = back_image)
        back.image = back_image
        back.pack(side = "left")
        back.bind("<Button-1>", lambda event: window.change_frame("Game"))

        header = tk.Label(header_holder,
                          text = "Leaderboard",
                          font = ("Arial", 16, "bold"))
        header.pack(side = "left",
                    padx = 70)

        self._build_leaderboard()
        self._display_player()

    def _build_leaderboard(self):
        self.leaderboard_holder = tk.Frame(self)
        self.leaderboard_holder.pack(anchor = "center",
                                fill = "both")
        
        self.leaderboard_holder.grid_columnconfigure(0, minsize = 50)
        self.leaderboard_holder.grid_columnconfigure(list(range(1, 4)), minsize = 100)
        rank_column = tk.Label(self.leaderboard_holder,
                               text = "Rank",
                               font = ("Arial", 12, "bold"),
                               bg = "Gray",
                               border = 1,
                               relief = "solid")
        rank_column.grid(row = 0,
                         column = 0,
                         sticky = "nsew")

        player_column = tk.Label(self.leaderboard_holder,
                                 text = "Player",
                                 font = ("Arial", 12, "bold"),
                                 border = 1,
                                 relief = "solid")
        player_column.grid(row = 0,
                           column = 1,
                           sticky = "nsew")
        
        consecutive_wins_column = tk.Label(self.leaderboard_holder,
                                           text = "Wins in a Row",
                                           font = ("Arial", 12, "bold"),
                                           bg = "Gray",
                                           border = 1,
                                           relief = "solid")
        consecutive_wins_column.grid(row = 0,
                                     column = 2,
                                     sticky = "nsew")
        
        score_column = tk.Label(self.leaderboard_holder,
                                text = "Score",
                                font = ("Arial", 12, "bold"),
                                border = 1,
                                relief = "solid")
        score_column.grid(row = 0,
                          column = 3,
                          sticky = "nsew")
        
        top_players = self._get_top_ten()
        self._populate_leaderboard(self.leaderboard_holder, top_players)
        
    def _get_top_ten(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM Leaderboard ORDER BY score DESC LIMIT 10""")
        results = cursor.fetchall()
        cursor.close()
        return results

    def _populate_leaderboard(self, master, players):
        self.top_players_ids = []
        for i in range(1, 11):
            try:
                id, player, score, consecutive_wins = players[i-1]
            except IndexError:
                id, player, score, consecutive_wins = False, "None", 0, 0
            self.top_players_ids.append(id)

            medal = self._check_medal(i)

            rank_column = tk.Label(master,
                                   text = i,
                                   font = ("Arial", 12, "bold"),
                                   fg = medal,
                                   bg = "Gray",
                                   border = 1,
                                   relief = "solid")
            rank_column.grid(row = i,
                             column = 0,
                             sticky = "nsew")

            player_column = tk.Label(master,
                                     text = player,
                                     font = ("Arial", 12, "bold"),
                                     border = 1,
                                     relief = "solid")
            player_column.grid(row = i,
                               column = 1,
                               sticky = "nsew")
            
            consecutive_wins_column = tk.Label(master,
                                               text = consecutive_wins,
                                               font = ("Arial", 12, "bold"),
                                               bg = "Gray",
                                               border = 1,
                                               relief = "solid")
            consecutive_wins_column.grid(row = i,
                                         column = 2,
                                         sticky = "nsew")
            
            score_column = tk.Label(master,
                                    text = score,
                                    font = ("Arial", 12, "bold"),
                                    border = 1,
                                    relief = "solid")
            score_column.grid(row = i,
                              column = 3,
                              sticky = "nsew")

    def _reload_leaderboard(self):
        self.leaderboard_holder.destroy()
        self._build_leaderboard()

    def _display_player(self, player = None):
        self.player_info = tk.Frame(self)
        self.player_info.pack(anchor = "center",
                              pady = 10)
        self.player_info.grid_columnconfigure(0, minsize = 50)
        self.player_info.grid_columnconfigure(list(range(1, 4)), minsize = 100)

        if player == None:
            not_saved = tk.Label(self.player_info,
                                 text = "Guests Scores are not Tracked!",
                                 font = ("Arial", 12, "bold"),
                                 border = 1,
                                 relief = "solid")
            not_saved.grid(row = 0,
                           column = 0, columnspan = 4,
                           sticky = "nsew")
            return
        
        player_id, player_nick, player_consecutive_wins, player_score = player
        rank = False
        for i, id in enumerate(self.top_players_ids):
            if player_id == id:
                rank = i+1
                break
            elif id == False:
                break
        medal = self._check_medal(rank)
        

        rank = tk.Label(self.player_info,
                        text = f"{'#' if rank == False else rank}",
                        font = ("Arial", 12, "bold"),
                        fg = medal,
                        bg = "Gray",
                        border = 1,
                        relief = "solid")
        rank.grid(row = 0,
                  column = 0,
                  sticky = "nsew")

        player = tk.Label(self.player_info,
                          text = player_nick,
                          font = ("Arial", 12, "bold"),
                          border = 1,
                          relief = "solid")
        player.grid(row = 0,
                    column = 1,
                    sticky = "nsew")
        
        consecutive_wins = tk.Label(self.player_info,
                                    text = player_consecutive_wins,
                                    font = ("Arial", 12, "bold"),
                                    bg = "Gray",
                                    border = 1,
                                    relief = "solid")
        consecutive_wins.grid(row = 0,
                              column = 2,
                              sticky = "nsew")
        
        score = tk.Label(self.player_info,
                         text = player_score,
                         font = ("Arial", 12, "bold"),
                         border = 1,
                         relief = "solid")
        score.grid(row = 0,
                   column = 3,
                   sticky = "nsew")

    def _reload_player(self, player):
        self.player_info.destroy()
        self._display_player(player)

    def _check_medal(self, rank):
        if rank == 1:
            medal = "Yellow"
        elif rank == 2:
            medal = "#C0C0C0"
        elif rank == 3:
            medal = "#cd7f32"
        else:
            medal = "Black"
        return medal

if __name__ == "__main__":
    app = GuessingNumberGame()
    app.mainloop()