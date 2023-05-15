import tkinter as tk


def create_boxes(self, app_window: tk.Tk) -> list:
    """Creates the boxes for the user to guess the number
    
    Parameters:
    app_window(tk.Tk): Window holding the frame

    Returns:
    rows(list): List containing the boxes created
    """
    boxes_holder = tk.Label(self,
                            bg = "#6e5c62")
    boxes_holder.pack(anchor = "n")

    validation_command = app_window.register(self._validate_entry)

    rows = [[] for _ in range(6)]
    for i in range(6):
        for j in range(5):
            box = tk.Entry(boxes_holder,
                           font = ("Arial", 14),
                           justify = "center",
                           fg = "White",
                           bg = "#615458",
                           width = 3,
                           border = 0,
                           highlightthickness = 4,
                           highlightbackground = "#615458",
                           state = "disabled",
                           validate = "key",
                           validatecommand=(validation_command, '%P'))
            box.configure(disabledforeground = box["fg"],
                          disabledbackground = box["bg"])
            box.grid(padx = 2,
                        pady = 3,
                        row = i+1,
                        column = j,
                        sticky = "ns")
            rows[i].append(box)

    for boxes in rows:
        for box in boxes:
            box.bind("<KeyPress>", self._focus_next_box)
            box.bind("<BackSpace>", self._focus_previous)

    for box in rows[0]:
        box.configure(state = "normal",
                      bg = "#6e5c62",
                      highlightbackground = "#4c4347",
                      highlightcolor = "#4c4347")

    return rows


def update_boxes(self, rows: list, next_row: None = True):
    """Disables the boxes in the guess row and unlocks the boxes in the next if the number wasn't guessed
    
    Parameters:
    rows(list): List of rows with the boxes from the player guess
    next_row(bool): Tells the function if the next row should or not be unlocked
    """
    for box in rows[self.guess_row]:
        box.configure(disabledbackground = box["bg"],
                      state = "disable")
        
    self.guess_row += 1
    if next_row == True:
        for box in rows[self.guess_row]:
            box.configure(state = "normal",
                          bg = "#6e5c62",
                          highlightbackground = "#4c4347",
                          highlightcolor = "#4c4347")
