import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from src.DatabaseHandler import *


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
        
        top_players = get_top_ten(self, connection)
        self._populate_leaderboard(self.leaderboard_holder, top_players, current_player)
        
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
