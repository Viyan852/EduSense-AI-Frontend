from flask import Flask, Response, jsonify
import cv2
import random
import time

app = Flask(__name__)

# -----------------------------
# Webcam
# -----------------------------
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Could not open webcam.")

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# OpenCV's built-in face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# -----------------------------
# Demo state
# -----------------------------
start_time = time.time()

demo_state = {
    "noise": 35,
    "cpu": 18,
    "ram": 42,
    "temperature": 43,
    "fps": 24,
}


def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            time.sleep(0.05)
            continue

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )

        # Draw detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 220, 120),
                2,
            )

            cv2.putText(
                frame,
                "Face detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 220, 120),
                2,
            )

        # Small demo label
        cv2.putText(
            frame,
            f"EduSense DEMO | Faces: {len(faces)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        # Encode JPEG
        success, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 80],
        )

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


# -----------------------------
# Live webcam stream
# -----------------------------
@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


# -----------------------------
# Dashboard API
# -----------------------------
@app.route("/api/data")
def api_data():

    detected_faces = []

    # Quick webcam snapshot for API statistics
    success, frame = camera.read()

    if success:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )

        for i, _ in enumerate(faces):
            detected_faces.append({
                "name": f"Demo Student {i + 1}",
                "confidence": random.randint(91, 99),
                "emotion": random.choice(
                    ["Happy", "Neutral", "Surprise"]
                ),
                "status": "Present",
            })

    face_count = len(detected_faces)

    # Slowly changing demo telemetry
    demo_state["noise"] = max(
        5,
        min(100, demo_state["noise"] + random.randint(-4, 4))
    )

    demo_state["cpu"] = max(
        5,
        min(95, demo_state["cpu"] + random.randint(-3, 3))
    )

    demo_state["ram"] = max(
        20,
        min(90, demo_state["ram"] + random.randint(-2, 2))
    )

    demo_state["temperature"] = max(
        35,
        min(75, demo_state["temperature"] + random.randint(-1, 1))
    )

    demo_state["fps"] = max(
        15,
        min(30, demo_state["fps"] + random.randint(-1, 1))
    )

    # Demo emotion distribution
    emotions = {
        "happy": random.randint(5, 12),
        "neutral": random.randint(8, 18),
        "surprise": random.randint(0, 3),
        "sad": random.randint(0, 3),
        "angry": random.randint(0, 2),
    }

    total_students = 30

    # Demo attendance
    present = min(
        total_students,
        max(0, 20 + face_count)
    )

    unknown_faces = random.randint(0, 2)

    engagement = random.randint(72, 94)

    return jsonify({
        "students": {
            "present_count": present
        },

        "total_students": total_students,

        "unknown_faces": unknown_faces,

        "engagement": engagement,

        "noise": demo_state["noise"],

        "cpu": demo_state["cpu"],

        "ram": demo_state["ram"],

        "temperature": demo_state["temperature"],

        "fps": demo_state["fps"],

        "teacher": True,

        "emotions": emotions,

        "camera_url": "http://127.0.0.1:5000/video",

        "faces": detected_faces,

        "logs": [
            {
                "time": time.strftime("%H:%M:%S"),
                "message": f"{face_count} face(s) detected by demo webcam"
            }
        ],

        "alerts": [],

        "server": {
            "mode": "DEMO",
            "uptime": round(time.time() - start_time, 1)
        }
    })


# -----------------------------
# Health check
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "EduSense Demo Server",
        "mode": "webcam-demo"
    })


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("EduSense AI - Webcam Demo Server")
    print("=" * 50)
    print("Dashboard API : http://127.0.0.1:5000/api/data")
    print("Webcam stream : http://127.0.0.1:5000/video")
    print("Server        : http://127.0.0.1:5000")
    print("=" * 50)

    try:
        app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            threaded=True,
        )
    finally:
        camera.release()