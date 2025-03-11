import tkinter as tk
from tkinter import messagebox
import random

# Digits of Pi
PI_DIGITS = "1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"  # Corrected to start after '3.'

class PiGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Guessing Game")
        
        self.teams = ["Team A", "Team B", "Team C"]
        self.scores = {team: 0 for team in self.teams}
        self.current_team = 0
        self.current_index = 0
        
        self.label = tk.Label(root, text="Guess the next digit of π!", font=("Arial", 14))
        self.label.pack()
        
        self.pi_display = tk.Label(root, text="3.", font=("Courier", 18))
        self.pi_display.pack()
        
        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack()
        
        self.submit_button = tk.Button(root, text="Submit", command=self.check_guess)
        self.submit_button.pack()
        
        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 12))
        self.score_label.pack()
        
    def get_score_text(self):
        return "  |  ".join([f"{team}: {score}" for team, score in self.scores.items()])
    
    def check_guess(self):
        guess = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        if not guess.isdigit() or len(guess) != 1:
            messagebox.showwarning("Invalid Input", "Please enter a single digit.")
            return
        
        if guess == PI_DIGITS[self.current_index]:
            self.pi_display.config(text=f"3.{PI_DIGITS[:self.current_index+1]}")
            self.scores[self.teams[self.current_team]] += 1
            self.current_index += 1
        else:
            messagebox.showinfo("Wrong Guess", "Incorrect digit! Switching teams.")
            self.current_team = (self.current_team + 1) % len(self.teams)
        
        if self.current_index == len(PI_DIGITS):
            winner = max(self.scores, key=self.scores.get)
            messagebox.showinfo("Game Over", f"{winner} wins with {self.scores[winner]} points!")
            self.root.quit()
        
        self.score_label.config(text=self.get_score_text())
        self.label.config(text=f"{self.teams[self.current_team]}, guess the next digit of π!")

if __name__ == "__main__":
    root = tk.Tk()
    game = PiGuessingGame(root)
    root.mainloop()

