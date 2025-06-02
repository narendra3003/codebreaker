import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar, RIGHT, Y
from app.helpers import (
    generate_all_candidates, generate_secret_code,
    get_feedback, filter_candidates, calculate_color_probabilities_by_position
)
from app.settings import DEFAULT_COLORS, DEFAULT_CODE_LENGTH, DEFAULT_SLOT_COUNT

class CodeBreakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 CodeBreaker Game")
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        self.selected_color_count = len(DEFAULT_COLORS)
        self.selected_slots = DEFAULT_SLOT_COUNT
        self.colors = DEFAULT_COLORS[:self.selected_color_count]
        self.code_length = self.selected_slots
        self.color_probability_by_position = {}
        self.all_candidates = []
        self.current_candidates = []
        self.setup_game_variables()
        self.create_widgets()

    def setup_game_variables(self):
        self.colors = DEFAULT_COLORS[:self.selected_color_count]
        self.code_length = self.selected_slots
        self.all_candidates = generate_all_candidates(self.colors, self.code_length)
        self.current_candidates = self.all_candidates.copy()
        self.color_probability_by_position = {i: {c: 0 for c in self.colors} for i in range(self.code_length)}
        self.secret_code = generate_secret_code(self.colors, self.code_length)
        self.guess = []
        self.current_index = 0

    def create_widgets(self):
        tk.Label(self.root, text="Pick colors:").pack()

        self.guess_frame = tk.Frame(self.root)
        self.guess_frame.pack()
        self.peg_labels = []
        for _ in range(self.code_length):
            label = tk.Label(self.guess_frame, text="⬜", width=6, height=2, bg="lightgray")
            label.pack(side=tk.LEFT, padx=5)
            self.peg_labels.append(label)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
        self.color_buttons = []
        for i, c in enumerate(self.colors):
            b = tk.Button(self.button_frame, text=c, bg=c.lower(), fg="white", command=lambda i=i: self.select_color(i))
            b.pack(side=tk.LEFT, padx=2)
            self.color_buttons.append(b)

        self.submit_btn = tk.Button(self.root, text="✅ Submit", command=self.submit_guess, state=tk.DISABLED)
        self.submit_btn.pack(pady=5)

        tk.Button(self.root, text="↩️ Undo", command=self.cancel_last).pack(pady=3)
        tk.Button(self.root, text="🕵️ Reveal Code", command=self.reveal_secret).pack(pady=3)
        tk.Button(self.root, text="📊 Show Probabilities", command=self.show_probabilities).pack(pady=5)

        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=5)
        tk.Button(self.root, text="⚙️ Settings", command=self.settings_window).pack(pady=5)

    def reset_widgets(self):
        for widget in self.guess_frame.winfo_children():
            widget.destroy()
        self.peg_labels = []
        for _ in range(self.code_length):
            label = tk.Label(self.guess_frame, text="⬜", width=6, height=2, bg="lightgray")
            label.pack(side=tk.LEFT, padx=5)
            self.peg_labels.append(label)

        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.color_buttons = []
        for i, c in enumerate(self.colors):
            b = tk.Button(self.button_frame, text=c, bg=c.lower(), fg="white", command=lambda i=i: self.select_color(i))
            b.pack(side=tk.LEFT, padx=2)
            self.color_buttons.append(b)

    def select_color(self, index):
        if self.current_index < self.code_length:
            self.guess.append(self.colors[index])
            self.peg_labels[self.current_index].config(bg=self.colors[index].lower(), text=self.colors[index])
            self.current_index += 1
            if self.current_index == self.code_length:
                self.submit_btn.config(state=tk.NORMAL)

    def cancel_last(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.guess.pop()
            self.peg_labels[self.current_index].config(bg="lightgray", text="⬜")
            self.submit_btn.config(state=tk.DISABLED)

    def submit_guess(self):
        black, white = get_feedback(self.secret_code, self.guess)
        self.feedback_label.config(text=f"[Guess] {self.guess}  ->  Black Pegs: {black}, White Pegs: {white}")
        self.current_candidates = filter_candidates(self.current_candidates, self.guess, (black, white))
        if black == self.code_length:
            messagebox.showinfo("🎉 You Won!", "You cracked the code!")
            self.full_reset()
        else:
            self.reset_for_next()

    def reset_for_next(self):
        self.guess = []
        self.current_index = 0
        for label in self.peg_labels:
            label.config(bg="lightgray", text="⬜")
        self.submit_btn.config(state=tk.DISABLED)

    def reveal_secret(self):
        messagebox.showinfo("🕵️ Secret Code", f"The secret code was: {self.secret_code}")
        self.full_reset()

    def full_reset(self):
        self.setup_game_variables()
        self.reset_widgets()
        self.reset_for_next()
        self.feedback_label.config(text="")

    def settings_window(self):
        def apply_settings():
            self.selected_slots = slot_var.get()
            self.selected_color_count = color_var.get()
            self.full_reset()
            settings.destroy()

        settings = Toplevel(self.root)
        settings.title("⚙️ Game Settings")
        settings.geometry("300x200")

        tk.Label(settings, text="Slots (2-6):").pack(pady=5)
        slot_var = tk.IntVar(value=self.selected_slots)
        tk.Spinbox(settings, from_=2, to=6, textvariable=slot_var, width=5).pack()

        tk.Label(settings, text="Colors (4-10):").pack(pady=5)
        color_var = tk.IntVar(value=self.selected_color_count)
        tk.Spinbox(settings, from_=4, to=10, textvariable=color_var, width=5).pack()

        tk.Button(settings, text="Apply", command=apply_settings).pack(pady=10)

    def show_probabilities(self):
        self.color_probability_by_position = calculate_color_probabilities_by_position(
            self.current_candidates, self.code_length, self.colors
        )
        win = Toplevel(self.root)
        win.title("Color Probabilities by Position")
        text = Text(win, wrap=tk.WORD, font=("Courier", 10), height=15, width=60)
        scroll = Scrollbar(win, command=text.yview)
        text.config(yscrollcommand=scroll.set)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)

        for i in range(self.code_length):
            text.insert(tk.END, f"Position {i+1}:\n")
            for color, prob in self.color_probability_by_position[i].items():
                text.insert(tk.END, f"  {color:<8}: {prob:.2f}\n")
            text.insert(tk.END, "\n")
