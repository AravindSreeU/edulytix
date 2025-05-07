import google.generativeai as genai
import pickle
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "report_data.dat")
with open(file_path, 'rb') as fo:
    data = pickle.load(fo)

exam_percentage = ""
for subject, percentages in data[6].items():
    exam_percentage += f"{subject}: {percentages}%, "

assignment_data = ""
for subject, percentage in data[4].items():
    assignment_data += f"{subject}: {percentage}%, "

#Prompt for Gemini
prompt = f'''A student named {data[0]} of class {data[1]} has an attendence percentage of {data[1]} and completed assignments of {assignment_data} and scored {exam_percentage}. This data is collected for the entire year and recorded. The student have written three monthly tests and 1 yearly and 1 annual test. Based on that data the overall percentage in each subject is given to you.
            With this information write 4 points under Insights, 3 points under Stregth, 3 points under Weaknesses and 4 points under suggestion for Improvemrnt. 
            There shall be no bold words. Just provide me the text with spaces and reqquired lines to separate each topic.'''

genai.configure(api_key="AIzaSyDA91w7mb834mjbevDph1eyaaRNJHEO6NM")
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()
response = chat.send_message(prompt)
output = response.text

def pass_output():
    return output 