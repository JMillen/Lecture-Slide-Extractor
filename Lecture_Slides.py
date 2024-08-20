import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from pdf2image import convert_from_path

ctk.set_appearance_mode("dark") # Sets dark mode to all elements

def extract_slides(pdf_path, width, height):
    # Convert PDF to a list of images, resize during conversion for efficiency
    slides = convert_from_path(pdf_path, size=(width, height))
    return slides

def create_template(slides, box_width, box_height, margin=60, notes_height=200):
    cols = int(entry3.get())  # Number of columns
    rows = (len(slides) + cols - 1) // cols
    template_width = cols * (box_width + margin) + margin
    template_height = rows * (box_height + notes_height + 2 * margin) + margin
    template = Image.new('RGB', (template_width, template_height), color=(0, 0, 0))

    for i, slide in enumerate(slides):
        top_left_x = margin + (i % cols) * (box_width + margin)
        top_left_y = margin + (i // cols) * (box_height + notes_height + margin)
        resized_slide = slide.resize((box_width, box_height))
        template.paste(resized_slide, (top_left_x, top_left_y))
        draw = ImageDraw.Draw(template)
        draw.rectangle([top_left_x, top_left_y + box_height, top_left_x + box_width, top_left_y + box_height + notes_height], fill=(255, 255, 255), outline=(220, 220, 220))

    return template

def select_pdf():
    width = int(entry1.get())
    height = int(entry2.get())
    file_path = filedialog.askopenfilename(initialdir=os.path.expanduser('~/Downloads'), filetypes=[("PDF files", "*.pdf")])   
    if file_path:
        slides = extract_slides(file_path, width, height)
        template = create_template(slides, width, height)
        output_path = filedialog.asksaveasfilename(initialdir=r'C:\Users\jakob\Desktop\Uni', defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            template.save(output_path)
            messagebox.showinfo("Success", f"Template saved as {output_path}")

root = ctk.CTk()  # Use CTk instead of Tk
root.geometry("500x350") # Size of the window
root.title("Lecture Slide Extractor") # Title of the window

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Select a PDF file", font=("Arial", 20))
label.pack(pady=12, padx=10)

entry1 = ctk.CTkEntry(master=frame, placeholder_text="Enter Width")
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame, placeholder_text="Enter Height")
entry2.pack(pady=12, padx=10)

entry3 = ctk.CTkEntry(master=frame, placeholder_text="Enter Rows")
entry3.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Select PDF", command=select_pdf)
button.pack(pady=12, padx=10)

root.mainloop()