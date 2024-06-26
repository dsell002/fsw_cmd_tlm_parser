import tkinter as tk
from tkinter import filedialog, messagebox
from clang_parser import parse_code, save_to_json

class ParserWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Software Parser Wizard")
        self.command_file = None
        self.telemetry_file = None
        self.command_keyword = ""
        self.telemetry_keyword = ""
        
        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root)
        
        self.create_page1()
        self.create_page2()
        
        self.frame1.pack()

    def create_page1(self):
        tk.Label(self.frame1, text="Command File:").grid(row=0, column=0, padx=10, pady=10)
        self.command_file_entry = tk.Entry(self.frame1, width=50)
        self.command_file_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.frame1, text="Browse", command=self.select_command_file).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.frame1, text="Telemetry File:").grid(row=1, column=0, padx=10, pady=10)
        self.telemetry_file_entry = tk.Entry(self.frame1, width=50)
        self.telemetry_file_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.frame1, text="Browse", command=self.select_telemetry_file).grid(row=1, column=2, padx=10, pady=10)

        tk.Button(self.frame1, text="Next", command=self.show_page2).grid(row=2, column=1, pady=20)

    def create_page2(self):
        tk.Label(self.frame2, text="Command File Keyword:").grid(row=0, column=0, padx=10, pady=10)
        self.command_keyword_entry = tk.Entry(self.frame2, width=50)
        self.command_keyword_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame2, text="Telemetry File Keyword:").grid(row=1, column=0, padx=10, pady=10)
        self.telemetry_keyword_entry = tk.Entry(self.frame2, width=50)
        self.telemetry_keyword_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.frame2, text="Back", command=self.show_page1).grid(row=2, column=0, pady=20)
        tk.Button(self.frame2, text="Parse and Save", command=self.parse_and_save).grid(row=2, column=2, pady=20)

    def select_command_file(self):
        self.command_file = filedialog.askopenfilename()
        self.command_file_entry.delete(0, tk.END)
        self.command_file_entry.insert(0, self.command_file)

    def select_telemetry_file(self):
        self.telemetry_file = filedialog.askopenfilename()
        self.telemetry_file_entry.delete(0, tk.END)
        self.telemetry_file_entry.insert(0, self.telemetry_file)

    def show_page1(self):
        self.frame2.pack_forget()
        self.frame1.pack()

    def show_page2(self):
        self.frame1.pack_forget()
        self.frame2.pack()

    def parse_and_save(self):
        self.command_keyword = self.command_keyword_entry.get()
        self.telemetry_keyword = self.telemetry_keyword_entry.get()
        
        parsed_data = parse_code(self.command_file, self.telemetry_file, self.command_keyword, self.telemetry_keyword)
        
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_path:
            save_to_json(parsed_data, save_path)
            messagebox.showinfo("Success", f"Data saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParserWizard(root)
    root.mainloop()
