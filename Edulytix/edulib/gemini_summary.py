import os
import sys
import google.generativeai as genai, pickle

def run():
    global output
    d = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(d, "report_data.dat")):
        sys.exit(0)

    with open(os.path.join(d, "report_data.dat"), "rb") as f: data = pickle.load(f)
    exam = ", ".join(f"{k}: {v}%" for k, v in data[6].items())
    assign = ", ".join(f"{k}: {v}%" for k, v in data[4].items())
    prompt = (f"A student named {data[0]} of class {data[1]} has an attendence percentage of {data[1]} and completed assignments of {assign} "
            f"and scored {exam}. This data is collected for the entire year and recorded. The student have written three monthly tests and 1 yearly and 1 annual test. "
            "Based on that data the overall percentage in each subject is given to you.\n"
            "With this information write 4 points under Insights, 3 points under Stregth, 3 points under Weaknesses and 4 points under suggestion for Improvemrnt. "
            "There shall be no bold words. Just provide me the text with spaces and reqquired lines to separate each topic.")

    genai.configure(api_key="AIzaSyDA91w7mb834mjbevDph1eyaaRNJHEO6NM")
    output = genai.GenerativeModel("gemini-2.0-flash").start_chat().send_message(prompt).text
def pass_output():
    return output