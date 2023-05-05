"""
Guessing Number Game
 Inspired by wordle/termo
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
from numpy import random as rd


def generate_number():
    random_number = rd.randint(0, 10, 5)
    return random_number


class GuessingNumberGame(tk.Tk):
    """Window of the game"""
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Guessing Number Game")
        self.geometry("300x300")
        self.eval("tk::PlaceWindow . center")

        game_frame = Game (self)
        game_frame.pack(anchor = "n")


class Game(tk.Frame):
    """Frame where you can play and guess"""
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        header = tk.Label(self,
                          text = "Welcome to a Number Guessing Game!",
                          font = ("Arial", 12, "bold"))
        header.grid(pady = 20,
                    padx = 10,
                    row = 0,
                    column = 0, columnspan = 5,
                    sticky="n")

        validation_command = master.register(self._validate_entry)
        boxes = self._create_boxes(master)
    
    def _create_boxes(self, app_window):
        """Creates the boxes for the user to guess the number
        
        Parameters:
        app_window (tk.Tk): Window holding the frame

        Returns:
        Boxes (Array): Array containing the boxes created
        """
        validation_command = app_window.register(self._validate_entry)
        boxes = [[] for _ in range(6)]
        for i in range(6):
            for j in range(5):
                box = tk.Entry(self,
                            font = ("Arial", 12),
                            state = "disabled",
                            validate = "key",
                            validatecommand=(validation_command, '%P'))
                box.grid(padx = 5,
                        pady = 10,
                        row = i+1,
                        column = j,
                        sticky = "nsew")
                boxes[i].append(box)
        return boxes

    def _validate_entry(self, entry_text):
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


if __name__ == "__main__":
    app = GuessingNumberGame()
    app.mainloop()