# Dextera - Gesture Controlled Virtual Mouse

**Dextera** is a Python-based desktop application that allows users to control their system's mouse using hand gestures via webcam. Built using **MediaPipe**, **OpenCV**, and **PyAutoGUI**, Dextera provides a touchless way to navigate, click, drag, and scroll with simple hand movements.

---

## Features

- **Virtual Mouse Movement** – Move the cursor using hand gestures
- **Left Click & Right Click** – Pinch gestures trigger left and right clicks
- **Drag and Drop** – Pinch and hold gesture to simulate drag actions
- **Scroll Mode** – Raise index finger to enter scroll mode and move hand up/down to scroll
- **Real-time FPS Display** – Displays current frame rate to monitor performance
- **Hand Detection** – Supports multiple hands using MediaPipe’s hand landmark tracking

---

## Demo

> *(Optional: You can add a GIF or YouTube link here to show a demo of Dextera in action)*

---

## Technologies Used

- **Python 3.x**
- **OpenCV** – For real-time webcam capture and image processing
- **MediaPipe** – Hand tracking using 21 hand landmarks
- **PyAutoGUI** – To control mouse functions like move, click, drag, and scroll

---

## File Structure
```
Dextera/
│
├── Dextera.py                 # Main application file
├── hand_detector.py          # Handles hand detection using MediaPipe
├── gesture_recognition.py    # Contains gesture logic (scroll, drag, etc.)
├── basic_hand_detection.py   # Standalone script for simple hand landmark test
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/dextera
   cd dextera
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python Dextera.py
   ```

---
   
## How It Works

- **Cursor Movement**  
  The system cursor is moved based on the index fingertip position using `pyautogui.moveTo()`.

- **Left Click (Thumb + Index)**  
  When the thumb and index fingertip come close together (pinch), a left click is triggered.

- **Right Click (Thumb + Middle)**  
  A pinch between the thumb and middle fingertip triggers a right click.

- **Drag and Drop (Thumb + Ring, Held)**  
  Pinching the ring finger with the thumb and holding it for a short duration triggers `mouseDown()`. Releasing ends it with `mouseUp()`.

- **Scroll Mode (Raised Index Finger)**  
  When the index finger is raised above the thumb, scroll mode is activated. Moving the hand up or down scrolls the screen accordingly.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

📧 **Email**: yourname@example.com  
🔗 **GitHub**: [your-username](https://github.com/your-username)

---

## Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!
