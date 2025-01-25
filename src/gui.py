import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from encryption import chacha20_poly1305, ENCRYPT, REVERSE
from qrcode_manager import QRCodeManager
import platform

MAX_CHARACTERS = 2174

class EncryptDecryptApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Encrypt/Decrypt App")
		self.qr_manager = QRCodeManager()
		self.save_button = None

		# Set window dimensions
		self.window_width = 1200
		self.window_height = 700
		self.center_window()

		# Initialize GUI components
		self.create_widgets()

	def center_window(self):
		"""Center the window on the screen."""
		# make window maximized, not resizable, set title and dont hide taskbar
		# get max height
		screen_height = self.root.winfo_screenheight()
		# get max width
		screen_width = self.root.winfo_screenwidth()
		# set window size
		self.root.geometry(f"{screen_width}x{screen_height}+0+0")

		self.root.resizable(True, True)

	def create_widgets(self):
		"""Create all widgets for the application."""
		# Configure root grid without dynamic resizing
		self.root.grid_columnconfigure(0, weight=0)
		self.root.grid_columnconfigure(1, weight=1)
		self.root.grid_rowconfigure(0, weight=1)

		# Create left frame
		left_frame = tk.Frame(self.root, width=900)
		left_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.N + tk.W + tk.S + tk.E)
		left_frame.grid_propagate(False)  # Prevent resizing based on content

		# Create right frame
		right_frame = tk.Frame(self.root)
		right_frame.grid(row=0, column=1, padx=1, pady=1, sticky=tk.N + tk.W + tk.S + tk.E)
		right_frame.grid_propagate(False)  # Prevent resizing based on content

		# Add widgets to the left and right frames
		self.create_left_frame_widgets(left_frame)
		self.create_right_frame_widgets(right_frame)


	def create_left_frame_widgets(self, frame):
		"""Create all widgets for the left frame."""
		# Center all widgets in this frame
		# Text Label
		tk.Label(frame, text="Text", font=("Arial", 14)).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

		# Text Entry (Fixed Width)
		self.text_entry = tk.Text(frame, height=15, width=50, font=("Arial", 12), wrap="word")
		self.text_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W + tk.E)

		# Scrollbar (Fixed Width)
		text_entry_scrollbar = tk.Scrollbar(frame, command=self.text_entry.yview, width=15)  # Ensure width remains fixed
		text_entry_scrollbar.grid(row=0, column=2, sticky="ns")  # No stretching
		self.text_entry.config(yscrollcommand=text_entry_scrollbar.set)

		# Character Counter Label (Fixed Width)
		self.char_count_label = tk.Label(frame, text=f"0/{MAX_CHARACTERS}", font=("Arial", 12), width=10, anchor="e")
		self.char_count_label.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)

		# Bind Text Modification
		self.text_entry.bind("<<Modified>>", self.update_char_count)

		# Prevent column resizing
		frame.grid_columnconfigure(0, weight=0)  # Label
		frame.grid_columnconfigure(1, weight=1)  # Text Box (Expandable)
		frame.grid_columnconfigure(2, weight=0)  # Scrollbar (Fixed)

		# Add scrollbar to the text entry
		text_entry_scrollbar = tk.Scrollbar(frame, command=self.text_entry.yview)
		text_entry_scrollbar.grid(row=0, column=2, sticky="nsew")
		self.text_entry.config(yscrollcommand=text_entry_scrollbar.set)

		# Add Key widget
		tk.Label(frame, text="Key", font=("Arial", 14)).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
		self.key_entry = tk.Entry(frame, font=("Arial", 12))
		self.key_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W + tk.E)

		# Add Mode widget
		tk.Label(frame, text="Mode", font=("Arial", 14)).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
		self.mode_var = tk.StringVar(value=ENCRYPT)
		mode_frame = ttk.Frame(frame)
		mode_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)

		# Add radio buttons to the mode frame
		mode_frame = tk.Frame(frame)
		mode_frame.grid(row=2, column=1, sticky=tk.W + tk.E, padx=10, pady=10)
		mode_frame.grid_columnconfigure(0, weight=0)
		mode_frame.grid_columnconfigure(1, weight=0)
		mode_frame.grid_columnconfigure(2, weight=1)
		mode_frame.grid_columnconfigure(3, weight=0)

		# Configure radio buttons
		style = ttk.Style(self.root)
		style.configure("Custom.TRadiobutton", font=("Arial", 14), padding=10)

		ttk.Radiobutton(mode_frame, text=ENCRYPT, variable=self.mode_var, value=ENCRYPT, style="Custom.TRadiobutton").grid(row=0, column=0, padx=10, sticky=tk.W)
		ttk.Radiobutton(mode_frame, text=REVERSE, variable=self.mode_var, value=REVERSE, style="Custom.TRadiobutton").grid(row=0, column=1, padx=10, sticky=tk.W)

		# Add Process button
		process_button = tk.Button(mode_frame, text="Processar", command=self.process, font=("Arial", 14))
		process_button.grid(row=0, column=3, padx=10, pady=10, sticky=tk.E)
		process_button.config(bg="lightgreen")

		# Add Result widget
		tk.Label(frame, text="Result", font=("Arial", 14)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
		self.result_text = tk.Text(frame, height=15, font=("Arial", 12))
		self.result_text.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W + tk.E)

		# Add scrollbar to the result text
		result_text_scrollbar = tk.Scrollbar(frame, command=self.result_text.yview)
		result_text_scrollbar.grid(row=3, column=2, sticky="nsew")
		self.result_text.config(yscrollcommand=result_text_scrollbar.set)

	def update_char_count(self, event):
		"""Update the character count label, enforce limit, and disable QR save if exceeded."""

		# Prevent redundant execution
		if not self.text_entry.edit_modified():
			return  # Skip if nothing actually changed

		text = self.text_entry.get("1.0", tk.END).strip()
		char_count = len(text)
		
		if char_count > MAX_CHARACTERS:
			self.text_entry.tag_remove("warning", "1.0", tk.END)
			self.text_entry.tag_add("warning", "1.0", "end")

			# Create tooltip only if it doesn't already exist
			if not hasattr(self, "tooltip") or not self.tooltip.winfo_exists():
				self.tooltip = tk.Label(self.text_entry, 
										text=f"No QRCode if {MAX_CHARACTERS} characters limit exceeded!", 
										bg="yellow", relief="solid")
				self.tooltip.place(relx=1.0, rely=0, anchor="ne")

			self.save_button.config(state=tk.DISABLED)
		else:
			self.text_entry.tag_remove("warning", "1.0", tk.END)
			# Destroy tooltip if it exists
			if hasattr(self, "tooltip") and self.tooltip.winfo_exists():
				self.tooltip.destroy()
				del self.tooltip  # Remove attribute to avoid stale references
		
		self.char_count_label.config(text=f"{char_count}/{MAX_CHARACTERS}")
		self.text_entry.edit_modified(False)
			
	def create_right_frame_widgets(self, frame):
		"""Create all widgets for the right frame."""
		# Center all widgets in this frame
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_rowconfigure(0, weight=0)
		frame.grid_rowconfigure(1, weight=0)
		frame.grid_rowconfigure(2, weight=0) 

		load_qr_button = tk.Button(frame, text="Upload QR Code", command=self.load_qr_code, font=("Arial", 14))
		load_qr_button.grid(row=0, column=0, padx=10, pady=10)
		load_qr_button.config(bg="lightblue")
		load_qr_button.config(width=20)

		self.save_button = tk.Button(frame, text="Save QR Code", command=self.save_qr_code, font=("Arial", 14))
		self.save_button.grid(row=1, column=0, padx=10, pady=10)
		self.save_button.config(bg="lightblue")
		self.save_button.config(state=tk.DISABLED)
		self.save_button.config(width=20)
		
		self.qr_image_label = tk.Label(frame) # label for the QR code image to be displayed
		self.qr_image_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.N)
 		

	def process(self):
		"""Callback for the 'Process' button."""
		user_text = self.text_entry.get("1.0", tk.END).strip()
		user_key = self.key_entry.get().strip()
		selected_mode = self.mode_var.get()

		# Clear previous result and QR code
		self.result_text.delete("1.0", tk.END)
		self.qr_image_label.config(image="")
		self.save_button.config(state=tk.DISABLED)

		try:
			result = chacha20_poly1305(user_key, user_text, selected_mode)
			self.result_text.insert(tk.END, result)

			if selected_mode == ENCRYPT and len(user_text) <= MAX_CHARACTERS:
				self.save_button.config(state=tk.NORMAL)
				self.qr_manager.generate_qr_code(result)
				qr_tk_image = self.qr_manager.get_qr_tk_image()
				self.qr_image_label.config(image=qr_tk_image)
				self.qr_image_label.image = qr_tk_image  # Keep a reference to avoid garbage collection

		except Exception as e:
			self.result_text.insert(tk.END, f"Error: {str(e)}")

	def save_qr_code(self):
		"""Save the generated QR code to a selected file."""
		try:
			file_path = filedialog.asksaveasfilename(
				defaultextension=".png",
				filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
				title="Save QR Code"
			)
			if file_path:
				self.qr_manager.save_qr_code(file_path)
		except ValueError as e:
			messagebox.showerror("Error", "No QR Code generated!")

	def load_qr_code(self):
		"""Load and decode a QR code from an image file."""
		try:
			file_path = filedialog.askopenfilename(
				filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")],
				title="Select a QR Code"
			)
			if file_path:
				decoded_text = self.qr_manager.decode_qr_code(file_path)
				self.text_entry.delete("1.0", tk.END)  # Clear existing text
				self.text_entry.insert(tk.END, decoded_text)  # Insert decoded text
				self.mode_var.set(REVERSE)
				messagebox.showinfo("Success", "QR Code text was successfully extracted!")
		except ValueError as e:
			messagebox.showerror("Error", str(e))


def main():
	root = tk.Tk()
	app = EncryptDecryptApp(root)
	root.mainloop()
