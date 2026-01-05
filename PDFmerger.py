import PyPDF2
import sys
import os

input_directory = r"C:\Users\yuvra\Downloads\testing"
merger = PyPDF2.PdfMerger()
files = os.listdir(input_directory)
print(files)
for file in files:
    if file.endswith(".pdf"):
        file_path = os.path.join(input_directory, file)
        merger.append(file_path)

merger.write(input_directory+r"\Combined.pdf")
merger.close()
print("Done!")