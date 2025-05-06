import csv
import statistics as st
import tkinter as tk
from tkinter import filedialog
import sys
import matplotlib.pyplot as plt
import os
import pickle

# Get subjects from CSV file
def get_subjects_from_csv(file_path):
    global attendance_percentage, assignment_data, student_name
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        subjects = [row['Subject'].strip().lower() for row in reader]

        # Reset pointer and read raw lines
        csvfile.seek(0)
        lines = csvfile.readlines()
        attendance = lines[1].strip().split(",")[2]

        assignments_done = {}
        assignments_given = {}
        student_name = ""

        for line in lines[1:]:
            columns = line.strip().split(",")

            # Grab student name only if not already set and column[1] is not empty
            if not student_name and len(columns) > 1 and columns[1].strip():
                student_name = columns[1].strip()

            subject = columns[3].strip().lower()
            try:
                done = float(columns[9])
                given = float(columns[10])

                if given != 0:
                    assignments_done[subject] = done
                    assignments_given[subject] = given
            except ValueError:
                continue

        assignment_percentages = {}
        for subject in assignments_done:
            if subject in assignments_given:
                percentage = (assignments_done[subject] / assignments_given[subject]) * 100
                assignment_percentages[subject] = round(percentage, 2)

        attendance_percentage = attendance.strip()
        assignment_data = assignment_percentages

        return list(set(subjects))

# Read and process CSV file for marks and subjects
def process_csv(file_path, user_subjects):
    with open(file_path, "r") as file:
        lines = file.readlines()

    data_lines = [line.strip().split(",") for line in lines[1:] if line.strip()]
    subject_percentages = {}
    current_name = ""

    for line in data_lines:
        if len(line) < 9:
            continue  # Skip incomplete lines

        if line[0]:  # New student row
            current_name = line[1]
            subject = line[3].strip().lower()
        else:
            subject = line[3].strip().lower()

        if subject not in user_subjects:
            continue  # Ignore irrelevant subjects

        try:
            mt1 = float(line[4])
            mt2 = float(line[5])
            term1 = float(line[6])
            mt3 = float(line[7])
            term2 = float(line[8])
        except ValueError:
            continue  # Skip invalid rows

        percentages = [
            round((mt1 / 40) * 100),  # MT1
            round((mt2 / 40) * 100),  # MT2
            round((term1 / 80) * 100),  # TE1
            round((mt3 / 40) * 100),  # MT3
            round((term2 / 80) * 100),  # TE2
        ]

        if subject not in subject_percentages:
            subject_percentages[subject] = []
        subject_percentages[subject].append(percentages)

    # Return the exam-wise percentage data
    return subject_percentages

# File selection and processing logic
def load_csv():
    global teacher_remarks
    selected_csv_file = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    if selected_csv_file:
        selected_path.set(selected_csv_file)
        # Get the remarks before destroying the window
        teacher_remarks = remarks_textbox.get("1.0", "end-1c").strip()
        remarks_output.set(teacher_remarks)
        root.destroy()

# Function to plot the subject-wise performance across exams and save as PNG
def plot_subjects_performance(subject_percentages):
    exams = ["MT1", "MT2", "TE1", "MT3", "TE2"]

    # Create a figure for the subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))  # 2 rows, 3 columns for 6 subjects
    axes = axes.flatten()

    for i, (subject, percentages_list) in enumerate(subject_percentages.items()):
        avg_percentages = [sum(exam[i] for exam in percentages_list) / len(percentages_list) for i in range(5)]

        axes[i].plot(exams, avg_percentages, marker='o', color='b', linestyle='-', label=subject)
        axes[i].set_title(subject.capitalize())
        axes[i].set_xlabel('Exams')
        axes[i].set_ylabel('Percentage')
        axes[i].grid(True)
        axes[i].legend()

    plt.tight_layout()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "performance_plot.png")
    plt.savefig(save_path)
    plt.close()

    return save_path

