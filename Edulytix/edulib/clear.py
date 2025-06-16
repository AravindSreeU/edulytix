import os, shutil

def remove(path):
    if os.path.isdir(path): shutil.rmtree(path)
    elif os.path.isfile(path): os.remove(path)

def run():
    d = os.path.dirname(__file__)
    for f in ["__pycache__", "report_data.dat", "performance_plot.png", "rotated_image.png"]:
        remove(os.path.join(d, f))