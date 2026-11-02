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
            if os.path.exists("icon.ico"):
                self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Prettifier variables
        self.input_files = []  # List of selected files
        self.output_folder = ctk.StringVar()
        self.processing = False
        self.delete_original = ctk.BooleanVar(value=False)
        
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
            text="Input JSON Files",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        input_label.pack(anchor="w", pady=(0, 8))
        
        input_container = ctk.CTkFrame(input_section, fg_color="transparent")
        input_container.pack(fill="x")
        
        self.input_entry = ctk.CTkEntry(
            input_container,
            placeholder_text="Select JSON files to prettify...",
            height=40,
            font=ctk.CTkFont(size=13),
            state="readonly"
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        input_btn = ctk.CTkButton(
            input_container,
            text="📁 Browse Files",
            command=self.select_input_files,
            width=140,
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
        
        # Delete original file option
        delete_section = ctk.CTkFrame(content_card, fg_color="transparent")
        delete_section.pack(fill="x", padx=30, pady=(0, 15))
        
        self.delete_checkbox = ctk.CTkCheckBox(
            delete_section,
            text="⚠️ Delete original files after prettifying (Use with caution!)",
            variable=self.delete_original,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#ff6b6b", "#ff5252"),
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            border_color="#d32f2f"
        )
        self.delete_checkbox.pack(anchor="w")
        
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
        
    def select_input_files(self):
        filenames = filedialog.askopenfilenames(
            title="Select JSON files (multiple selection enabled)",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filenames:
            self.input_files = list(filenames)
            # Update display
            if len(self.input_files) == 1:
                self.input_entry.configure(state="normal")
                self.input_entry.delete(0, 'end')
                self.input_entry.insert(0, os.path.basename(self.input_files[0]))
                self.input_entry.configure(state="readonly")
            else:
                self.input_entry.configure(state="normal")
                self.input_entry.delete(0, 'end')
                self.input_entry.insert(0, f"{len(self.input_files)} files selected")
                self.input_entry.configure(state="readonly")
            
            # Set output folder to first file's directory
            input_folder = os.path.dirname(self.input_files[0])
            self.output_folder.set(input_folder)
            
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)
            
    def process_file(self):
        if not self.input_files:
            messagebox.showerror("Error", "Please select input files!")
            return
            
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder!")
            return
            
        if self.processing:
            messagebox.showwarning("Warning", "Processing already in progress!")
            return
            
        self.processing = True
        self.process_btn.configure(state="disabled", text="⏳ Processing...")
        thread = threading.Thread(target=self.prettify_multiple_files, daemon=True)
        thread.start()
        
    def prettify_multiple_files(self):
        total_files = len(self.input_files)
        delete_orig = self.delete_original.get()
        processed_files = []
        failed_files = []
        files_to_delete = []
        
        overall_start = time.time()
        
        try:
            for idx, input_path in enumerate(self.input_files, 1):
                try:
                    input_filename = os.path.basename(input_path)
                    name, ext = os.path.splitext(input_filename)
                    output_filename = name + "_pretty" + ext
                    output_path = os.path.join(self.output_folder.get(), output_filename)
                    
                    file_size = os.path.getsize(input_path)
                    file_start = time.time()
                    
                    # Phase 1: Reading (0-40% of file progress)
                    base_progress = (idx - 1) / total_files
                    file_progress_weight = 1.0 / total_files
                    
                    self.root.after(0, self.update_progress,
                                  base_progress,
                                  f"[{idx}/{total_files}] Reading: {input_filename}")
                    self.root.after(0, self.update_status,
                                  f"⚙️ Reading file {idx} of {total_files}...", "normal")
                    
                    # Read file with progress tracking
                    with open(input_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update: Reading complete (40%)
                    self.root.after(0, self.update_progress,
                                  base_progress + (file_progress_weight * 0.4),
                                  f"[{idx}/{total_files}] Parsing: {input_filename}")
                    
                    # Phase 2: Parsing JSON (40-60%)
                    data = json.loads(content)
                    
                    # Update: Parsing complete (60%)
                    self.root.after(0, self.update_progress,
                                  base_progress + (file_progress_weight * 0.6),
                                  f"[{idx}/{total_files}] Formatting: {input_filename}")
                    
                    # Phase 3: Formatting (60-80%)
                    formatted = json.dumps(data, indent=2, ensure_ascii=False, separators=(',', ': '))
                    
                    # Update: Formatting complete (80%)
                    self.root.after(0, self.update_progress,
                                  base_progress + (file_progress_weight * 0.8),
                                  f"[{idx}/{total_files}] Writing: {input_filename}")
                    
                    # Phase 4: Writing (80-100%)
                    with open(output_path, 'w', encoding='utf-8') as w:
                        w.write(formatted)
                        w.write('\n')
                    
                    file_elapsed = time.time() - file_start
                    
                    # Update: File complete (100%)
                    self.root.after(0, self.update_progress,
                                  base_progress + file_progress_weight,
                                  f"[{idx}/{total_files}] ✓ Complete: {input_filename} ({file_elapsed:.2f}s)")
                    
                    processed_files.append((input_filename, file_elapsed))
                    
                    # Track for deletion if requested
                    if delete_orig:
                        files_to_delete.append(input_path)
                    
                except Exception as e:
                    failed_files.append((os.path.basename(input_path), str(e)))
                    # Show error for this file
                    self.root.after(0, self.update_progress,
                                  (idx) / total_files,
                                  f"[{idx}/{total_files}] ✗ Failed: {os.path.basename(input_path)}")
            
            # Final progress update
            overall_elapsed = time.time() - overall_start
            self.root.after(0, self.update_progress, 1.0, f"100% • ✓ Complete in {overall_elapsed:.2f}s!")
            self.root.after(0, self.update_status, "✓ All files processed!", "success")
            
            # Show completion dialog
            def show_completion():
                success_count = len(processed_files)
                fail_count = len(failed_files)
                
                result_msg = f"Processing Complete!\n\n"
                result_msg += f"✓ Successful: {success_count} file(s)\n"
                if fail_count > 0:
                    result_msg += f"✗ Failed: {fail_count} file(s)\n"
                result_msg += f"\nTotal time: {overall_elapsed:.2f} seconds\n"
                result_msg += f"Output folder: {self.output_folder.get()}"
                
                if failed_files:
                    result_msg += "\n\nFailed files:\n"
                    for fname, err in failed_files[:5]:  # Show first 5 failures
                        result_msg += f"• {fname}: {err[:50]}\n"
                
                messagebox.showinfo("Batch Processing Complete", result_msg)
                
                # Handle deletion if requested
                if delete_orig and files_to_delete:
                    delete_result = messagebox.askyesno(
                        "Delete Original Files?",
                        f"⚠️ WARNING: Delete {len(files_to_delete)} original file(s)?\n\nThis action CANNOT be undone!",
                        icon='warning'
                    )
                    if delete_result:
                        deleted = 0
                        delete_errors = []
                        for fpath in files_to_delete:
                            try:
                                os.remove(fpath)
                                deleted += 1
                            except Exception as del_err:
                                delete_errors.append((os.path.basename(fpath), str(del_err)))
                        
                        del_msg = f"Deleted {deleted} file(s)"
                        if delete_errors:
                            del_msg += f"\n\nFailed to delete {len(delete_errors)} file(s)"
                        messagebox.showinfo("Deletion Complete", del_msg)
                
                self.reset_ui()
            
            self.root.after(0, show_completion)
            
        except Exception as e:
            self.root.after(0, self.update_status, f"✗ Error: {str(e)}", "error")
            def show_error():
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
                self.reset_ui()
            self.root.after(0, show_error)
            
        finally:
            self.processing = False
            self.root.after(0, lambda: self.process_btn.configure(state="normal", text="✨ Prettify JSON"))
    
    def reset_ui(self):
        """Reset UI to ready state after dialog closes"""
        self.progress_bar.set(0)
        self.detail_label.configure(text="")
        self.status_label.configure(text="✓ Ready to process")
            
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