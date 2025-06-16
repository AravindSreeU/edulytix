EduLytix - Scholastic Report Generator
=======================================

Overview:
---------
EduLytix is a Python-based project that generates a scholastic report for a student by processing a CSV file containing exam marks, attendance, and assignment completion details. The project validates the CSV data, generates a performance graph, and creates a detailed DOCX report which includes an AI-generated summary. The final report is saved at the specified document path.

Project Structure:
------------------
Edulytix/
├── edulib/
│   ├── main.py           - Handles CSV processing, GUI input, and graph generation.
│   ├── gemini_summary.py - Uses Google Generative AI to produce insights based on the report data.
│   ├── compose.py        - Composes the final DOCX report with text details and the performance graph.
│   └── clear.py          - Deletes temporary files and folders created during processing.
├── help/
│   └── sample.csv        - Sample CSV with required data. (Use this for the "Commerce" stream.)
└── execute.py            - Runs the entire project by sequentially executing the main tasks.

How It Works:
-------------
1. Run the project:
   - Execute the command: 
         python3 execute.py
   - This script sequentially runs:
     - edulib/main.py (launches the GUI for data entry, document path selection, and CSV selection)
     - edulib/gemini_summary.py (generates the AI-based report summary)
     - edulib/compose.py (creates the final DOCX report)
     - edulib/clear.py (cleans up temporary files and folders)

2. In the GUI:
   - Step 1: Choose the stream. For the sample CSV, select "Commerce".
   - Step 2: Enter the student's Class and Section
   - Step 3: Provide Teacher's Remarks.
   - Step 4: Click on "Choose Default" to save in Desktop/Edulytix in your computer or click on "Choose Custom" to select a custom folder.
   - Step 5: Load the CSV file by clicking on "Load CSV".For the provided sample CSV, select the file located at: Edulytix/help/sample.csv 

3. CSV Validation:
   - The program validates the CSV file to ensure it contains exactly 6 subjects.
   - If the CSV file does not meet the criteria, an error message is displayed.
   - In such a case, fix the CSV or select a proper file and run the program again.

4. Report Generation:
   - After successful CSV validation, exam percentages and assignment data are calculated.
   - A performance graph is plotted and saved.
   - All inputs are saved into a binary data file (report_data.dat).
   - The AI (via Google Generative AI) produces a summary with insights, strengths, weaknesses, and suggestions.
   - Finally, the DOCX report is composed which includes:
     - Student and academic details
     - Assignment and attendance information
     - AI-generated summary text
     - Subject-wise performance graph (rotated)
5. Output:
   - The final report is saved at the document path chosen by the user, with the student’s name in the filename (e.g., John_Report.docx).
   - A console message confirms the report location.

6. Cleanup:
   - After the report is generated, clear.py permanently deletes temporary files and the __pycache__ folder from the edulib directory.

Requirements:
-------------
Python 3.12 with required packages:
  - tkinter (for GUI)
  - matplotlib (for plotting)
  - pickle, csv, and os (standard libraries)
  - python-docx (for DOCX report generation)
  - Pillow (for image processing)
  - google-generativeai (for interacting with the Gemini AI model)
  
Make sure to install any missing packages via pip.

 IMPORTANT:
-----------
- If your in the Edulytix window then fill the required details requested, chose a path to store the Report as per your wish and then Click Load CSV. 
{REMEMBER TO ALWAYS CLICK LOAD CSV ONLY AFTER CHOOSING THE DESIGNATED PATH TO STORE THE REPORT}
- After clicking the Load CSV button you can navigate in the Pop-Up to Desktop/Edulytix Docs where you can find the sample.csv 
- To delete this application from your computer ..... do nothing

Enjoy generating insightful scholastic reports with EduLytix!
