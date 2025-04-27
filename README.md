# PPP Event QR Code Ticket System

This project provides a complete QR Code ticketing system for the PPP Event. It includes:

- **QR Code Generation** with serial numbers for Day 1 and Day 2
- **Framing QR Codes** with event-specific backgrounds
- **Real-time QR Code Scanning and Verification** using a webcam


## Project Structure

```
PPP-QR-Code/                # Folder where raw QR codes are saved
Framed-QR-Codes/            # Folder where framed QR codes are saved
PPP-serial_qrcodes.csv      # CSV file storing serial numbers and names
ticketDay02Verify.csv       # CSV file recording verified QR scans
GenerateDay1&2.py           # Script to generate QR codes
frameGenerator.py           # Script to frame QR codes
verify.py                   # Script to scan and verify QR codes
PPP_QR_DAy1.png             # Background frame for Day 1 QR codes
PPP_QR_DAy2.png             # Background frame for Day 2 QR codes
```

## Requirements

- Python 3.x
- Libraries:
  - `qrcode`
  - `Pillow`
  - `opencv-python`
  - `pyzbar`
  - `numpy`
  - `winsound` (Windows only)

Install required libraries:

```bash
pip install qrcode pillow opencv-python pyzbar numpy
```

## How It Works

### 1. QR Code Generation

- Generates random serial numbers following the format:
  - Day 1: `D1PPP######`
  - Day 2: `D2PPP######`
- Creates QR code images for each serial number.
- Saves both the images and serial numbers into a CSV file (`PPP-serial_qrcodes.csv`).

### 2. QR Code Framing

- Frames each generated QR code onto a custom event background:
  - **Day 1** QR codes use `PPP_QR_DAy1.png`
  - **Day 2** QR codes use `PPP_QR_DAy2.png`
- Saves the framed QR codes in the `Framed-QR-Codes/` directory.

### 3. QR Code Scanning and Verification

- Opens the webcam to scan QR codes in real-time.
- Verifies scanned codes based on the generated serial numbers.
- Behavior:
  - ✅ **Green** Frame: Successfully verified Day 1 ticket (first scan).
  - 🧡 **Orange** Frame: Ticket already verified earlier.
  - 💜 **Purple** Frame: Day 2 ticket detected (cannot verify for Day 1 event).
  - ❌ **Red** Frame: Invalid ticket.
- Saves verification logs (serial number, name, timestamp) into `ticketDay02Verify.csv`.

## Notes

- The project **separates Day 1 and Day 2 tickets** using the serial prefix (`D1`, `D2`).
- This project currently supports scanning only for **Day 1** event.
- If the same QR code is scanned again after verification, it will show a different color to indicate it's already verified.
- **winsound** is used to play a beep on successful verification. (If you're not using Windows, you may need to comment it out.)
- Make sure the paths for the QR code images and frame images are correctly set according to your directory.

## UI/UX Limitation

- When the QR code is verified successfully! You may not see the green frame because verification happens very fast. Please listen for the confirmation sound.

## Author

✨ Developed for the **PPP Event Ticketing System**.

