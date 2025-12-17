import json
import os
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading


class JSONPrettifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Prettifier")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        try:
            if os.path.exists("json_logo_icon_168490.ico"):
                self.root.iconbitmap("json_logo_icon_168490.ico")
        except:
            pass
        
        # Prettifier variables
        self.input_file = ctk.StringVar()
        self.output_folder = ctk.StringVar()
        self.output_file_path = ctk.StringVar()
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎨 JSON Prettifier",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Transform your JSON files into beautifully formatted documents",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
        )
        subtitle_label.pack(pady=(5, 0))
        
        content_card = ctk.CTkFrame(main_frame, corner_radius=15)
        content_card.pack(fill="both", expand=True)
        
        # Input file section
        input_section = ctk.CTkFrame(content_card, fg_color="transparent")
        input_section.pack(fill="x", padx=30, pady=(30, 15))
        
        input_label = ctk.CTkLabel(
            input_section,
            text="Input JSON File",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        input_label.pack(anchor="w", pady=(0, 8))
        
        input_container = ctk.CTkFrame(input_section, fg_color="transparent")
        input_container.pack(fill="x")
        
        self.input_entry = ctk.CTkEntry(
            input_container,
            textvariable=self.input_file,
            placeholder_text="Select a JSON file to prettify...",
            height=40,
            font=ctk.CTkFont(size=13),
            state="readonly"
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        input_btn = ctk.CTkButton(
            input_container,
            text="📁 Browse",
            command=self.select_input_file,
            width=120,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        input_btn.pack(side="right")
        
        # Output folder section
        output_section = ctk.CTkFrame(content_card, fg_color="transparent")
        output_section.pack(fill="x", padx=30, pady=15)
        
        output_label = ctk.CTkLabel(
            output_section,
            text="Output Folder",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        output_label.pack(anchor="w", pady=(0, 8))
        
        output_container = ctk.CTkFrame(output_section, fg_color="transparent")
        output_container.pack(fill="x")
        
        self.output_entry = ctk.CTkEntry(
            output_container,
            textvariable=self.output_folder,
            placeholder_text="Select output folder (auto-set to input file folder)...",
            height=40,
            font=ctk.CTkFont(size=13),
            state="readonly"
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        output_btn = ctk.CTkButton(
            output_container,
            text="📂 Choose Folder",
            command=self.select_output_folder,
            width=140,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        output_btn.pack(side="right")
        
        # Progress section
        progress_section = ctk.CTkFrame(content_card, fg_color="transparent")
        progress_section.pack(fill="x", padx=30, pady=15)
        
        progress_label = ctk.CTkLabel(
            progress_section,
            text="Progress",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        progress_label.pack(anchor="w", pady=(0, 8))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_section,
            height=12,
            corner_radius=6
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            progress_section,
            text="✓ Ready to process",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.status_label.pack(anchor="w", pady=(0, 5))
        
        self.detail_label = ctk.CTkLabel(
            progress_section,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40"),
            anchor="w"
        )
        self.detail_label.pack(anchor="w")
        
        # Process button
        button_container = ctk.CTkFrame(content_card, fg_color="transparent")
        button_container.pack(fill="x", padx=30, pady=(15, 30))
        
        self.process_btn = ctk.CTkButton(
            button_container,
            text="✨ Prettify JSON",
            command=self.process_file,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10
        )
        self.process_btn.pack(fill="x", pady=0)
        
        footer_label = ctk.CTkLabel(
            main_frame,
            text="Created By Harshmeet Singh • Ultra-Fast Performance",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50")
        )
        footer_label.pack(pady=(15, 0))
        
    def select_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            input_folder = os.path.dirname(filename)
            self.output_folder.set(input_folder)
            self.update_output_path()
            
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)
            self.update_output_path()
    
    def update_output_path(self):
        if self.input_file.get() and self.output_folder.get():
            input_filename = os.path.basename(self.input_file.get())
            name, ext = os.path.splitext(input_filename)
            output_filename = name + "_pretty" + ext
            self.output_file_path.set(os.path.join(self.output_folder.get(), output_filename))
            
    def process_file(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file!")
            return
            
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder!")
            return
            
        if self.processing:
            messagebox.showwarning("Warning", "Processing already in progress!")
            return
            
        self.processing = True
        self.process_btn.configure(state="disabled", text="⏳ Processing...")
        thread = threading.Thread(target=self.prettify_json, daemon=True)
        thread.start()
        
    def prettify_json(self):
        try:
            p = self.input_file.get()
            out = self.output_file_path.get()
            
            start_time = time.time()
            
            self.root.after(0, self.update_status, "⚙️ Processing...", "normal")
            
            # Original fast implementation
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with open(out, 'w', encoding='utf-8') as w:
                json.dump(data, w, indent=2, ensure_ascii=False, separators=(',', ': '))
                w.write('\n')
            
            elapsed = time.time() - start_time
            
            self.root.after(0, self.update_progress, 1.0, f"100% • ✓ Complete in {elapsed:.2f}s!")
            self.root.after(0, self.update_status, "✓ Complete!", "success")
            self.root.after(0, lambda: messagebox.showinfo("Success", f"JSON prettified successfully!\n\nSaved to:\n{out}\n\nTime: {elapsed:.2f} seconds"))
            
        except Exception as e:
            self.root.after(0, self.update_status, f"✗ Error: {str(e)}", "error")
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred:\n{str(e)}"))
            
        finally:
            self.processing = False
            self.root.after(0, lambda: self.process_btn.configure(state="normal", text="✨ Prettify JSON"))
            
    def update_progress(self, percent, detail):
        self.progress_bar.set(percent)
        self.detail_label.configure(text=detail)
        
    def update_status(self, message, status_type):
        self.status_label.configure(text=message)


def main():
    root = ctk.CTk()
    app = JSONPrettifierApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()