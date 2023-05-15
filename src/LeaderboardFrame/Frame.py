import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from src.DatabaseHandler import *
from src.LeaderboardFrame.utils import *


class LeaderboardFrame(tk.Frame):
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
        back.bind("<Button-1>", lambda event: window.change_frame("GameFrame"))

        header = tk.Label(header_holder,
                          text = "LeaderboardFrame",
                          font = ("Arial", 16, "bold"),
                          fg = "White",
                          bg = "#6e5c62")
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
