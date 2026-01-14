import tkinter as tk
from tkinter import ttk
from music21 import *
import random
import matplotlib.pyplot as plt

keys = ["C", "D", "E", "F", "G", "A", "B", "C#", "D#", "F#", "G#", "A#"]
def generate_analyse(scale_name,step_prob,seed,key_name,write_midi=True,verbose=True):
    random.seed(seed)
    # ================#
    # MIDI GENERATOR #
    # ================#

    bar_num = 8
    beats_per_bar = 4
    beat_total = bar_num * beats_per_bar
    current_beat = 0
    low_oct = 3
    high_oct = 5
    durations = [1.0, 0.5]

    scale_options = {
        "major": scale.MajorScale,
        "natural minor": scale.MinorScale,
        "melodic minor": scale.MelodicMinorScale,
        "harmonic minor": scale.HarmonicMinorScale,
        "mixolydian": scale.MixolydianScale,
        "lydian": scale.LydianScale,
        "phrygian": scale.PhrygianScale,
        "dorian": scale.DorianScale,
    }
    tonic = key_name

    score = stream.Score()
    melody = stream.Part()
    melody.insert(0, instrument.Piano())
    melody.append(tempo.MetronomeMark(number=120))
    melody.append(meter.TimeSignature("4/4"))
    if "minor" in scale_name:
        melody.append(key.Key(key_name, "minor"))
    else:
        melody.append(key.Key(key_name, "major"))
    melody_scale = scale_options[scale_name](tonic)

    current_degree = random.randint(1, 7)
    step_moves = [-1, 1]
    leap_moves = [-3, -2, 2, 3]
    last_move = 0
    current_octave = random.randint(low_oct, high_oct)

    motif = []
    motif_length = 3
    motif_usage_prob = 0.3

    while current_beat < beat_total:
        duration = random.choice(durations)

        if current_beat + duration > beat_total:
            duration = beat_total - current_beat

        if motif and random.random() < motif_usage_prob:
            move = random.choice(motif)
        else:
            if random.random() < step_prob:
                move = random.choice(step_moves)
            else:
                move = random.choice(leap_moves)

        if random.random() < 0.2:
            move += random.choice([-1, 1])
            move = max(-3, min(3, move))

        if last_move != 0 and abs(move) > 1 and (move * last_move) < 0:
            move = -last_move

        if len(motif) < motif_length:
            motif.append(move)

        last_move = move
        next_degree = current_degree + move
        next_degree = max(1, min(7, next_degree))
        current_degree = next_degree
        pitch = melody_scale.pitchFromDegree(current_degree)
        octave_shift = random.choice([-1, 0, 0, 0, 1])
        current_octave = max(low_oct, min(high_oct, current_octave + octave_shift))
        pitch.octave = current_octave

        n = note.Note(pitch)
        n.duration.quarterLength = duration
        melody.append(n)

        current_beat += duration

    score.append(melody)
    if write_midi:
        filename = f"{key_name}_{scale_name}_step{round(step_prob,2)}_seed{seed}.mid"
        score.write("midi", filename)

    # ===================#
    # INTERVAL ANALYSIS #
    # ===================#

    notes = [n for n in melody.notes]
    midi_numbers = [n.pitch.midi for n in notes]

    intervals = []
    for i in range(len(midi_numbers) - 1):
        interval = abs(midi_numbers[i + 1] - midi_numbers[i])
        intervals.append(interval)

    steps = [i for i in intervals if i <= 2]
    leaps = [i for i in intervals if i > 2]
    step_count = len(steps)
    leap_count = len(leaps)
    total_intervals = len(intervals)
    step_ratio = step_count / total_intervals
    leap_ratio = leap_count / total_intervals
    mean_interval = sum(intervals) / len(intervals)

    if verbose:
        print("Scale:", scale_name)
        print("Total Notes:", len(notes))
        print("Total Intervals:", total_intervals)
        print("Steps:", step_count)
        print("Leaps:", leap_count)
        print("Step Ratio:", round(step_ratio, 3))
        print("Leap Ratio:", round(leap_ratio, 3))
        print("Mean Interval:", round(mean_interval, 3))

    return step_ratio, mean_interval

