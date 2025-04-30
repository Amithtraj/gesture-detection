# Hand Gesture Detection System

## Features

- Real-time hand gesture recognition using webcam
- Supports multiple gestures (Thumbs Up, Victory sign)
- REST API endpoint for image processing
- Interactive web interface
+ Interactive web interface
+ Toggle button to enable/disable mouse control
+ Trackpad mode: move cursor with pointing gesture, click with fist gesture

## Requirements

- Python 3.8+
- OpenCV 4.5+
- MediaPipe 0.8+
- Django 4.0+
- NumPy

## Installation

```bash
pip install django opencv-python mediapipe numpy
```

## Project Setup

1. Clone repository
2. Run migrations:

```bash
python manage.py migrate
```

3. Start development server:

```bash
python manage.py runserver
```

## Gesture Recognition

Currently supported gestures:

- ✅ Thumbs Up
- ✅ Victory Sign (Index + Middle fingers)
- ✅ Open Palm
- ✅ Fist
- ✅ Pointing

## Usage

1. Access web interface at `http://localhost:8000`
2. Allow camera access
3. Use the toggle button to enable or disable mouse control
4. Perform gestures in front of webcam:
   - **Pointing**: Move the cursor like a trackpad (relative movement)
   - **Fist**: Perform a mouse click
   - Other gestures (Thumbs Up, Victory, Open Palm) are detected and displayed but do not control the mouse

## Detection Logic

The system recognizes gestures based on finger landmark positions:

- 👍 Thumbs Up: Thumb extended upward, other fingers closed
- ✌️ Victory: Index and middle fingers raised, others closed
- 🖐 Open Palm: All fingers fully extended
- ✊ Fist: All fingers closed tightly
- 👆 Pointing: Index finger extended, others closed

## API Usage

**Endpoint:** `/detect/`

**POST Request:**

```json
{
  "image": "data:image/jpeg;base64,/9j/..."
}
```

**Response:**

```json
{
  "processed_image": "base64_string",
  "gestures": ["Thumbs Up"]
}
```

## Real-time Webcam Feed

Access `http://localhost:8000/detect` directly for MJPEG stream

## Technical Specifications

- MediaPipe Hand Landmark model
- Custom gesture detection algorithm
- 30 FPS processing @ 640x480 resolution
- Multi-hand detection support

## Mouse Control (Trackpad Mode)

- When mouse control is enabled, use the **Pointing** gesture to move the cursor relative to your finger's movement (trackpad style).
- Use the **Fist** gesture to perform a mouse click.
- Mouse control is only active when the toggle is enabled.
