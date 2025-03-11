import tkinter as tk
from tkinter import messagebox
import time

# Digits of Pi
PI_DIGITS = """1415926535 8979323846 2643383279 5028841971 6939937510 5820974944 5923078164 0628620899 8628034825 3421170679 4610126483 6999892256 9596881592 0560010165 5256375679""".replace(" ","", -1).replace('\n','',-1)

class PiMemorizationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Memorization Game")
        self.root.configure(bg="#1E1E2E")  # Set background color
        
        self.teams = ["Team A", "Team B", "Team C", "Team D"]
        self.scores = {team: 0 for team in self.teams}
        self.current_team = 0
        self.digits_to_add = 2  # Start with 3.14
        self.start_time = None  # Track start time
        self.time_records = {team: [] for team in self.teams}  # Store time records
        
        self.frame = tk.Frame(root, bg="#1E1E2E")
        self.frame.pack(expand=True)
        
        self.label = tk.Label(self.frame, text="Memorize the next digits of π!", font=("Arial", 14), bg="#1E1E2E", fg="#CDD6F4")
        self.label.pack(pady=10)
        
        self.pi_display = tk.Label(self.frame, text="", font=("Courier", 18), bg="#1E1E2E", fg="#F5E0DC")
        self.pi_display.pack(pady=10)
        
        self.entry = tk.Entry(self.frame, font=("Arial", 14), state=tk.DISABLED, bg="#313244", fg="#CDD6F4", insertbackground="#F5E0DC", justify="center")
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.check_guess())  # Bind Enter key
        
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.check_guess, state=tk.DISABLED, bg="#A6E3A1", fg="#1E1E2E")
        self.submit_button.pack(pady=10)
        
        self.score_label = tk.Label(self.frame, text=self.get_score_text(), font=("Arial", 12), bg="#1E1E2E", fg="#89B4FA")
        self.score_label.pack(pady=10)
        
        self.message_label = tk.Label(self.frame, text="", font=("Arial", 12), bg="#1E1E2E", fg="#A6E3A1")
        self.message_label.pack(pady=10)
        
        self.current_sequence = "3."  # Start with 3.14
        self.current_index = 0  # Start tracking after "3."
        self.more_digits = 2
        
        self.start_round()
        
    def get_score_text(self):
        return "  |  ".join([f"{team}: {score:.2f}" for team, score in self.scores.items()])
    
    def start_round(self):
        new_digits = PI_DIGITS[self.current_index:self.current_index + self.more_digits]
        self.current_sequence = "3." + PI_DIGITS[:self.current_index + self.more_digits]
        self.pi_display.config(text=self.current_sequence)
        self.root.after((self.digits_to_add + 1) * 1000, self.hide_digits)
    
    def hide_digits(self):
        hidden_sequence = "3." + "_" * (len(self.current_sequence) - self.more_digits)
        self.pi_display.config(text=hidden_sequence)
        self.entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.start_time = time.time()
    
    def check_guess(self):
        elapsed_time = time.time() - self.start_time
        self.time_records[self.teams[self.current_team]].append(elapsed_time)
        
        guess = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        correct_sequence = self.current_sequence[2:]
        
        if guess == correct_sequence:
            self.current_index += self.more_digits
            self.digits_to_add += self.more_digits
            self.scores[self.teams[self.current_team]] += 1 * (1 / elapsed_time)
            self.message_label.config(text=f"Great job! You took {elapsed_time:.2f} seconds.", fg="#A6E3A1")
        else:
            self.message_label.config(text="Incorrect sequence! Switching teams.", fg="#F38BA8")
            self.current_team = (self.current_team + 1) % len(self.teams)
        
        if self.current_index >= len(PI_DIGITS):
            winner = max(self.scores, key=self.scores.get)
            self.message_label.config(text=f"{winner} wins with {self.scores[winner]:.2f} points!", fg="#A6E3A1")
            self.show_time_records()
            self.root.quit()
        
        self.score_label.config(text=self.get_score_text())
        self.label.config(text=f"{self.teams[self.current_team]}, memorize and enter the full sequence of π so far!")
        
        self.entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.start_round()
    
    def show_time_records(self):
        time_summary = "\n".join([f"{team}: {sum(times)/len(times):.2f} sec avg ({len(times)} rounds)" if times else f"{team}: No data" for team, times in self.time_records.items()])
        self.message_label.config(text=f"Time Taken Per Team:\n{time_summary}", fg="#A6E3A1")

if __name__ == "__main__":
    root = tk.Tk()
    game = PiMemorizationGame(root)
    root.mainloop()

