# Hand Gesture Detection System

## Features

- Real-time hand gesture recognition using webcam
- Supports multiple gestures (Thumbs Up, Victory sign)
- REST API endpoint for image processing
- Interactive web interface

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
3. Perform gestures in front of webcam

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
