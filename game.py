import tkinter as tk
from tkinter import messagebox
import time
import sys

# Digits of Pi
PI_DIGITS = """1415926535 8979323846 2643383279 5028841971 6939937510 5820974944 5923078164 0628620899 8628034825 3421170679 4610126483 6999892256 9596881592 0560010165 5256375679""".replace(" ", "").replace('\n', '')

class PiMemorizationGame:
    def __init__(self, root, teams):
        self.root = root
        self.root.title("Pi Memorization Game")
        self.root.configure(bg="#1E1E2E")

        self.teams = teams
        self.scores = {team: 0.0 for team in self.teams}
        self.current_team = 0
        self.digits_to_add = 2
        self.start_time = None
        
        self.frame = tk.Frame(root, bg="#1E1E2E")
        self.frame.pack(expand=True)
        
        self.label = tk.Label(self.frame, text="Memorize the next digits of π!", font=("Arial", 14), bg="#1E1E2E", fg="#CDD6F4")
        self.label.pack(pady=10)
        
        self.pi_display = tk.Label(self.frame, text="", font=("Courier", 18), bg="#1E1E2E", fg="#F5E0DC")
        self.pi_display.pack(pady=10)
        
        self.entry = tk.Entry(self.frame, font=("Arial", 14), state=tk.DISABLED, bg="#313244", fg="#CDD6F4", insertbackground="#F5E0DC", justify="center")
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.check_guess())
        
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.check_guess, state=tk.DISABLED, bg="#A6E3A1", fg="#1E1E2E")
        self.submit_button.pack(pady=10)
        
        self.score_label = tk.Label(self.frame, text=self.get_score_text(), font=("Arial", 12), bg="#1E1E2E", fg="#89B4FA")
        self.score_label.pack(pady=10)
        
        self.message_label = tk.Label(self.frame, text="", font=("Arial", 12), bg="#1E1E2E", fg="#A6E3A1")
        self.message_label.pack(pady=10)
        
        self.start_round()
        
    def get_score_text(self):
        return "  |  ".join([f"{team}: {score:.2f}" for team, score in self.scores.items()])
    
    def start_round(self):
        self.current_sequence = "3."
        self.current_index = 0
        self.show_next_digits()
    
    def show_next_digits(self):
        new_digits = PI_DIGITS[self.current_index:self.current_index + self.digits_to_add]
        self.current_sequence += new_digits
        self.pi_display.config(text=self.current_sequence)
        self.entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.root.after((self.digits_to_add + 1) * 1000, self.hide_digits)
    
    def hide_digits(self):
        hidden_sequence = "3." + "_" * (len(self.current_sequence) - 2)
        self.pi_display.config(text=hidden_sequence)
        self.entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.start_time = time.time()
    
    def check_guess(self):
        elapsed_time = time.time() - self.start_time
        guess = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        correct_sequence = self.current_sequence[2:]
        
        if guess == correct_sequence:
            score = 1 + (1 / elapsed_time)
            self.scores[self.teams[self.current_team]] += score
            self.score_label.config(text=self.get_score_text())
            self.message_label.config(text=f"Great job, {self.teams[self.current_team]}! You took {elapsed_time:.2f} seconds.", fg="#A6E3A1")
            self.current_index += self.digits_to_add
            self.show_next_digits()
        else:
            self.message_label.config(text=f"{self.teams[self.current_team]} is done!", fg="#F38BA8")
            self.current_team += 1
            if self.current_team >= len(self.teams):
                self.root.after(5000, self.end_game)
            else:
                self.entry.config(state=tk.DISABLED)
                self.submit_button.config(state=tk.DISABLED)
                self.root.after(2500, self.start_round)
                
    
    def end_game(self):
        winner = max(self.scores, key=self.scores.get)
        print("Final Scores:")
        for team, score in self.scores.items():
            print(f"{team}: {score:.2f}")
        self.message_label.config(text=f"{winner} wins with {self.scores[winner]:.2f} points!", fg="#A6E3A1")
        self.root.quit()
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 game.py <team1> <team2> ...")
        sys.exit(1)
    
    teams = sys.argv[1:]
    root = tk.Tk()
    game = PiMemorizationGame(root, teams)
    root.mainloop()

