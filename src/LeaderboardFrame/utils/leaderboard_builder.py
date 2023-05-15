import tkinter as tk
import sqlite3
from src.settings import *
from src.DatabaseHandler import *
from src.LeaderboardFrame.utils.check_rank import *


def build_leaderboard(test, connection: sqlite3.Connection, current_player: list = None):
    """Builds the leaderboard heads
    
    Parameters:
    connection(sqlite3.Connection): Connection to the database
    current_player(list): List with the data of the current player
    """
    test.leaderboard_holder = tk.Frame(test,
                                       bg = BG_APP)
    test.leaderboard_holder.pack(anchor = "center",
                                 fill = "both",
                                 pady = 10)
    
    test.leaderboard_holder.grid_columnconfigure(0, minsize = 50)
    test.leaderboard_holder.grid_columnconfigure(1, minsize = 113)
    test.leaderboard_holder.grid_columnconfigure(list(range(2, 4)), minsize = 100)

    rank_column = tk.Label(test.leaderboard_holder,
                           text = "Rank",
                           font = ("Arial", 12, "bold"),
                           fg = FG,
                           bg = BG_LEADERBOARD_ODD,
                           border = 1,
                           relief = "solid")
    rank_column.grid(row = 0,
                     column = 0,
                     sticky = "nsew")

    player_column = tk.Label(test.leaderboard_holder,
                             text = "Player",
                             font = ("Arial", 12, "bold"),
                             fg = FG,
                             bg = BG_LEADERBOARD_EVEN,
                             border = 1,
                             relief = "solid")
    player_column.grid(row = 0,
                       column = 1,
                       sticky = "nsew")
    
    consecutive_wins_column = tk.Label(test.leaderboard_holder,
                                       text = "Win Streak",
                                       font = ("Arial", 12, "bold"),
                                       fg = FG,
                                       bg = BG_LEADERBOARD_ODD,
                                       border = 1,
                                       relief = "solid")
    consecutive_wins_column.grid(row = 0,
                                 column = 2,
                                 sticky = "nsew")
    
    score_column = tk.Label(test.leaderboard_holder,
                            text = "Score",
                            font = ("Arial", 12, "bold"),
                            fg = FG,
                            bg = BG_LEADERBOARD_EVEN,
                            border = 1,
                            relief = "solid")
    score_column.grid(row = 0,
                      column = 3,
                      sticky = "nsew")
    
    top_players = get_top_ten(test, connection)
    populate_leaderboard(test, test.leaderboard_holder, top_players, current_player)

 
def populate_leaderboard(self, master: tk.Frame, top_players: list, current_player: list):
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
        medal = check_medal(i)

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
                               bg = BG_LEADERBOARD_ODD,
                               border = 1,
                               relief = "solid")
        rank_column.grid(row = i,
                         column = 0,
                         sticky = "nsew")

        player_column = tk.Label(master,
                                 text = "You" if is_current else player,
                                 font = ("Arial", 12, "bold"),
                                 fg = "Blue" if is_current else FG,
                                 bg = BG_LEADERBOARD_EVEN,
                                 border = 1,
                                 relief = "solid")
        player_column.grid(row = i,
                           column = 1,
                           sticky = "nsew")
        
        consecutive_wins_column = tk.Label(master,
                                           text = consecutive_wins,
                                           font = ("Arial", 12, "bold"),
                                           fg = FG,
                                           bg = BG_LEADERBOARD_ODD,
                                           border = 1,
                                           relief = "solid")
        consecutive_wins_column.grid(row = i,
                                     column = 2,
                                     sticky = "nsew")
        
        score_column = tk.Label(master,
                                text = score,
                                font = ("Arial", 12, "bold"),
                                fg = FG,
                                bg = BG_LEADERBOARD_EVEN,
                                border = 1,
                                relief = "solid")
        score_column.grid(row = i,
                          column = 3,
                          sticky = "nsew")
    self.last_rank_score = score
    