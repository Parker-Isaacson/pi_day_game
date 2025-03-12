import tkinter as tk
from tkinter import messagebox
import time

# Digits of Pi
PI_DIGITS = "141592653589793238462643383279502884197"  # Extended Pi digits

class PiMemorizationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Memorization Game")
        
        self.teams = ["Team A", "Team B"]
        self.scores = {team: 0 for team in self.teams}
        self.current_team = 0
        self.digits_to_add = 2  # Start with 3.14
        self.start_time = None  # Track start time
        self.time_records = {team: [] for team in self.teams}  # Store time records
        
        self.label = tk.Label(root, text="Memorize the next digits of π!", font=("Arial", 14))
        self.label.pack()
        
        self.pi_display = tk.Label(root, text="", font=("Courier", 18))
        self.pi_display.pack()
        
        self.entry = tk.Entry(root, font=("Arial", 14), state=tk.DISABLED)
        self.entry.pack()
        
        self.submit_button = tk.Button(root, text="Submit", command=self.check_guess, state=tk.DISABLED)
        self.submit_button.pack()
        
        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 12))
        self.score_label.pack()
        
        self.current_sequence = "3."  # Start with 3.14
        self.current_index = 0  # Start tracking after "3."
        self.more_digits = 2
        
        self.start_round()
        
    def get_score_text(self):
        return "  |  ".join([f"{team}: {score:.2f}" for team, score in self.scores.items()])
    
    def start_round(self):
        # Append new digits for the round
        new_digits = PI_DIGITS[self.current_index:self.current_index + self.more_digits]
        self.current_sequence = "3." + PI_DIGITS[:self.current_index + self.more_digits]
        self.pi_display.config(text=self.current_sequence)
        
        # Hide digits after 1 second per digit
        self.root.after((self.digits_to_add + 1) * 1000, self.hide_digits)
    
    def hide_digits(self):
        hidden_sequence = "3." + "_" * (len(self.current_sequence) - self.more_digits)
        self.pi_display.config(text=hidden_sequence)
        self.entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.start_time = time.time()  # Start timing when input is enabled
    
    def check_guess(self):
        elapsed_time = time.time() - self.start_time  # Calculate elapsed time
        self.time_records[self.teams[self.current_team]].append(elapsed_time)
        
        guess = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        correct_sequence = self.current_sequence[2:]  # Remove "3." for checking
        
        if guess == correct_sequence:
            self.current_index += self.more_digits
            self.digits_to_add += self.more_digits
            self.scores[self.teams[self.current_team]] += 1 * (1 / elapsed_time)
            messagebox.showinfo("Correct!", f"Great job! You took {elapsed_time:.2f} seconds. Next round.")
        else:
            messagebox.showinfo("Wrong Guess", "Incorrect sequence! Switching teams.")
            self.current_team = (self.current_team + 1) % len(self.teams)
        
        if self.current_index >= len(PI_DIGITS):
            winner = max(self.scores, key=self.scores.get)
            messagebox.showinfo("Game Over", f"{winner} wins with {self.scores[winner]:.2f} points!")
            self.show_time_records()
            self.root.quit()
        
        self.score_label.config(text=self.get_score_text())
        self.label.config(text=f"{self.teams[self.current_team]}, memorize and enter the full sequence of π so far!")
        
        self.entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.start_round()
    
    def show_time_records(self):
        time_summary = "\n".join([f"{team}: {sum(times)/len(times):.2f} sec avg ({len(times)} rounds)" if times else f"{team}: No data" for team, times in self.time_records.items()])
        messagebox.showinfo("Time Records", f"Time Taken Per Team:\n{time_summary}")

if __name__ == "__main__":
    root = tk.Tk()
    game = PiMemorizationGame(root)
    root.mainloop()

