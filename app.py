import os
from tkinter import *
from tkinter import filedialog
import pyperclip as pc

root = Tk()

# Customize the window
root.title("Water Molecules")
root.config(bg="#edf6f9")

root.iconbitmap("water-molecules.ico")

# Global variables
color_theme = StringVar()
color_theme.set("light")

file_types = [("Python file", "*.py"), ("Text file", "*.txt"), ("HTMl file", "*.html"), ("CSS file", "*.css"),
              ("Javascript file", "*.js")]
saved_or_not = False
filename = None
current_dir = None
final_dir = None


# Functions
def set_theme(mode):
    if mode == "dark":
        text.config(selectbackground="white", selectforeground="Sea green", bg="#2B2B2B", fg="light cyan")
        root.config(bg="##313335")
    else:
        text.config(selectbackground="Black", selectforeground="White", bg="white", fg="Black")
        root.config(bg="#F2F2F2")

def copy():
    # Checks if we selected any text
    if text.selection_get():
        # Copies it in the clipboard
        pc.copy(str(text.selection_get()))

def paste():
    # Gets keyboard cursor position
    position = text.index(INSERT)

    text.insert(position, pc.paste())

def cut():
    copy()
    text.delete("sel.first", "sel.last")

def new():
    text.delete(1.0, END)

    root.title("#New file - Water molecules")
    status_bar.config(bd=4, text="New file created (Unsaved)")

    global saved_or_not
    saved_or_not = False


def open_file():
    global saved_or_not, filename, current_dir, final_dir
    current_dir = os.getcwd()

    # Ask filedialog box
    file = filedialog.askopenfilename(title="Open file...", filetypes=file_types, defaultextension=file_types)

    # Permission to TRUE
    saved_or_not = True

    # Checks if file exists
    if file:
        filename = file.split("/")[-1]

        desired_directory = file.split("/")
        desired_directory = desired_directory[:-1]
        final_dir = ""
        for i in desired_directory:
            final_dir += f"{i}/"

        with open(file, "r") as f:
            text.insert(1.0, f.read())

        # Updates status bar
        status_bar.config(bd=4, text=f"{filename} has opened successfully")
        root.title(f"{filename} - Water molecule")


def save_as():
    global saved_or_not, final_dir, filename, current_dir

    # Permission to TRUE
    saved_or_not = True

    # Ask filedialog box
    file = filedialog.asksaveasfilename(title="Save as file...", filetypes=file_types, defaultextension=file_types)

    # Check if file exists
    if file:
        filename = file.split("/")[-1]

        # Changes directory to needed
        current_dir = os.getcwd()

        desired_directory = file.split("/")
        desired_directory = desired_directory[:-1]
        final_dir = ""
        for i in desired_directory:
            final_dir += f"{i}/"

        os.chdir(final_dir)

        # Makes the file
        f = open(filename, "w")
        f.close()

        # Updates status bar
        status_bar.config(bd=4, text=f"{filename} has been created and saved successfully")
        root.title(f"{filename} - Water molecule")

        # Resets the directory
        os.chdir(current_dir)


def save():
    global saved_or_not

    # Checks if the file is saved or not
    if saved_or_not:
        # Changes directory for file creation
        os.chdir(final_dir)

        # Saves the file
        with open(filename, "w") as f:
            f.write(text.get(1.0, END))

        # Goes back to original directory
        os.chdir(current_dir)

        # Updates status bars
        status_bar.config(bd=4, text=f"{filename} has been saved successfully")
        root.title(f"{filename} - Water molecules")

        # Sets "saved" variable to TRUE
        saved_or_not = True
    else:
        save_as()


def check_update_for_file():
    os.chdir(final_dir)

    with open(filename, "r") as f:
        text.delete(1.0, END)

        text.insert(1.0, f.read())


# Typing area
text = Text(root, width=108, height=30, selectbackground="Black", selectforeground="White", font=("Consolas", 17),
            undo=True)
text.pack(pady=5)

# Menu
menu = Menu(root, font=("Helvetica", 14))

file_sub_menu = Menu(menu, tearoff=0, font=("Helvetica", 12), bg="white smoke")
menu.add_cascade(label="File", menu=file_sub_menu)
file_sub_menu.add_command(label="Open", command=open_file)
file_sub_menu.add_command(label="Save", command=save)
file_sub_menu.add_command(label="Save as", command=save_as)
file_sub_menu.add_separator()
file_sub_menu.add_command(label="Update file", command=check_update_for_file)
file_sub_menu.add_command(label="New", command=new)

edit_sub_menu = Menu(menu, tearoff=0, font=("Helvetica", 12), bg="white smoke")
menu.add_cascade(label="Edit", menu=edit_sub_menu)
edit_sub_menu.add_command(label="Copy", command=copy)
edit_sub_menu.add_command(label="Paste", command=paste)
edit_sub_menu.add_command(label="Cut", command=cut)

theme_sub_menu = Menu(menu, tearoff=0, font=("Helvetica", 12), bg="white smoke")
menu.add_cascade(label="Themes", menu=theme_sub_menu)
theme_sub_menu.add_radiobutton(label="Dark", variable=color_theme, value="dark", command=lambda: set_theme("dark"))
theme_sub_menu.add_radiobutton(label="Light", variable=color_theme, value="light", command=lambda: set_theme("light"))

root.config(menu=menu)

# Status bar
status_bar = Label(root, text="Ready        ", padx=5, pady=5, anchor=E, font=("Tw cen mt", 13))
status_bar.pack(fill=X)

root.mainloop()
