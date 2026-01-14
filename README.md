**Project Overview:**

I have created a project which aims to explore the relationship between probability and musical outcomes. I have created a melody generator which creates melodies based on specific constraints, and uses interval analysis to retrieve their statistical properties. This project does not just create "random music", but models melodies mathematically, and analyses how control variables affect musical structures.

**Requirements:**

- PIPs (Tkinter, music21, matplotlib)
- Python 3.13 or above

**Constraints:**

To ensure each output can be analysed effectively, I will make sure the system runs under the following constraints:

- Output : One single melody line
- Fixed Tempo : 120 BPM for all melodies
- One instrument : Piano for all melodies
- Fixed Length : 8 Bar melodies
- Fixed Time Signature : Each melody will be in 4/4
- Fixed Note Durations : Notes will be only crotchets (quarter notes) and quavers (eighth notes)
- Fixed Pitch Range : MIDI range from C3 - C5
- Scale Selection : Major, Melodic/Harmonic/Natural Minor, Dorian, Lydian, Phrygian, Mixylodian

**Melody Generation:**

Each melody is generated using a degree-based scale system where:
- Notes are chosen by scale degree rather than pitch
- Melodic motion is controlled by steps and leaps, where a step = ±1 scale degree, and a leap = ±2 or ±3 degrees
- There is a fixed random seed, which ensures melody reproduction stays the same

**Interval Analysis:**

Each generated melody is analysed with the following statistics:

- Step Ratio = The proportion of intervals ≤ 2 semitones
- Leap Ratio = The proportion of intervals > 2 semitones
- Mean Interval Size = The average semitone movement in each melody
  
**Key findings:**

- Step probability and step ratio are directly proportional to one another
- Scale choice can subtly affects melodic motion undeer the same constraints
- Modal scales exhibit different interval characteristics under the same constraints

I used matplotlib to visualise the results, where the scales are split into major and minor families.

**GUI:**

I incorporated a Tkinter-Based GUI which allows the user to:
- Select scale and key
- Adjust step probability using sliders
- Set random seed for reproducibility
- Generate melodies and export a MIDI file
- View a summary export panel showing the key and scale, parameters, step ratio and mean interval, and the exported MIDI file location

**Future Improvements:**

I am exremely proud of this code as it has allowed me to combine my interests in music and quantitative researcb into one project. However there are a few things that I think I could imrpove next time on the design, such as:
- Allowing the user to control more variables, such as pitch range and bar length
- Extending the project to generate chords as opposed to one-line melodies
- Exporting the data as a CSV file
