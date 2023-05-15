import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import sqlite3
from src.settings import *
from src.DatabaseHandler import *
from src.GameFrame.utils import *


class GameFrame(tk.Frame):
    """Frame where you can play the game"""
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, leaderboard: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)
        window.protocol("WM_DELETE_WINDOW", lambda: self._on_closing(leaderboard, connection, window))

        header_holder = tk.Frame(self,
                                 bg = BG_APP)
        header_holder.pack(anchor = "center",
                           fill = "x",
                           pady = 5)
        
        leaderboard_profile = tk.Frame(header_holder,
                                       bg = BG_APP)
        leaderboard_profile.grid(row = 0,
                                 column = 0,
                                 sticky = "w")

        profile_image = Image.open("assets/ProfileWhite.png")
        profile_image.thumbnail((30, 30))
        profile_image = ImageTk.PhotoImage(profile_image)

        self.player = [None, "Guest", 0, 0]
        self.score = 0
        self.win_streak = 0
        profile = tk.Button(leaderboard_profile,
                           image = profile_image,
                           bg = BG_APP,
                           command = lambda: change_player(self, rows, leaderboard, connection, window))
        profile.configure(relief = tk.FLAT)
        profile.image = profile_image
        profile.grid(row = 0,
                     column = 1,
                     sticky = "e")

        leaderboard_image = Image.open("assets/LeaderboardWhite.png")
        leaderboard_image.thumbnail((30, 30))
        leaderboard_image = ImageTk.PhotoImage(leaderboard_image)

        open_leaderboard = tk.Button(leaderboard_profile,
                                     image = leaderboard_image,
                                     bg = BG_APP,
                                     command = lambda: window.change_frame("LeaderboardFrame"))
        open_leaderboard.configure(relief = tk.FLAT)
        open_leaderboard.image = leaderboard_image
        open_leaderboard.grid(row = 0,
                              column = 0,
                              sticky = "w")

        header = tk.Label(header_holder,
                          text = "Numdle",
                          font = ("Arial", 16, "bold"),
                          fg = "White",
                          bg = BG_APP)
        header.grid(row = 0,
                    column = 1,
                    padx = 65,
                    sticky = "nsew")
        
        self.player_score = tk.Label(header_holder,
                                      text = f"Score: {self.player[2]}",
                                      font = ("Arial", 12, "bold"),
                                      fg = "White",
                                      bg = BG_APP)
        self.player_score.grid(row = 0,
                                column = 2,
                                sticky = "e")

        self.info = tk.Label(self,
                             text = "",
                             font = ("Arial", 12),
                             fg = "White",
                             bg = BG_APP)
        self.info.pack(anchor = "center")

        self.random_number = generate_number()
        rows = create_boxes(self, master)

        self.guess_row = 0
        self.guess_button = tk.Button(self,
                                      text = "Guess",
                                      font = ("Arial", 14, "bold"),
                                      fg = "White",
                                      bg = GUESS_BUTTON,
                                      width = 8,
                                      height = 1,
                                      command = lambda: check_guess(self, rows, leaderboard, connection, window))
        self.guess_button.pack(anchor = "n",
                               pady = 10)
        self.return_function = "guess"
        window.bind("<Return>", lambda event: self._return_bind(rows, leaderboard, connection, window))
    
    def _return_bind(self, rows: list, leaderboard: tk.Frame, connection: sqlite3.Connection, window: tk.Tk):
        """Checks which function the key press should call
        
        Parameters:
        rows(list): List of rows with the boxes from the player guess
        leaderboard(tk.Frame): Frame holding the leaderboard
        connection(sqlite3.Connection): Connection to the database
        window(tk.Tk): Window of the app
        """
        if self.return_function == "guess":
            check_guess(self, rows, leaderboard, connection, window)

        elif self.return_function == "clear":
            self._clear_ui(rows, leaderboard, connection, window)

    def _clear_ui(self, rows: list, leaderboard: tk.Frame, connection: sqlite3.Connection, window: tk.Tk, changing_player = False):
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
                              bg = BG_DISABLED,
                              highlightbackground = HIGHLIGHTBG_DISABLED)
                box.delete(0, tk.END)
                box.configure(disabledbackground = box["bg"],
                              state = "disable")

        for box in rows[0]:
            box.configure(state = "normal",
                          bg = BG_APP,
                          highlightbackground = HIGHLIGHTBG_GUESS_ROW,
                          highlightcolor = HIGHLIGHTCOLOR_GUESS_ROW)

        self.guess_row = 0
        if not changing_player and self.win_streak >= 1:
            self.info.configure(text = f"Win Streak: {self.win_streak}")
        else:
            self.info.configure(text = "")
        self.player_score.configure(text = f"Score: {self.score}")

        rows[0][0].focus()
        self.return_function = "guess"
        self.random_number = generate_number()
        self.guess_button.configure(text = "Guess",
                                    command = lambda: check_guess(self, rows, leaderboard, connection, window))

    def _focus_handler(self, event: tk.Event, rows: list, box_row: int, box_column: int):
        """Handles the focus between the boxes
        
        Parameters:
        event(tk.Event): Key press that called the function
        rows(list): List of boxes
        box_row(int): Row the box that called the function is in
        box_column(int): Column the box that called the function is in
        """
        if event.char.isdigit():
            try:
                rows[box_row][box_column+1].focus()
            except IndexError:
                pass
            return
        
        elif event.keysym == "BackSpace":
            if box_column < 1:
                return
            
            if len(rows[box_row][box_column].get()) < 1:
                rows[box_row][box_column-1].delete(0, tk.END)
                rows[box_row][box_column-1].focus()
                return
    
        elif rows[box_row][box_column].index("insert") == 0 and event.keysym == "Left":
            if box_column < 1:
                return

            rows[box_row][box_column-1].focus()
        
        elif rows[box_row][box_column].index("insert") == len(rows[box_row][box_column].get()) and event.keysym == "Right":
            try:
                rows[box_row][box_column+1].focus()
            except IndexError:
                pass
            return
            
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

    def _on_closing(self, leaderboard: tk.Frame, connection: sqlite3.Connection, window: tk.Tk):
        """Updates the current player status before closing the app
        
        Parameters:
        leaderboard(tk.Frame): Frame holding the leaderboard
        connection(sqlite3.Connection): Connection to the database
        window(tk.Tk): Window of the game
        """
        update_status(self, leaderboard, connection)
        window.destroy()
