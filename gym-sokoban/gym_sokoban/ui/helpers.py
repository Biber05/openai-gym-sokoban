from tkinter import messagebox, Label, Button, Entry


# Add Text Fields, Inputs
def create_text_field(window, text: str, col: int, row: int, font=("Arial Bold", 10)):
    lbl = Label(window, text=text, font=font)
    lbl.grid(column=col, row=row)
    return window


def create_button(window, text: str, col: int, row: int, func, bg="gray", fg="black"):
    btn = Button(window, text=text, command=func, bg=bg, fg=fg)
    btn.grid(column=col, row=row)
    return window


def create_text_input(window, col: int, row: int, text_var=None):
    txt = Entry(window) if text_var is None else Entry(window, textvariable=text_var)
    txt.grid(column=col, row=row)
    return txt


# Logging
def show_info(info: str):
    messagebox.showinfo('Info', info)


def show_error(error: str):
    messagebox.showerror('Error', error)
