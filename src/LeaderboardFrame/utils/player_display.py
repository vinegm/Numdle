import tkinter as tk
from src.settings import *
from src.LeaderboardFrame.utils.check_rank import *


def display_player(self, current_player: list = None):
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
                                 fg = FG,
                                 bg = BG_LEADERBOARD_ODD,
                                 relief = "solid")
            not_saved.grid(row = 0,
                           column = 0, columnspan = 4,
                           sticky = "nsew")
            return
        else:
            player_id, player_nick, player_score, player_consecutive_wins = current_player
            rank, medal = check_rank(self, player_id)

        rank = tk.Label(self.player_holder,
                        text = "#" if rank == None else rank,
                        font = ("Arial", 12, "bold"),
                        fg = medal,
                        bg = BG_LEADERBOARD_ODD,
                        border = 1,
                        relief = "solid")
        rank.grid(row = 0,
                  column = 0,
                  sticky = "nsew")

        player = tk.Label(self.player_holder,
                          text = player_nick,
                          font = ("Arial", 12, "bold"),
                          fg = FG,
                          bg = BG_LEADERBOARD_EVEN,
                          border = 1,
                          relief = "solid")
        player.grid(row = 0,
                    column = 1,
                    sticky = "nsew")
        
        consecutive_wins = tk.Label(self.player_holder,
                                    text = player_consecutive_wins,
                                    font = ("Arial", 12, "bold"),
                                    fg = FG,
                                    bg = BG_LEADERBOARD_ODD,
                                    border = 1,
                                    relief = "solid")
        consecutive_wins.grid(row = 0,
                              column = 2,
                              sticky = "nsew")
        
        score = tk.Label(self.player_holder,
                         text = player_score,
                         font = ("Arial", 12, "bold"),
                         fg = FG,
                         bg = BG_LEADERBOARD_EVEN,
                         border = 1,
                         relief = "solid")
        score.grid(row = 0,
                   column = 3,
                   sticky = "nsew")
