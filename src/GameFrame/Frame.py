import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import sqlite3
from src.DatabaseHandler import *
from src.GameFrame.utils import *


class GameFrame(tk.Frame):
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
        profile.bind("<Button-1>", lambda event: change_player(self, rows, leaderboard, connection, window))

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
        open_leaderboard.bind("<Button-1>", lambda event: (window.change_frame("LeaderboardFrame"), window.unbind("<Return>")))

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
        rows = create_boxes(self, master)

        self.guess_row = 0
        self.guess_button = tk.Button(self,
                                      text = "Guess",
                                      font = ("Arial", 14, "bold"),
                                      takefocus = False,
                                      fg = "White",
                                      bg = "#6e5c62",
                                      width = 8,
                                      height = 1,
                                      command = lambda: check_guess(self, rows, random_number, leaderboard, connection, window))
        self.guess_button.pack(anchor = "n",
                               pady = 10)
        # window.bind("<Return>", lambda event: check_guess(self, rows, random_number, leaderboard, connection, window))
    
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

        # window.unbind("<Return>")
        # window.bind("<Return>", lambda event: check_guess(self, rows, random_number, leaderboard, connection, window))

        random_number = generate_number()
        self.guess_button.configure(text = "Guess",
                                    command = lambda: check_guess(self, rows, random_number, leaderboard, connection, window))
    
    def _focus_next_box(self, event: tk.Event):
        """Focus on the next entry
        
        Parameters:
        event(tk.Event): Event that called the function
        """
        if event.char.isdigit():
            event.widget.tk_focusNext().focus()

    def _focus_previous(self, event: tk.Event):
        """Focus on the previous entry
        
        Parameters:
        event(tk.Event): Event that called the function
        """
        event.widget.tk_focusPrev().focus()

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
