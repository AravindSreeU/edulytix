EduLytix - Scholastic Report Generator
=======================================

Overview:
---------
EduLytix is a Python-based project that generates a scholastic report for a student by processing a CSV file containing exam marks, attendance, and assignment completion details. The project validates the CSV data and then generates a detailed report using AI summarization and plots. The final report is output as a DOCX file.

Project Structure:
------------------
Edulytix/
├── edulib/
│   ├── main.py           # Handles CSV processing, GUI input, and graph generation.
│   ├── gemini_summary.py # Uses Google Generative AI to produce insights based on the report data.
│   └── compose.py        # Composes the final DOCX report with text details and the performance graph.
├── help/
│   └── sample.csv        # Sample CSV with required data. (Use this for the "Commerce" stream.)
└── execute.py            # Runs the entire project by sequentially executing the main tasks.

How It Works: (A example run-through)
-------------
1. Run the project:
   - Execute the command: 
       python3 execute.py
   - This script sequentially runs:
     • edulib/main.py (launches the GUI for data entry and CSV selection)
     • edulib/gemini_summary.py (generates the AI-based report summary)
     • edulib/compose.py (creates the final DOCX report)

2. In the GUI:
   - Choose your preferred stream. For the provided sample CSV, select "Commerce".
   - Enter the required student details (Name, Class, Section, etc.).
   - Click on "Load CSV" and choose the sample CSV file located at:
         Edulytix/help/sample.csv

3. CSV Validation:
   - The program validates the CSV file to ensure it contains exactly 6 subjects.
   - If the CSV file does not meet the criteria, an error message is displayed.
   - In such a case, fix the CSV or select a proper file and run the program again.

4. Report Generation:
   - After successful CSV validation, exam percentages and assignment data are calculated.
   - A performance graph is plotted and saved.
   - The project creates a binary data file (report_data.dat) with all the required inputs.
   - The AI (via Google Generative AI) produces a summary with insights, strengths, weaknesses, and suggestions.
   - Finally, a DOCX report is composed which includes:
     • Student and academic details
     • Assignment and attendance information
     • AI-generated summary text
     • Subject-wise performance graph (rotated)

5. Output:
   - The final report is saved in the parent folder of edulib, with the student’s name included in the filename (e.g., John_Report.docx).
   - A console message confirms the report location.

Requirements:
-------------
• Python 3.12 with required packages:
  - tkinter (for GUI)
  - matplotlib (for plotting)
  - pickle, csv, and os (standard libraries)
  - python-docx (for DOCX report generation)
  - Pillow (for image processing)
  - google-generativeai (for interacting with the Gemini AI model)
  
Make sure to install any missing packages via pip.

Usage Tips:
-----------
• You can change the stream and CSV file as per your requirements. 
• Ensure the CSV file has exactly 6 subjects; otherwise, the project will terminate with an error.
• Rerun the program if there is an error with the CSV file, after correcting the file.

Enjoy generating insightful scholastic reports with EduLytix!