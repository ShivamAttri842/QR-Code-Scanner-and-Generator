import cv2
from pyzbar.pyzbar import decode
import pyttsx3
import numpy as np
import qrcode 

def scan_qr_code_from_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image. Check the path.")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded_objects = decode(gray_image)

    if not decoded_objects:
        return None

    qr_data_list = []
    for obj in decoded_objects:
        qr_data = obj.data.decode("utf-8")
        qr_type = obj.type
        qr_data_list.append(f"Data: {qr_data}, Type: {qr_type}")

    return qr_data_list

def generate_qr_code(text, output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(output_path)
    return output_path

def speak_text(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    engine.say(text)
    engine.runAndWait()

def main():
    action = input("Do you want to (1) Generate a QR code or (2) Scan a QR code? Enter 1 or 2: ")

    if action == '1':
        text = input("Enter the text for the QR code: ")
        output_path = 'generated_qrcode.png'
        generate_qr_code(text, output_path)
        print(f"QR code generated and saved to {output_path}.")
        speak_text("QR code generated successfully.")
    elif action == '2':
        image_path = input("Enter the path of the image file to scan: ")
        qr_data_list = scan_qr_code_from_image(image_path)

        if qr_data_list:
            for qr_data in qr_data_list:
                print(qr_data)
                speak_text(qr_data)
            speak_text("QR code scanned successfully.")
        else:
            print("No QR code detected.")
            speak_text("No QR code detected.")
    else:
        print("Invalid option. Please enter 1 or 2.")
        speak_text("Invalid option.")

if __name__ == "__main__":
    main()
