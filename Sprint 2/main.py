from game import start_game
import tkinter as tk
from ui import PegSolitaireUI

def main():
    root = tk.Tk()
    PegSolitaireUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
