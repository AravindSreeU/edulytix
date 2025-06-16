import csv, statistics as st, tkinter as tk, sys, matplotlib.pyplot as plt, os, pickle
from tkinter import filedialog
import subprocess

teacher_remarks = ""

def get_subjects_from_csv(fp):
    with open(fp, newline='') as f:
        r = csv.DictReader(f)
        subs = [row['Subject'].strip().lower() for row in r]
        f.seek(0)
        lines = f.readlines()
        att = lines[1].split(",")[2].strip()
        name = next((l.split(",")[1].strip() for l in lines[1:] if l.split(",")[1].strip()), "")
        adone = {l.split(",")[3].strip().lower(): float(l.split(",")[9]) for l in lines[1:] if l.split(",")[9].strip().replace('.','',1).isdigit()}
        agiven = {l.split(",")[3].strip().lower(): float(l.split(",")[10]) for l in lines[1:] if l.split(",")[10].strip().replace('.','',1).isdigit()}
        apercent = {s: round(adone[s]/agiven[s]*100,2) for s in adone if s in agiven and agiven[s]}
        return list(set(subs)), att, apercent, name

def process_csv(fp, user_subs):
    with open(fp) as f: lines = [l.strip().split(",") for l in f.readlines()[1:] if l.strip()]
    sp = {}
    for l in lines:
        if len(l) < 9: continue
        subj = l[3].strip().lower()
        if subj not in user_subs: continue
        try: vals = [float(l[i]) for i in range(4,9)]
        except: continue
        perc = [round(vals[0]/40*100), round(vals[1]/40*100), round(vals[2]/80*100), round(vals[3]/40*100), round(vals[4]/80*100)]
        sp.setdefault(subj, []).append(perc)
    return sp

def plot_subjects_performance(sp):
    exams = ["MT1", "MT2", "TE1", "MT3", "TE2"]
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    for i, (subj, plist) in enumerate(sp.items()):
        avg = [sum(e[i] for e in plist)/len(plist) for i in range(5)]
        axes[i].plot(exams, avg, marker='o', color='b', label=subj)
        axes[i].set_title(subj.capitalize())
        axes[i].set_xlabel('Exams')
        axes[i].set_ylabel('Percentage')
        axes[i].grid(True)
        axes[i].legend()
    plt.tight_layout()
    p = os.path.join(os.path.dirname(__file__), "performance_plot.png")
    plt.savefig(p)
    plt.close()
    return p

