import tkinter as tk
from tkinter import messagebox
import sqlite3
import numpy as np
from src.DatabaseHandler import *
from src.GameFrame.utils.boxes_handler import *


def check_guess(self, rows: list, random_number: np.ndarray, leaderboard: tk.Frame, connection: sqlite3.Connection, window: tk.Tk):
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
            box.configure(bg = BG_CORRECT,
                          highlightbackground = HIGHLIGHTBG_CORRECT)
        else:
            box.configure(bg = BG_MISS,
                          highlightbackground = HIGHLIGHTBG_MISS)
    
    # If every number is correct
    if np.all(target == _found):
        self.guess_button.config(text = "Play Again",
                                    command = lambda: self._clear_ui(rows, leaderboard, connection, window))
        self.return_function = "clear"

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
        update_status(self, leaderboard, connection)
        update_boxes(self, rows, False)
        return

    for box in rows[self.guess_row]:
        for i, number in enumerate(target):
            if int(box.get()) == number and box["bg"] != BG_CORRECT:
                target[i] = _found
                box.configure(bg = BG_CLOSE,
                              highlightbackground = HIGHLIGHTBG_CLOSE)
                break
    
    # If the player used it's last guess
    if self.guess_row > 4:
        self.guess_button.config(text = "Try Again",
                                    command = lambda: self._clear_ui(rows, leaderboard, connection, window))
        self.return_function = "clear"
        self.info.configure(text = f"The number was {''.join(map(str, random_number))}")

        update_status(self, leaderboard, connection)
        update_boxes(self, rows, False)

        self.win_streak = 0
        self.score = 0
    else:
        update_boxes(self, rows)
