import csv
import os  # Import os to check file existence and size
import winsound  # Importing winsound for sound
from datetime import datetime

import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Load the serial numbers and corresponding names from the CSV file (use absolute path)
serial_qrcode_map = {}
with open('PPP-serial_qrcodes.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        serial_qrcode_map[row[0]] = row[2]  # Map serial number to name

# Initialize the webcam: If you're using a different camera, change the index to 1 (0 for default camera)
cap = cv2.VideoCapture(0)

# Path to verification file
verify_csv_path = 'ticketDay02Verify.csv'

# Check if the file exists and is empty
file_exists = os.path.exists(verify_csv_path)
is_empty = os.path.getsize(verify_csv_path) == 0 if file_exists else True

# Load previously verified serial numbers
verified_serial_numbers = set()
if file_exists:
    with open(verify_csv_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip header if present
        for row in csvreader:
            verified_serial_numbers.add(row[2])  # Add serial number to the verified set
            if len(row) >= 3:
                name = row[2] if row[2] != 'None' else None
                serial_qrcode_map[row[0]] = name  # Map serial number to name
        else:
            print(f"Skipping row due to insufficient columns: {row}")

# Open the CSV file to save verification records in append mode
with open(verify_csv_path, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write the header only if the file does not already exist or is empty
    if is_empty:
        csvwriter.writerow(['Num', 'Name', 'Serial Number', 'Timestamp'])

    # Dictionary to track verification and reappearance state of each QR code
    qr_status = {}
    
    # Initialize a counter for verified QR codes
    verified_count = len(verified_serial_numbers)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            break
        
        # Decode the QR code
        decoded_objects = decode(frame)
        current_qr_codes = set()  # Track QR codes detected in this frame

        for obj in decoded_objects:
            serial_number = obj.data.decode('utf-8')
            current_qr_codes.add(serial_number)  # Add to currently detected QR codes

            # Determine the points of the QR code to draw a frame around it
            points = obj.polygon
            if len(points) == 4:  # If the QR code is a rectangle
                hull = points
            else:  # If the QR code is not a rectangle, use convex hull
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            
            hull = list(map(tuple, hull))

            # Initialize qr_status for the current serial number if it doesn't exist
            if serial_number not in qr_status:
                qr_status[serial_number] = {"status": None, "timestamp": None, "disappeared": True}

            # Check if the QR code starts with "D1" or "D2"
            if serial_number.startswith("D1"):
                if serial_number in serial_qrcode_map:  # Check if it exists in the mapping
                    name = serial_qrcode_map[serial_number]
                    if name is None:
                        name = 'Unknown'  # Or handle it in another way if needed
                    if serial_number in verified_serial_numbers:
                        # QR code has reappeared after disappearing (show orange frame)
                        if qr_status[serial_number]["disappeared"]:
                            color = (0, 165, 255)  # Orange for previously verified
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            phrase = f"Already verified: {timestamp}"
                            # Display the phrase on the frame
                            cv2.putText(frame, phrase, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                        else:
                            # If it has been continuously detected, keep showing the phrase
                            timestamp = qr_status[serial_number]["timestamp"]
                            phrase = f"Already verified: {timestamp}"
                            cv2.putText(frame, phrase, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

                        # Update the disappearance status to False (indicating it's visible again)
                        qr_status[serial_number]["disappeared"] = False

                    else:
                        # First-time verification (show green frame)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        verified_count += 1  # Increment the count
                        print(f"Verified QR Code: {serial_number} at {timestamp}")
                        # Write count, name, serial number, and timestamp to CSV
                        csvwriter.writerow([verified_count, name, serial_number, timestamp])
                        csvfile.flush()  # Ensure data is saved
                        verified_serial_numbers.add(serial_number)  # Mark as verified
                        qr_status[serial_number] = {"status": "Verified", "timestamp": timestamp, "disappeared": False}
                        
                        # Play beep sound
                        winsound.Beep(1000, 800)  # Frequency: 1000 Hz, Duration: 800 ms

                        color = (0, 255, 0)  # Green for first-time verified
                        verify_phrase = f"Verified: {timestamp}"
                        cv2.putText(frame, verify_phrase, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                else:
                    # QR code is not in valid serial numbers (show red frame)
                    if serial_number not in qr_status:  # Only log "Not Verified" once
                        print(f"Not verified: {serial_number}")
                        qr_status[serial_number] = {"status": "Not Verified", "disappeared": False}
                    color = (0, 0, 255)  # Red for not verified

            elif serial_number.startswith("D2"):
                # Show purple frame and message for D2 serial numbers
                color = (128, 0, 128)  # Purple color
                phrase = "The ticket is on day 2nd"
                cv2.putText(frame, phrase, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 0, 128), 2)

                # Mark as verified for D2 but without adding to the verified count
                if serial_number not in qr_status:
                    qr_status[serial_number] = {"status": "D2 Ticket", "disappeared": False}
                    
            else:
                # QR code is not verified (show red frame)
                if serial_number not in qr_status:  # Only log "Not Verified" once
                    print(f"Not verified: {serial_number}")
                    qr_status[serial_number] = {"status": "Not Verified", "disappeared": False}
                color = (0, 0, 255)  # Red for not verified

            # Draw the frame around the QR code only if the hull is valid
            if len(hull) > 0 and isinstance(hull[0], tuple) and len(hull[0]) == 2:
                for j in range(len(hull)):
                    cv2.line(frame, hull[j], hull[(j + 1) % len(hull)], color, 3)

        # Update QR codes that have disappeared from the frame
        disappeared_qr_codes = set(qr_status.keys()) - current_qr_codes
        for qr_code in disappeared_qr_codes:
            if qr_status[qr_code]["status"] == "Verified":
                qr_status[qr_code]["disappeared"] = True  # Mark as disappeared when it is no longer detected

        # Display the frame
        cv2.imshow('QR Code Scanner', frame)
        
        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()