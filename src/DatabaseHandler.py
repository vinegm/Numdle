import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import sqlite3


def create_leaderboard(connection: sqlite3.Connection):
    """Creates the table of the leaderboard if it doesn't exist
    
    Parameters:
    connection(sqlite3.Connection): Connection to the database
    """
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS leaderboard (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   player VARCHAR NOT NULL UNIQUE,
                   score INTEGER NOT NULL,
                   consecutive_wins INTEGER NOT NULL
                   )""")
    cursor.close()


def create_player(player: str, connection: sqlite3.Connection):
    """Creates a player on the database
    
    Parameters:
    player(str): Nickname of the player that will be created
    connection(connection: sqlite3.Connection): Connection to the database
    """
    cursor = connection.cursor()

    cursor.execute("INSERT INTO leaderboard (player, score, consecutive_wins) VALUES (?, ?, ?)", (player, 0, 0))
    connection.commit()

    cursor.close()


def change_player(self, rows: list, leaderboard: tk.Frame, connection: sqlite3.Connection, window: tk.Tk):
    """Changes the current player
    
    Parameters:
    rows(list): List of rows with the boxes from the player guess
    leaderboard(tk.Frame): Frame holding the leaderboard
    connection(sqlite3.Connection): Connection to the database
    window(tk.Tk): Window of the game
    """
    player = simpledialog.askstring("Who are you?", f"Currently playing as: {self.player[1]}\nType a different nickname to\nchange player (Limit of 7 characters):")
    # If the user didn't type a player
    if player == None or player == "":
        return
    
    # If the user typed a player nick that is too long
    if len(player) > 7:
        messagebox.showerror("Too Big!", "The nickname you tried is too big!")
        return
    
    update_status(self, leaderboard, connection, True)
    # Turns the player into a guest
    if player == "Guest" or player == "guest":
        self.player = [None, "Guest", 0, 0]
    # Gets the player from the database
    else:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM leaderboard WHERE player = ?""", (player,))
        result = cursor.fetchone()
        
        # Creates the player if he doesn't exist yet
        if result == None:
            create_player(player, connection)
            cursor.execute("""SELECT * FROM leaderboard WHERE player = ?""", (player,))
            result = cursor.fetchone()
        
        cursor.close()
        self.player = list(result)

    # Resets the score and win streak
    self.score = 0
    self.win_streak = 0

    # Updates the UI
    window.title(f"Numdle ({self.player[1]})")
    self._clear_ui(rows, leaderboard, connection, True)

    # Reloads the leaderboard
    leaderboard.reload_leaderboard(connection, self.player)
    leaderboard.reload_player(self.player)


def update_status(self, leaderboard: tk.Frame, connection: sqlite3.Connection, changing_player: bool = False):
    """Updates the current player status
    
    Parameters:
    leaderboard(tk.Frame): Frame holding the leaderboard
    connection(sqlite3.Connection): Connection to the database
    changing_player(bool): Tells the function if the player is being changed
    """
    # If the current player is a guest
    if self.player[1] == "Guest" or self.player[1] == "guest":
        return

    cursor = connection.cursor()

    update = False  # For keeping track if the player got a new record
    if self.player[2] < self.score and self.player[3] < self.win_streak:
        cursor.execute("""UPDATE leaderboard SET score = ?, consecutive_wins = ?  WHERE id = ?""", (self.score, self.win_streak, self.player[0]))
        self.player[2] = self.score
        self.player[3] = self.win_streak
        update = True

    elif self.player[2] < self.score:
        cursor.execute("""UPDATE leaderboard SET score = ?  WHERE id = ?""", (self.score, self.player[0]))
        self.player[2] = self.score
        update = True

    elif self.player[3] < self.win_streak:
        cursor.execute("""UPDATE leaderboard SET consecutive_wins = ?  WHERE id = ?""", (self.win_streak, self.player[0]))
        self.player[3] = self.win_streak
        update = True

    connection.commit()
    cursor.close()

    if not changing_player:
        # Updates the leaderboard if the player got new rank
        if (leaderboard.on_top_players and update) or (leaderboard.last_rank_score <= self.score):
            leaderboard.reload_leaderboard(connection, self.player)
            was_updated = True

        if update or was_updated:
            leaderboard.reload_player(self.player)


def get_top_ten(self, connection: sqlite3.Connection) -> list:
    """Gets the top 10 players from the database, based on score

    Parameters:
    connection(sqlite3.Connection): Connection to the database

    Returns:
    results(list): List of tuples containing the players data
    """
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM Leaderboard ORDER BY score DESC LIMIT 10""")
    results = cursor.fetchall()
    
    cursor.close()
    return results