# GUI Setup
root = tk.Tk()
root.title("EduLytix - Scholastic Performance Analyzer")
root.geometry("600x320")
root.config(bg="#f0f0f0")

selected_path = tk.StringVar()
selected_choice = tk.StringVar()
class_input = tk.StringVar()
section_input = tk.StringVar()
remarks_output = tk.StringVar()

# Labels and Inputs
tk.Label(root, text="Choose Stream:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, columnspan=4, pady=(15, 5))

tk.Radiobutton(root, text="Math/CS", value="Math/CS", variable=selected_choice, bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
tk.Radiobutton(root, text="Bio/Math", value="Bio/Math", variable=selected_choice, bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5)
tk.Radiobutton(root, text="Pure Science", value="Pure Science", variable=selected_choice, bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=5)
tk.Radiobutton(root, text="Commerce", value="Commerce", variable=selected_choice, bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=3, padx=10, pady=5)

tk.Label(root, text="Class:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, pady=(10, 5), sticky="e")
tk.Entry(root, textvariable=class_input, font=("Arial", 12), width=10).grid(row=2, column=1, pady=(10, 5), sticky="w")

tk.Label(root, text="Section:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=2, pady=(10, 5), sticky="e")
tk.Entry(root, textvariable=section_input, font=("Arial", 12), width=10).grid(row=2, column=3, pady=(10, 5), sticky="w")

remarks_label = tk.Label(root, text="Teacher's Remarks:", font=("Arial", 12), bg="#f0f0f0")
remarks_label.grid(row=3, column=0, columnspan=4, pady=(10, 5))
remarks_textbox = tk.Text(root, font=("Arial", 12), height=4, width=65)
remarks_textbox.grid(row=4, column=0, columnspan=4, padx=10)
tk.Button(root, text="Load CSV", command=load_csv, bg="#007acc", fg="white", font=("Arial", 12)).grid(row=5, column=0, columnspan=4, pady=15)
root.mainloop()

# Subject stream mapping
stream_subject_map = {
    "Math/CS": [["math", "english", "physics", "chemistry", "computer science", "skill"]],
    "Bio/Math": [["math", "english", "physics", "chemistry", "biology", "skill"]],
    "Pure Science": [
        ["physics", "chemistry", "biology", "english", "psychology", "skill"],
        ["physics", "chemistry", "biology", "english", "computer science", "skill"]
    ],
    "Commerce": [
        ["math", "english", "accountancy", "business studies", "economics", "skill"],
        ["computer science", "english", "accountancy", "business studies", "economics", "skill"]
    ]
}

# Main logic after GUI
user_input = selected_choice.get()
valid_subject_sets = stream_subject_map.get(user_input, [])

selected_csv_file = selected_path.get()
csv_subjects = get_subjects_from_csv(selected_csv_file)

if len(csv_subjects) != 6:
    print("❌ ERROR: CSV file must contain exactly 6 subjects.")
    sys.exit()

if any(sorted(csv_subjects) == sorted(combo) for combo in valid_subject_sets):
    print("✅ Subjects match. Processing CSV file...")
    subject_percentages = process_csv(selected_csv_file, csv_subjects)
else:
    sys.exit()

subject_percentages = process_csv(selected_csv_file, csv_subjects)  # Use the subject-wise performance data from the process_csv function
graph_path = plot_subjects_performance(subject_percentages)  # Plot the graph and also save the graph in the variable
# subjects percentage as average
averages = {}
for subject, percentages in subject_percentages.items():
    averages[subject] = st.mean(percentages[0])

# Wrote the all data to binary file
edulib_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(edulib_dir, "report_data.dat")
with open(file_path, "wb") as fo: # All inputs are writen to an binary file
    pickle.dump([student_name, class_input.get(), section_input.get(), attendance_percentage, assignment_data, teacher_remarks, averages], fo)