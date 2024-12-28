import qrcode
from PIL import Image, ImageTk
import pyzbar.pyzbar as pyzbar


class QRCodeManager:
    def __init__(self):
        self.qr_image = None  # To hold the generated QR code image

    def generate_qr_code(self, data, size=(300, 300)):
        """
        Generate a QR code from the provided data and store it as an Image.
        """
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        self.qr_image = qr.make_image(fill_color="black", back_color="white")
        self.qr_image = self.qr_image.resize(size, Image.Resampling.LANCZOS)
        return self.qr_image

    def get_qr_tk_image(self):
        """
        Convert the QR code to an ImageTk.PhotoImage for use in a Tkinter widget.
        """
        if not self.qr_image:
            raise ValueError("No QR code image available. Please generate one first.")
        return ImageTk.PhotoImage(self.qr_image)

    def save_qr_code(self, file_path):
        """
        Save the QR code to the specified file path.
        """
        if not self.qr_image:
            raise ValueError("No QR code image available. Please generate one first.")
        self.qr_image.save(file_path)

    def decode_qr_code(self, image_path):
        """
        Decode the content of a QR code from an image file.
        """
        image = Image.open(image_path)
        decoded_objects = pyzbar.decode(image)
        if not decoded_objects:
            raise ValueError("No QR code found in the image.")
        return decoded_objects[0].data.decode("utf-8")