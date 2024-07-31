import tkinter as tk
from tkinter import ttk
import json
import random

class QuestGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Quest Game")
        self.root.attributes('-fullscreen', True)

        self.load_data()
        self.setup_variables()
        self.create_widgets()
        self.next_question()
        self.root.bind('<Escape>', self.exit_fullscreen)

    def load_data(self):
        with open('quest_dialogues.json', 'r') as file:
            self.dialogue_data = json.load(file)
        with open('geography_questions.json', 'r') as file:
            self.question_data = json.load(file)
        with open('quest_progress_settings.json', 'r') as file:
            self.settings = json.load(file)

    def setup_variables(self):
        self.questions = self.question_data['questions']
        random.shuffle(self.questions)
        self.current_question_index = 0
        self.correct_answers = 0
        self.answered_questions = 0
        self.used_dialogues = set()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        left_frame = ttk.Frame(main_frame, padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame = ttk.Frame(main_frame, padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left frame widgets
        self.question_label = ttk.Label(left_frame, wraplength=600, font=("Arial", 20))
        self.question_label.pack(pady=20, expand=True)

        self.answer_buttons = []
        for i in range(4):
            btn = ttk.Button(left_frame, command=lambda x=i: self.check_answer(x), style='TButton')
            btn.pack(fill=tk.X, pady=10)
            self.answer_buttons.append(btn)

        self.result_label = ttk.Label(left_frame, text="Choose an answer", font=("Arial", 14))
        self.result_label.pack(pady=20)

        # Right frame widgets
        self.dialogue_text = tk.Text(right_frame, height=10, width=50, wrap=tk.WORD, font=("Arial", 20))
        self.dialogue_text.pack(pady=20, expand=True, fill=tk.BOTH)

        self.progress_bar = ttk.Progressbar(right_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=20)

        self.progress_circle = tk.Canvas(right_frame, width=100, height=100)
        self.progress_circle.pack(pady=20)

        self.answered_label = ttk.Label(right_frame, font=("Arial", 14))
        self.answered_label.pack()

        self.remaining_label = ttk.Label(right_frame, font=("Arial", 14))
        self.remaining_label.pack()

        # Configure style for larger buttons
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14))

    def next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question['question_text'])
            for i, btn in enumerate(self.answer_buttons):
                btn.config(text=question['answers'][i])
            self.result_label.config(text="Choose an answer")
            self.update_progress()
            self.show_dialogue()
        else:
            self.end_game()

    def check_answer(self, answer_index):
        question = self.questions[self.current_question_index]
        if answer_index + 1 == question['correct_answer']:
            self.result_label.config(text="Correct!", foreground="green")
            self.correct_answers += 1
        else:
            self.result_label.config(text="Incorrect", foreground="red")
        self.answered_questions += 1
        self.current_question_index += 1
        self.root.after(1000, self.next_question)

    def update_progress(self):
        progress = self.answered_questions / self.settings['total_questions']
        self.progress_bar['value'] = progress * 100

        success_rate = self.correct_answers / max(1, self.answered_questions)
        color = self.get_progress_color(success_rate)
        self.progress_circle.delete("all")
        self.progress_circle.create_oval(10, 10, 90, 90, fill=color)

        self.answered_label.config(text=f"Answered: {self.answered_questions}")
        remaining = self.settings['total_questions'] - self.answered_questions
        self.remaining_label.config(text=f"Remaining: {remaining}")

    def get_progress_color(self, rate):
        if rate >= self.settings['thresholds']['cyan']:
            return "cyan"
        elif rate >= self.settings['thresholds']['green']:
            return "green"
        elif rate >= self.settings['thresholds']['yellow']:
            return "yellow"
        else:
            return "red"

    def show_dialogue(self):
        if self.answered_questions == 0:
            stage = "opening"
            color = None
        elif self.answered_questions == self.settings['total_questions']:
            stage = "closing"
            color = self.get_progress_color(self.correct_answers / self.settings['total_questions'])
        elif self.answered_questions % 3 == 0:
            stage = "ongoing"
            color = self.get_progress_color(self.correct_answers / self.answered_questions)
        else:
            return

        if stage == "opening":
            dialogues = self.dialogue_data['dialogues']['opening']
        else:
            dialogues = self.dialogue_data['dialogues'][stage][color]

        available_dialogues = [d for d in dialogues if d['id'] not in self.used_dialogues]
        if available_dialogues:
            selected_dialogue = random.choice(available_dialogues)
            self.used_dialogues.add(selected_dialogue['id'])
            self.dialogue_text.delete(1.0, tk.END)
            self.dialogue_text.insert(tk.END, selected_dialogue['text'])
        else:
            self.dialogue_text.delete(1.0, tk.END)

    def end_game(self):
        self.question_label.config(text="Quest completed!")
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)
        self.result_label.config(text=f"Final score: {self.correct_answers}/{self.settings['total_questions']}")
        self.show_dialogue()

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        self.root.geometry("1000x600")


if __name__ == "__main__":
    root = tk.Tk()
    game = QuestGame(root)
    root.mainloop()