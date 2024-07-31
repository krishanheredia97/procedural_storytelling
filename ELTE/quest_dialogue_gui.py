import tkinter as tk
from tkinter import ttk
import json
import random


def load_dialogue_data():
    with open('quest_dialogues.json', 'r') as file:
        return json.load(file)


def show_dialogue():
    stage = selected_stage.get()
    color = selected_color.get()

    if stage and (stage == 'opening' or color):
        if stage == 'opening':
            dialogues = dialogue_data['dialogues']['opening']
        else:
            dialogues = dialogue_data['dialogues'][stage][color]

        selected_dialogue = random.choice(dialogues)['text']
        dialogue_text.delete(1.0, tk.END)
        dialogue_text.insert(tk.END, selected_dialogue)
    else:
        dialogue_text.delete(1.0, tk.END)
        dialogue_text.insert(tk.END, "Please select both a stage and a color (except for opening).")


# Create the main window
root = tk.Tk()
root.title("Quest Dialogue Viewer")

# Load the JSON data
dialogue_data = load_dialogue_data()

# Create StringVar objects after root is initialized
selected_stage = tk.StringVar(root)
selected_color = tk.StringVar(root)

# Create and pack the dialogue text box
dialogue_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
dialogue_text.pack(pady=10)

# Create and pack the stage buttons
stage_frame = ttk.Frame(root)
stage_frame.pack(pady=5)

stages = ['Opening', 'Ongoing', 'Closing']
for stage in stages:
    ttk.Radiobutton(stage_frame, text=stage, value=stage.lower(), variable=selected_stage).pack(side=tk.LEFT, padx=5)

# Create and pack the color buttons
color_frame = ttk.Frame(root)
color_frame.pack(pady=5)

colors = ['Red', 'Yellow', 'Green', 'Cyan']
for color in colors:
    ttk.Radiobutton(color_frame, text=color, value=color.lower(), variable=selected_color).pack(side=tk.LEFT, padx=5)

# Create and pack the Show button
show_button = ttk.Button(root, text="Show", command=show_dialogue)
show_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()