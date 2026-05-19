from PIL import Image
import pytesseract


class Vision:

    def read_screen(self, image_path):

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text


    def get_text_data(self, image_path):

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        image = Image.open(image_path)

        data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT
        )

        return data