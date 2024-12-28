import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from encryption import chacha20_poly1305, ENCRYPT, REVERSE
from qrcode_manager import QRCodeManager


class EncryptDecryptApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Encrypt/Decrypt App")
		self.qr_manager = QRCodeManager()  # Instantiate QRCodeManager
		self.save_button = None

		# Initialize GUI components
		self.create_widgets()

	def create_widgets(self):
		"""Create all widgets for the application."""
		self.create_text_input()
		self.create_key_input()
		self.create_mode_selection()
		self.create_result_display()
		self.create_qr_display()
		self.create_load_qr_button()

	def create_load_qr_button(self):
		"""Create a button to load and decode a QR code."""
		load_qr_button = tk.Button(self.root, text="Upload QR Code", command=self.load_qr_code)
		load_qr_button.grid(row=6, column=1, padx=5, pady=5)
	
	def load_qr_code(self):
		"""Load and decode a QR code from an image file."""
		try:
			file_path = filedialog.askopenfilename(
				filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")],
				title="Selecione um QR Code"
			)
			if file_path:
				decoded_text = self.qr_manager.decode_qr_code(file_path)
				self.text_entry.delete("1.0", tk.END)  # Clear existing text
				self.text_entry.insert(tk.END, decoded_text)  # Insert decoded text
				messagebox.showinfo("Sucesso", "QR Code lido e texto extraído.")
		except ValueError as e:
			messagebox.showerror("Error", str(e))

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
		process_button = tk.Button(mode_frame, text="Processar", command=self.process)
		process_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

	def create_result_display(self):
		"""Create the result display section."""
		tk.Label(self.root, text="Resultado:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
		self.result_text = tk.Text(self.root, width=50, height=5)
		self.result_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

	def create_qr_display(self):
		"""Create QR code display and save button."""
		self.qr_label = tk.Label(self.root)
		self.qr_label.grid(row=4, column=1, padx=5, pady=5)
	
	def create_qr_save_button(self):
		"""Create the 'Salvar QR Code' button."""
		self.save_button = tk.Button(self.root, text="Salvar QR Code", command=self.save_qr_code)
		self.save_button.grid(row=5, column=1, padx=5, pady=5)

	def process(self):
		"""Callback for the 'Process' button."""
		user_text = self.text_entry.get("1.0", tk.END).strip()
		user_key = self.key_entry.get().strip()
		selected_mode = self.mode_var.get()

		# Clear previous result and QR code
		self.result_text.delete("1.0", tk.END)
		self.qr_label.config(image="")

		try:
			result = chacha20_poly1305(user_key, user_text, selected_mode)
			self.result_text.insert(tk.END, result)

			if selected_mode == ENCRYPT:
				self.create_qr_save_button()
				self.qr_manager.generate_qr_code(result)
				qr_tk_image = self.qr_manager.get_qr_tk_image()
				self.qr_label.config(image=qr_tk_image)
				self.qr_label.image = qr_tk_image  # Keep a reference to avoid garbage collection
			else:
				self.qr_manager.qr_image = None
				self.root.geometry("") # Reset window size
				if self.save_button:
					self.save_button.destroy()
					self.save_button = None

		except Exception as e:
			self.result_text.insert(tk.END, f"Error: {str(e)}")

	def save_qr_code(self):
		"""Save the generated QR code to a selected file."""
		try:
			file_path = filedialog.asksaveasfilename(
				defaultextension=".png",
				filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
				title="Salvar QR Code"
			)
			if file_path:
				self.qr_manager.save_qr_code(file_path)
		except ValueError as e:
			messagebox.showerror("Erro", "Nenhum QR Code foi gerado!")

	def select_all_text(self, widget):
		"""Select all text in a given widget."""
		widget.tag_add("sel", "1.0", "end")  # Select all text
		widget.mark_set("insert", "1.0")    # Set cursor position to start
		widget.see("insert")                # Scroll to cursor position


def main():
	root = tk.Tk()
	app = EncryptDecryptApp(root)
	root.mainloop()
