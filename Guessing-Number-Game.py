"""
Guessing Number Game
 Inspired by wordle/termo
"""
import tkinter as tk
import numpy as np
from numpy import random as rd
import time

def generate_number():
    """Generates a array with 5 random numbers from 0 to 9"""
    random_number = np.array(rd.randint(1, 10, 1))
    random_number = np.append(random_number, rd.randint(0, 10, 4))
    print(random_number)  # Used for testing ONLY
    return random_number


class GuessingNumberGame(tk.Tk):
    """Window of the game"""
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Guessing Number Game")
        self.geometry("400x400")
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
        header.pack(anchor = "n",
                    pady = 20,
                    padx = 10)

        random_number = generate_number()
        boxes = self._create_boxes(master)

        self.guess_row = 0
        guess_button = tk.Button(self,
                                 text = "Guess",
                                 command = lambda: self._check_guess(boxes, random_number))
        guess_button.pack(anchor = "n")

    def _check_guess(self, boxes, random_number):
        """Checks the users guess"""     
        if self.guess_row >= 5:
            print("you lost!")
            return

        target = np.copy(random_number)
        correct_number = 0

        for i, box in enumerate(boxes[self.guess_row]):
            if int(box.get()) == target[i]:
                target[i] = -1
                correct_number += 1
                box.configure(bg = "Green")

        if correct_number == 5:
            print("You Guessed It!")
            return
        
        for box in boxes[self.guess_row]:
            for j in target:
                if int(box.get()) == j:
                    box.configure(bg = "Yellow")
                    break
        
        self.guess_row += 1
        self._update_boxes(boxes, self.guess_row)

    def _update_boxes(self, boxes, row):
        for box in boxes[row]:
            box.configure(state = "normal")
        for box in boxes[row-1]:
            box.configure(disabledbackground = box["bg"],
                          disabledforeground = box["fg"],
                          state = "disable")
    
    def _create_boxes(self, app_window):
        """Creates the boxes for the user to guess the number
        
        Parameters:
        app_window (tk.Tk): Window holding the frame

        Returns:
        Boxes (Array): Array containing the boxes created
        """
        validation_command = app_window.register(self._validate_entry)
        boxes_holder = tk.Label(self)
        boxes_holder.pack(anchor = "n")
        boxes = [[] for _ in range(6)]
        for i in range(6):
            for j in range(5):
                box = tk.Entry(boxes_holder,
                               font = ("Arial", 12),
                               justify = "center",
                               fg = "Black",
                               width = 5,
                               state = "disabled",
                               validate = "key",
                               validatecommand=(validation_command, '%P'))
                box.grid(padx = 5,
                         pady = 10,
                         row = i+1,
                         column = j,
                         sticky = "ns")
                boxes[i].append(box)
        for box in boxes[0]:
            box.configure(state = "normal")
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