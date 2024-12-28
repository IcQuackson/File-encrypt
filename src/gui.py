import tkinter as tk
from tkinter import ttk
from encryption import chacha20_poly1305, ENCRYPT, REVERSE

class EncryptDecryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Encrypt/Decrypt GUI")

        # Initialize GUI components
        self.create_widgets()

    def create_widgets(self):
        """Create all widgets for the application."""
        self.create_text_input()
        self.create_key_input()
        self.create_mode_selection()
        self.create_result_display()

    def create_text_input(self):
        """Create the text input section."""
        tk.Label(self.root, text="Texto:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_entry = tk.Text(self.root, width=50, height=5)
        self.text_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

    def create_key_input(self):
        """Create the key input section."""
        tk.Label(self.root, text="Chave:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.key_entry = tk.Entry(self.root, width=50)
        self.key_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

    def create_mode_selection(self):
        """Create the mode selection (radio buttons) section."""
        tk.Label(self.root, text="Modo:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.mode_var = tk.StringVar(value=ENCRYPT)
        mode_frame = ttk.Frame(self.root)
        mode_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Radio buttons side-by-side, aligned to the left
        ttk.Radiobutton(mode_frame, text=ENCRYPT, variable=self.mode_var, value=ENCRYPT).grid(row=0, column=0, padx=5, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text=REVERSE, variable=self.mode_var, value=REVERSE).grid(row=0, column=1, padx=5, sticky=tk.W)

        # Process button to the right of radio buttons
        process_button = tk.Button(self.root, text="Processar", command=self.process)
        process_button.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    def create_result_display(self):
        """Create the result display section."""
        tk.Label(self.root, text="Resultado:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.result_text = tk.Text(self.root, width=50, height=5)
        self.result_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

    def process(self):
        """Callback for the 'Process' button."""
        user_text = self.text_entry.get("1.0", tk.END).strip()
        # delete all text
        self.select_all_text(self.text_entry)
        user_key = self.key_entry.get().strip()
        selected_mode = self.mode_var.get()

        # Clear previous result
        self.result_text.delete("1.0", tk.END)

        try:
            result = chacha20_poly1305(user_key, user_text, selected_mode)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {str(e)}")
    
    def select_all_text(self, widget):
        """Select all text in a given widget."""
        widget.tag_add("sel", "1.0", "end")  # Select all text
        widget.mark_set("insert", "1.0")    # Set cursor position to start
        widget.see("insert")                # Scroll to cursor position
    
def main():
    root = tk.Tk()
    app = EncryptDecryptApp(root)
    root.mainloop()
