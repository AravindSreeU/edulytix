from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import os
import pickle
import gemini_summary as gem

script_dir = os.path.dirname(os.path.abspath(__file__))

# Load data
file_path = os.path.join(script_dir, "report_data.dat")
with open(file_path, 'rb') as fo:
    data = pickle.load(fo)
    
doc_path = data[7]

# Set paths
original_image_path = os.path.join(script_dir, "performance_plot.png")
rotated_image_path = os.path.join(script_dir, "rotated_image.png")
output_doc_path = os.path.join(doc_path, f"{data[0]}_Report"+".docx")

img = Image.open(original_image_path)
rotated_img = img.rotate(270, expand=True)
rotated_img.save(rotated_image_path)

assignment_data = ""
for subject, percentage in data[4].items():
    assignment_data += f'''{subject.title()}: {percentage}%\n'''

raw_prompt_output = gem.pass_output().strip().split("\n\n")
output = "\n\n".join(raw_prompt_output)

doc = Document()
for section in doc.sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

# Title
title_para = doc.add_paragraph("EduLytix - Scholastic Report")
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_para.runs[0]
title_run.bold = True
title_run.font.size = Pt(14)

# Inline content section
def add_inline_section(heading, content):
    para = doc.add_paragraph()
    run1 = para.add_run(heading + " ")
    run1.bold = True
    run1.font.size = Pt(13)
    
    run2 = para.add_run(content)
    run2.font.size = Pt(12)

# Newline content section
def add_multiline_section(heading, content):
    para = doc.add_paragraph()
    run1 = para.add_run(heading)
    run1.bold = True
    run1.font.size = Pt(13)
    content_para = doc.add_paragraph(content)
    content_para.runs[0].font.size = Pt(12)

# Add sections
add_inline_section("Student Name:", data[0])
add_inline_section("Class:", data[1])
add_inline_section("Section:", data[2])
add_inline_section("Attendance:", data[3])
add_multiline_section("Assignment Completion:",assignment_data)
add_multiline_section("Teacher's Remarks:", data[5])

doc.add_paragraph("AI Summary:", style=None).runs[0].bold = True
doc.add_paragraph(output).runs[0].font.size = Pt(12)


# Page break for image
doc.add_page_break()

# Image section
title = doc.add_paragraph("Subject Wise Performance Graph")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title.runs[0]
title_run.bold = True
title_run.font.size = Pt(14)

img_para = doc.add_paragraph()
img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
img_para.add_run().add_picture(rotated_image_path, width=Inches(6))

# Save
doc.save(output_doc_path)
print(f"Document saved to: {output_doc_path}")
