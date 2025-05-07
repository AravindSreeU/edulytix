import os
import shutil

def clear_edulib():
    # Get the current directory (edulib folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define paths to delete
    pycache_folder = os.path.join(script_dir, "__pycache__")
    report_data_file = os.path.join(script_dir, "report_data.dat")
    performance_plot = os.path.join(script_dir, "performance_plot.png")
    rotated_image = os.path.join(script_dir, "rotated_image.png")

    # Delete the folder "-pycache_" if it exists
    if os.path.isdir(pycache_folder):
        shutil.rmtree(pycache_folder)

    # Delete the file report_data.dat if it exists
    if os.path.isfile(report_data_file):
        os.remove(report_data_file)

    # Delete the file performance_plot.png if it exists
    if os.path.isfile(performance_plot):
        os.remove(performance_plot)

    # Delete the file rotated_image.png if it exists
    if os.path.isfile(rotated_image):
        os.remove(rotated_image)

if __name__ == "__main__":
    clear_edulib()