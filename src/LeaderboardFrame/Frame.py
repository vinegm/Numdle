import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from src.DatabaseHandler import *
from src.LeaderboardFrame.utils import *


class LeaderboardFrame(tk.Frame):
    """Frame for displaying the top 10 best players and the current player best score"""
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)

        header_holder= tk.Frame(self,
                                bg = BG_APP)
        header_holder.pack(anchor = "center",
                           fill = "x",
                           pady = 5)
        
        back_image = Image.open("assets/BackWhite.png")
        back_image.thumbnail((30, 30))
        back_image = ImageTk.PhotoImage(back_image)

        back = tk.Button(header_holder,
                        image = back_image,
                        bg = BG_APP,
                        command = lambda: window.change_frame("GameFrame"))
        back.configure(relief = tk.FLAT)
        back.image = back_image
        back.pack(side = "left")

        header = tk.Label(header_holder,
                          text = "Leaderboard",
                          font = ("Arial", 16, "bold"),
                          fg = FG,
                          bg = BG_APP)
        header.pack(side = "left",
                    padx = 70)

        build_leaderboard(self, connection)
        display_player(self)

    def reload_leaderboard(self, connection: sqlite3.Connection, current_player: list):
        """Reloads the leaderboard
        
        Parameters:
        connection(sqlite3.Connection): Connection to the database
        current_player(list): List with the current player data
        """        
        self.leaderboard_holder.destroy()
        build_leaderboard(self, connection, current_player)

    def reload_player(self, current_player: list):
        """Realoads the player display
        
        Parameters:
        current_player(list): List with the current player data
        """
        self.player_holder.destroy()
        display_player(self, current_player)
