import os
from PIL import Image

# Load the frame images for each prefix
frame_path_D1 = 'PPP_QR_DAy1.png'
frame_path_D2 = 'PPP_QR_DAy2.png'

frame_D1 = Image.open(frame_path_D1)
frame_D2 = Image.open(frame_path_D2)

# Directory where the QR code images are saved
qr_code_directory = 'C:/Users/User/OneDrive - Cambodia Academy of Digital Technology/Programming Languages/PPP Ticket System/PPP Ticket System - Name - Copy/PPP-QR-Code'

# Directory to save the framed QR codes
os.makedirs('Framed-QR-Codes', exist_ok=True)

# Loop through each QR code image
for qr_filename in os.listdir(qr_code_directory):
    if qr_filename.endswith('.png'):
        qr_path = os.path.join(qr_code_directory, qr_filename)

        # Open the QR code image
        qr_code = Image.open(qr_path)

        # Resize the QR code to fit into the frame (adjust dimensions as needed)
        qr_code = qr_code.resize((850, 840))  # Change (200, 200) to fit your frames

        # Determine the appropriate frame based on the prefix
        if qr_filename.startswith('D1'):
            framed_image = frame_D1.copy()
        elif qr_filename.startswith('D2'):
            framed_image = frame_D2.copy()
        else:
            continue  # Skip if the filename does not match the expected prefixes

        # Calculate the position to paste the QR code (centered)
        frame_width, frame_height = framed_image.size
        qr_width, qr_height = qr_code.size
        position = (205, 618)
        
        # Pasting
        framed_image.paste(qr_code, position)

        # Save the framed QR code image
        framed_image.save(f'Framed-QR-Codes/{qr_filename}')

print("QR codes framed and saved successfully.")