def run():
    global teacher_remarks, doc_path

    # --- UI Setup ---
    root = tk.Tk()
    root.title("EduLytix - Scholastic Performance Analyzer")
    root.geometry("780x420")  # Increased size to fit the Guide row comfortably
    root.resizable(False, False)
    root.config(bg="#f0f0f0")
    selected_path, selected_choice, class_input, section_input, remarks_output = (tk.StringVar() for _ in range(5))

    def load_csv():
        nonlocal root
        global teacher_remarks
        f = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV Files", "*.csv")])
        if f:
            selected_path.set(f)
            teacher_remarks = remarks_textbox.get("1.0", "end-1c").strip()
            remarks_output.set(teacher_remarks)
            def show_popup_and_close():
                tk.messagebox.showinfo("Info", "CSV loaded successfully. The window will now close.")
                root.destroy()
            root.after(1000, show_popup_and_close)

    def set_default_path():
        global doc_path
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        doc_path = os.path.join(desktop, "Edulytix")
        # Optionally, create the directory if it doesn't exist
        if not os.path.exists(doc_path):
            os.makedirs(doc_path)

    def set_custom_path():
        global doc_path
        p = filedialog.askdirectory(title="Select a Directory")
        if p: doc_path = p

    def open_guide():
        guide_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../help/readme.txt"))
        if sys.platform.startswith("win"):
            os.startfile(guide_path)
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", guide_path])
        else:
            # Use nano as the default editor on Linux
            try:
                subprocess.Popen(["nano", guide_path])
            except FileNotFoundError:
                subprocess.call(["xdg-open", guide_path])

    tk.Label(root, text="Choose Stream:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, columnspan=4, pady=(15, 5))
    for i, s in enumerate(["Math/CS", "Bio/Math", "Pure Science", "Commerce"]):
        tk.Radiobutton(root, text=s, value=s, variable=selected_choice, bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=i, padx=10, pady=5)
    tk.Label(root, text="Class:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, pady=(10, 5), sticky="e")
    tk.Entry(root, textvariable=class_input, font=("Arial", 12), width=10).grid(row=2, column=1, pady=(10, 5), sticky="w")
    tk.Label(root, text="Section:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=2, pady=(10, 5), sticky="e")
    tk.Entry(root, textvariable=section_input, font=("Arial", 12), width=10).grid(row=2, column=3, pady=(10, 5), sticky="w")
    tk.Label(root, text="Teacher's Remarks:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, columnspan=4, pady=(10, 5))
    remarks_textbox = tk.Text(root, font=("Arial", 12), height=4, width=65)
    remarks_textbox.grid(row=4, column=0, columnspan=4, padx=10)
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.grid(row=5, column=0, columnspan=4, pady=20)
    tk.Label(button_frame, text="Choose Path for Report Document", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, columnspan=2, pady=(0, 10))
    tk.Label(button_frame, text="Provide File", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=3, padx=20)
    tk.Button(button_frame, text="Choose Default", command=set_default_path, bg="#007acc", fg="white", font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=5)
    tk.Button(button_frame, text="Choose Custom", command=set_custom_path, bg="#007acc", fg="white", font=("Arial", 12)).grid(row=2, column=1, padx=20, pady=5)
    tk.Button(button_frame, text="Load CSV", command=load_csv, bg="#007acc", fg="white", font=("Arial", 12)).grid(row=2, column=3, padx=20, pady=5)

    # --- Guide Row ---
    guide_frame = tk.Frame(root, bg="#f0f0f0")
    guide_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=10, pady=(10, 10))
    tk.Label(
        guide_frame,
        text='To access a complete understanding and detailed user instructions for this software, please click the Guide button.',
        font=("Arial", 10),
        bg="#f0f0f0",
        anchor="w",
        justify="left"
    ).pack(side="left", fill="x", expand=True)
    tk.Button(
        guide_frame,
        text="Guide",
        command=open_guide,
        bg="#007acc",
        fg="white",
        font=("Arial", 11),
        padx=15,
        pady=2
    ).pack(side="right", padx=10)

    root.mainloop()

    # --- Data Validation and Processing ---
    if not selected_path.get():
        # User closed the window or did not load a CSV, exit gracefully
        sys.exit(0)

    try:
        errors = []
        if not selected_choice.get(): errors.append("You must select a Stream before loading the CSV.")
        if not class_input.get(): errors.append("You must enter the Class before loading the CSV.")
        if not section_input.get(): errors.append("You must enter the Section before loading the CSV.")
        if not teacher_remarks or not teacher_remarks.strip(): errors.append("You must enter Teacher's Remarks before loading the CSV.")
        if 'doc_path' not in globals() or not doc_path: errors.append("You must select a path for saving the report document (Choose Default or Choose Custom).")
        if errors:
            print("\n❌ ERROR: The following issues were found:")
            for err in errors: print(" -", err)
            print("Please rerun the program and fill in all required fields.")
            sys.exit(1)
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
        user_input = selected_choice.get()
        valid_subject_sets = stream_subject_map.get(user_input, [])
        csv_subjects, attendance_percentage, assignment_data, student_name = get_subjects_from_csv(selected_path.get())
        if len(csv_subjects) != 6:
            print("❌ ERROR: CSV file must contain exactly 6 subjects.\nPlease rerun the program with a valid CSV file.")
            sys.exit(1)
        if not any(sorted(csv_subjects) == sorted(combo) for combo in valid_subject_sets):
            print("❌ ERROR: Selected stream and CSV subjects do not match.\nPlease rerun the program with correct stream and CSV.")
            sys.exit(1)
        subject_percentages = process_csv(selected_path.get(), csv_subjects)
        plot_subjects_performance(subject_percentages)
        averages = {s: st.mean(p[0]) for s, p in subject_percentages.items()}
        with open(os.path.join(os.path.dirname(__file__), "report_data.dat"), "wb") as fo:
            pickle.dump([student_name, class_input.get(), section_input.get(), attendance_percentage, assignment_data, teacher_remarks, averages, doc_path], fo)
    except Exception as e:
        print("\n❌ An error occurred:", str(e))
        print("Please check your inputs (stream, CSV file, remarks, or document path).")
        print("Rerun the program after fixing the issue.")
        sys.exit(1)