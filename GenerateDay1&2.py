import csv
import os
import random
import string
import qrcode

# Function to generate a random serial number
def generate_serial_number(day):
    return f'D{day}PPP' + ''.join(random.choices(string.digits, k=6))

# Create a directory to save QR code images
os.makedirs('PPP-QR-Code', exist_ok=True)

# List to store serial numbers and their QR codes
serial_qr_pairs = []

# Generate QR codes with random serial numbers for both days
for day in range(1, 3):  # Loop through days 1 and 2
    for _ in range(10):  # Change the range to generate the desired number of QR codes
        serial_number = generate_serial_number(day)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(serial_number)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Save the QR code image
        img_filename = f'PPP-QR-Code/{serial_number}.png'
        img.save(img_filename)

        # Append to the list
        serial_qr_pairs.append((serial_number, img_filename, 'None'))

# Save serial numbers and QR code image filenames to a CSV file
with open('PPP-serial_qrcodes.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Serial Number', 'QR Code Image', 'Name'])
    csvwriter.writerows(serial_qr_pairs)

print("QR codes generated and saved successfully.")