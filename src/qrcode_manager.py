import qrcode
from PIL import Image, ImageTk
import cv2


class QRCodeManager:
    def __init__(self):
        self.qr_image = None

    def generate_qr_code(self, data, size=(600, 600)):
        """
        Generate a QR code from the provided data and store it as an Image.
        """
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        self.qr_image = qr.make_image(fill_color="black", back_color="white")
        self.qr_image = self.qr_image.resize(size, Image.Resampling.NEAREST)
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
            Decode the content of a QR code from an image file using OpenCV.
            """
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Invalid image file or path.")

            detector = cv2.QRCodeDetector()
            data, points, _ = detector.detectAndDecode(image)

            if not data:
                raise ValueError("No QR code found in the image.")
            return data