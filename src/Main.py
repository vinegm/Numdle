import tkinter as tk
import sqlite3
from src.GameFrame import *
from src.LeaderboardFrame import *
from src.DatabaseHandler import *


class Numdle(tk.Tk):
    """Window of the game"""
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Numdle (Guest)")
        self.geometry("360x360")
        self.resizable(False, False)
        self.eval("tk::PlaceWindow . center")
        self.iconbitmap("assets/Numdle.ico")

        leaderboard = connect_db()

        frames_holder = tk.Frame(self)
        frames_holder.pack(anchor = "center",
                           fill = "both",
                           expand = "True")

        self.frames = {}
        leaderboard_frame = LeaderboardFrame(leaderboard, frames_holder, self)
        leaderboard_frame.grid(row = 0,
                               column = 0,
                               sticky = "nsew")
        self.frames[LeaderboardFrame.__name__] = leaderboard_frame

        game_frame = GameFrame(leaderboard, frames_holder, leaderboard_frame, self)
        game_frame.grid(row = 0,
                        column = 0,
                        sticky = "nsew")
        self.frames[GameFrame.__name__] = game_frame

        frames_holder.columnconfigure(0, weight=1)
        frames_holder.rowconfigure(0, weight=1)

        self.change_frame("GameFrame")

        self.mainloop()
        
    def change_frame(self, selected_frame: tk.Frame):
        """Changes to the next selected frame
        
        Parameters:
        selected_frame(tk.Frame): Frame that will be raised
        """
        next_frame = self.frames[selected_frame]
        next_frame.tkraise()
