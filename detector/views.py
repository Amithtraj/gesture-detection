from django.http import HttpResponse, StreamingHttpResponse
import base64

import cv2
import mediapipe as mp
import numpy as np
import json
import base64

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'detector/index.html')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_gesture(landmarks):
    # Thumb up detection
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    
    # Victory sign detection (index and middle fingers up)
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    
    # Get additional landmarks for new gestures
    index_dip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    middle_dip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    ring_dip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
    pinky_dip = landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]

    # Open palm detection (all fingers extended)
    if (index_tip.y < index_dip.y and
        middle_tip.y < middle_dip.y and
        ring_tip.y < ring_dip.y and
        pinky_tip.y < pinky_dip.y):
        return 'Open Palm'

    # Fist detection (all fingers closed)
    if (index_tip.y > index_dip.y and
        middle_tip.y > middle_dip.y and
        ring_tip.y > ring_dip.y and
        pinky_tip.y > pinky_dip.y and
        thumb_tip.y > thumb_ip.y):
        return 'Fist'

    # Pointing gesture (index extended, others closed)
    if (index_tip.y < index_dip.y and
        middle_tip.y > middle_dip.y and
        ring_tip.y > ring_dip.y and
        pinky_tip.y > pinky_dip.y):
        return 'Pointing'
    
    if thumb_tip.y < thumb_ip.y and \
       index_tip.y < middle_tip.y and \
       ring_tip.y > middle_tip.y and \
       pinky_tip.y > middle_tip.y:
        return 'Thumbs Up'
    
    if index_tip.y < middle_tip.y and \
       middle_tip.y < ring_tip.y and \
       thumb_tip.x > index_tip.x:
        return 'Victory'
    
    return None

def gen():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame with MediaPipe
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect and display gesture
                gesture = get_gesture(hand_landmarks)
                if gesture:
                    cv2.putText(frame, gesture, (50, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@csrf_exempt
def detect_fingers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data['image'].split(',')[1]
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect and display gesture
                gesture = get_gesture(hand_landmarks)
                if gesture:
                    cv2.putText(frame, gesture, (50, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        _, buffer = cv2.imencode('.jpg', frame)
        processed_image = base64.b64encode(buffer).decode('utf-8')
        
        # Collect all detected gestures
        gestures = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = get_gesture(hand_landmarks)
                if gesture:
                    gestures.append(gesture)
        
        return HttpResponse(json.dumps({
            'processed_image': processed_image,
            'gestures': list(set(gestures))  # Remove duplicates
        }), content_type='application/json')
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
    return HttpResponse(status=405)
