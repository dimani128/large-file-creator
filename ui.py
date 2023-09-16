
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import humanfriendly
import util

MAX_FILE_SIZE = 1000000 * 1000 # 1000 MB
WARNING_FILE_SIZE = 1000000 * 100 # 1000 MB

class FileGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Generator")
        
        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(padx=10, pady=10)

        ttk.Label(self.input_frame, text="Enter file text:").pack(anchor="w")
        self.text_entry = ttk.Entry(self.input_frame)
        self.text_entry.pack(fill="x", padx=5, pady=5)

        # ttk.Label(self.input_frame, text="Enter save file name:").pack(anchor="w")
        # self.filename_entry = ttk.Entry(self.input_frame)
        # self.filename_entry.pack(fill="x", padx=5, pady=5)

        self.new_line_var = tk.BooleanVar()
        ttk.Checkbutton(self.input_frame, text="Use new lines", variable=self.new_line_var).pack(anchor="w")

        ttk.Label(self.input_frame, text="Enter File Size:").pack(anchor="w")
        self.size_entry = ttk.Entry(self.input_frame)
        self.size_entry.pack(fill="x", padx=5, pady=5)

        ttk.Button(self.input_frame, text="Generate File", command=self.generate_file).pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress_bar.pack(pady=10, padx=10)

        self.output_frame = ttk.Frame(root)
        self.output_frame.pack(padx=10, pady=10)

        # self.output_text = tk.Text(self.output_frame, wrap="word", height=10, width=50)
        # self.output_text.pack(fill="both", expand=True)

    def generate_file(self):
        _text = self.text_entry.get()
        # filename = self.filename_entry.get()
        _text += '\n' if self.new_line_var.get() else ''

        try:
            b = util.strToBytes(self.size_entry.get())

            if b <= 0:
                raise ValueError('Size must be bigger than 0.')
            elif b > MAX_FILE_SIZE:
                raise ValueError(f'Size must be less than {humanfriendly.format_size(MAX_FILE_SIZE)}.')
            elif b > WARNING_FILE_SIZE:
                cont = messagebox.askokcancel("Warning:", f'The file size, {humanfriendly.format_size(b)}, is greater than the recommended max size, {humanfriendly.format_size(WARNING_FILE_SIZE)}.\nThis may take a while. Are you sure you want to continue?')
                if not cont:
                    return

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        correct = messagebox.askyesno(
            "Confirmation",
            f'{humanfriendly.format_size(b)} of\n{_text}\nIs this right?'
        )

        if not correct:
            return
        
        filename = filedialog.asksaveasfilename(defaultextension='txt', filetypes=[("Text files", ".txt"), ("All Files", '.*')])

        # self.output_text.insert("end", "Compiling...\n")
        self.root.update_idletasks()

        size_of_text = util.utf8len(_text)
        # final = ''.join([_text for _ in range(b // size_of_text)])
        chunks = 20
        final = ''.join([_text for _ in range(b // size_of_text // chunks)])
        final = [final for i in range(chunks)]

        # self.output_text.insert("end", "Saving...\n")
        self.root.update_idletasks()

        try:
            with open(filename, 'w') as f:
                for i, chunk in enumerate(final):
                    f.write(chunk)
                    progress = (i + 1) / len(final) * 100
                    self.progress_bar["value"] = progress
                    self.root.update_idletasks()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")
        else:
            self.progress_bar["value"] = 100
            messagebox.showinfo("Success", "File saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileGeneratorApp(root)
    root.mainloop()
