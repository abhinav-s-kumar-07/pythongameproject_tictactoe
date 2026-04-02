from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title("Tic Tac Toe")
root.geometry("320x400")
root.resizable(True, True)  # allow resizing for maximize

buttons = [[None for _ in range(3)] for _ in range(3)]
player = "X"
mode = None  # 'PVP' or 'PVC'
label_turn = None
fullscreen = False  # Track fullscreen state

# ---------- Game Functions ----------

def check_winner(symbol):
    for i in range(3):
        if all(buttons[i][j]["text"] == symbol for j in range(3)):
            return True
        if all(buttons[j][i]["text"] == symbol for j in range(3)):
            return True
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] == symbol:
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] == symbol:
        return True
    return False

def check_draw():
    return all(buttons[r][c]["text"] != "" for r in range(3) for c in range(3))

def reset_board():
    global player
    player = "X"
    label_turn.config(text="Player X's Turn")
    for r in range(3):
        for c in range(3):
            buttons[r][c]["text"] = ""
            buttons[r][c]["state"] = NORMAL

def computer_move_event():
    empty = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
    if empty:
        move = random.choice(empty)
        buttons[move[0]][move[1]]["text"] = "O"
        if check_winner("O"):
            messagebox.showinfo("Game Over", "Computer Wins!")
            reset_board()
            return
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a Draw!")
            reset_board()
            return
        label_turn.config(text="Player X's Turn")

def on_click(r, c):
    global player
    if buttons[r][c]["text"] == "":
        buttons[r][c]["text"] = player
        if check_winner(player):
            messagebox.showinfo("Game Over", f"Player {player} Wins!")
            reset_board()
            return
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a Draw!")
            reset_board()
            return

        if mode == "PVP":
            player = "O" if player == "X" else "X"
            label_turn.config(text=f"Player {player}'s Turn")
        else:
            label_turn.config(text="Computer's Turn...")
            root.after(300, computer_move_event)

# ---------- GUI Functions ----------

def start_game(selected_mode):
    global mode
    mode = selected_mode
    for widget in root.winfo_children():
        widget.destroy()
    load_game_screen()

def load_start_screen():
    Label(root, text="Tic Tac Toe", font=("Arial", 20, "bold")).pack(pady=20)
    Label(root, text="Choose Game Mode", font=("Arial", 14)).pack(pady=10)
    Button(root, text="🎮 Player vs Player", font=("Arial", 12), width=20, bg="blue", fg="white",
           command=lambda: start_game("PVP")).pack(pady=10)
    Button(root, text="💻 Player vs Computer", font=("Arial", 12), width=20, bg="green", fg="white",
           command=lambda: start_game("PVC")).pack(pady=10)

def load_game_screen():
    global label_turn
    Label(root, text="Tic Tac Toe", font=("Arial", 18, "bold")).pack(pady=10)
    label_turn = Label(root, text="Player X's Turn", font=("Arial", 12))
    label_turn.pack()
    frame = Frame(root)
    frame.pack(pady=10)

    for r in range(3):
        for c in range(3):
            buttons[r][c] = Button(frame, text="", font=("Arial", 20, "bold"), width=5, height=2,
                                   command=lambda row=r, col=c: on_click(row, col))
            buttons[r][c].grid(row=r, column=c)

    Button(root, text="Reset Game", bg="red", fg="white", font=("Arial", 12, "bold"),
           command=reset_board).pack(pady=10)
    Button(root, text="← Back to Menu", bg="gray", fg="white", font=("Arial", 11),
           command=restart_to_menu).pack()

def restart_to_menu():
    for widget in root.winfo_children():
        widget.destroy()
    load_start_screen()

# ---------- Event Bindings ----------

def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

def exit_program(event=None):
    root.destroy()

root.bind("<Escape>", exit_program)      # ESC to exit
root.bind("<F11>", toggle_fullscreen)    # F11 to toggle fullscreen

# ---------- Start Menu ----------
load_start_screen()
root.mainloop()