def gui():
    main = tk.Tk()
    main.title("Melodic Generator Controller")

    scale_var = tk.StringVar(value="major")
    step_prob_var = tk.DoubleVar(value=0.75)
    seed_var = tk.IntVar(value=0)

    ttk.Label(main, text="Scale").grid(row=0, column=0, padx=5, pady=5)
    scale_menu = ttk.Combobox(main, textvariable=scale_var, values=
    ["major", "natural minor", "melodic minor", "harmonic minor",
     "mixolydian", "lydian", "phrygian", "dorian"], state="readonly")
    scale_menu.grid(row=0, column=1)

    key_var = tk.StringVar(value="C")
    key_menu = ttk.Combobox(main, textvariable=key_var, values=keys, state="readonly")
    key_menu.grid(row=1, column=1)
    ttk.Label(main, text="Key").grid(row=1, column=0, padx=5, pady=5)

    ttk.Label(main, text="Step Probability").grid(row=2, column=0, padx=5, pady=5)
    step_slider = ttk.Scale(main, from_=0.0, to=1.0, variable=step_prob_var, orient="horizontal")
    step_slider.grid(row=2, column=1)

    ttk.Label(main, text="Random Seed").grid(row=3, column=0, padx=5, pady=5)
    seed_slider = ttk.Scale(main,from_=0,to=100,variable=seed_var,orient="horizontal")
    seed_slider.grid(row=3, column=1)

    summary_box = tk.Text(main, height=8, width=45, state="disabled")
    summary_box.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def update_summary(text):
        summary_box.config(state="normal")
        summary_box.delete("1.0", tk.END)
        summary_box.insert(tk.END, text)
        summary_box.config(state="disabled")

    def generate():
        step_ratio, mean_interval = generate_analyse(
            scale_name=scale_var.get(),
            step_prob=step_prob_var.get(),
            seed=int(seed_var.get()),
            key_name=key_var.get(),
            write_midi=True,
            verbose=False
        )

        filename = f"{key_var.get()}_{scale_var.get()}_step{round(step_prob_var.get(), 2)}_seed{seed_var.get()}.mid"

        summary = (
            "Melody Generated\n"
            "-----------------\n"
            f"Scale: {scale_var.get()}\n"
            f"Key: {key_var.get()}\n"
            f"Step Probability: {round(step_prob_var.get(), 2)}\n"
            f"Random Seed: {seed_var.get()}\n\n"
            f"Step Ratio: {round(step_ratio, 3)}\n"
            f"Mean Interval: {round(mean_interval, 3)}\n\n"
            f"Exported File:\n{filename}"
        )

        update_summary(summary)

    def run_experiments():
        major_family = ["major", "lydian", "mixolydian"]
        minor_family = ["natural minor", "dorian", "phrygian", "harmonic minor", "melodic minor"]
        plt.figure()
        for scale_name in major_family:
            plt.plot(step_probs, results[scale_name], marker="o", label=scale_name)

        plt.xlabel("Step Probability")
        plt.ylabel("Average Step Ratio")
        plt.title("Major-family Scales: Step Probability vs Melodic Motion")
        plt.legend()
        plt.grid(True)

        plt.figure()
        for scale_name in minor_family:
            plt.plot(step_probs, results[scale_name], marker="o", label=scale_name)
        plt.xlabel("Step Probability")
        plt.ylabel("Average Step Ratio")
        plt.title("Minor-family Scales: Step Probability vs Melodic Motion")
        plt.legend()
        plt.grid(True)
        plt.show()

    ttk.Button(main, text="Generate Melody",command=generate).grid(row=4,column=0,columnspan=2,pady=10)
    ttk.Button(main, text="Run Analysis",command=run_experiments).grid(row=5,column=0,columnspan=2,pady=5)

    main.mainloop()

step_probs = [0.6,0.75,0.9]
scales = ["major","natural minor","melodic minor","harmonic minor","mixolydian","lydian","phrygian","dorian"]
runs = 25
results = {scale: [] for scale in scales}

for scale_name in scales:
    for prob in step_probs:
        ratios = []
        for i in range(runs):
            step_ratio, mean_interval = generate_analyse(
                scale_name=scale_name,
                step_prob=prob,
                seed=i,
                key_name="C",
                write_midi = False,
                verbose = False
            )
            ratios.append(step_ratio)
        avg_ratio = sum(ratios) / len(ratios)
        results[scale_name].append(avg_ratio)

gui()

