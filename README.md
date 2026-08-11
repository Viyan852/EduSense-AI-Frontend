# EduSense AI — Smart Classroom Dashboard

EduSense AI is a real-time smart classroom monitoring dashboard designed to provide a centralized interface for classroom analytics, attendance, student recognition, emotion analysis, engagement monitoring, noise monitoring, camera streaming, and system telemetry.

The frontend is contained in a single `index.html` file and communicates with a separate EduSense backend through an HTTP API.

---

## Overview

EduSense AI follows a frontend/backend architecture:

    Camera / Sensors
          │
          ▼
    ┌─────────────────────┐
    │   EduSense Backend  │
    │                     │
    │ Face Recognition    │
    │ Emotion Detection   │
    │ Attendance          │
    │ Engagement Analysis │
    │ Noise Monitoring    │
    │ System Telemetry    │
    └──────────┬──────────┘
               │
            JSON API
               │
               ▼
    ┌─────────────────────┐
    │  EduSense Dashboard │
    │      index.html     │
    │                     │
    │ Attendance          │
    │ Students            │
    │ Emotions            │
    │ Camera              │
    │ Engagement          │
    │ Noise               │
    │ System Health       │
    │ Logs & Alerts       │
    └─────────────────────┘

The dashboard is responsible for displaying and interacting with backend data.

The actual AI processing is performed by the backend.

---

## Main Features

### Real-Time Dashboard

Displays classroom information received from the backend, including:

- Present students
- Total students
- Unknown faces
- Attendance percentage
- Class engagement
- Noise level
- Teacher status
- CPU usage
- RAM usage
- Temperature
- Processing FPS

---

## Student Recognition

The dashboard can display recognized students returned by the backend.

Supported information can include:

- Student name
- Recognition confidence
- Detected emotion
- Attendance status

Example:

    {
      "name": "Student 1",
      "confidence": 97,
      "emotion": "Happy",
      "status": "Present"
    }

The dashboard does not independently perform face recognition.

---

## Emotion Analytics

EduSense can display emotion information received from the backend.

Supported emotion categories include:

- Happy
- Neutral
- Surprise
- Sad
- Angry

The frontend visualizes the received values using charts.

The chart should remain data-driven and must not invent classroom statistics.

---

## Camera Feed

The dashboard supports a backend-provided camera stream.

Depending on the backend implementation, the API may provide fields such as:

    camera_url
    stream_url
    video_url
    mjpeg_url

The dashboard can display the returned camera source.

Camera controls may include:

- Camera refresh
- Fullscreen mode
- Stream status

The actual camera capture and processing are handled outside the frontend.

---

## Backend Connection

The dashboard connects to the EduSense backend using its API URL.

Example:

    http://192.168.1.100:5000

The frontend communicates with:

    /api/data

Example:

    http://192.168.1.100:5000/api/data

The backend must be running and accessible from the device running the dashboard.

---

## API Data

The dashboard expects structured JSON from the backend.

A simplified example:

    {
      "students": {
        "present_count": 23
      },
      "total_students": 30,
      "unknown_faces": 2,
      "engagement": 87,
      "noise": 42,
      "cpu": 35,
      "ram": 61,
      "temperature": 48,
      "fps": 25,
      "teacher": true,
      "emotions": {
        "happy": 8,
        "neutral": 12,
        "surprise": 1,
        "sad": 2,
        "angry": 0
      },
      "camera_url": "http://192.168.1.100:5000/video",
      "faces": [
        {
          "name": "Student 1",
          "confidence": 97,
          "emotion": "Happy",
          "status": "Present"
        }
      ]
    }

The exact backend schema should match the final backend implementation.

---

## No Fake Production Data

The final dashboard is designed to be data-driven.

It should not generate random classroom statistics to simulate AI results during normal operation.

If the backend is unavailable, the dashboard should show an appropriate disconnected, unavailable, or error state rather than presenting simulated classroom measurements as real data.

For development and demonstration, a separate demo server can be used.

---

## Demo Server

A lightweight demo backend can be used to test the frontend before connecting the actual AI hardware/backend.

Example:

    demo_server.py

The demo server can provide test JSON responses through:

    /api/data

This allows the frontend to be tested independently of the Raspberry Pi, camera, sensors, and AI models.

The demo server is for development/testing only.

---

## System Monitoring

The dashboard can display backend-provided system telemetry such as:

- CPU usage
- RAM usage
- Temperature
- FPS

These values should originate from the backend/system being monitored.

The frontend should not claim that it is measuring Raspberry Pi hardware unless the backend actually provides those measurements.

---

## Logs, Alerts and Events

The dashboard supports displaying backend-generated system information such as:

- Information messages
- Warnings
- Errors
- System events
- Backend logs
- Camera errors
- Connection errors

This provides a central place for monitoring the state of the EduSense system.

---

## Connection Handling

The frontend includes connection-management logic for situations such as:

- Backend available
- Backend unavailable
- Connection timeout
- Temporary network failure
- Backend recovery
- API errors
- Reconnection

The dashboard can automatically attempt to reconnect when appropriate.

---

## Refresh and Polling

The dashboard periodically requests updated backend information.

The polling interval is controlled by the frontend implementation.

A manual refresh control can also be used to request the latest available backend data.

The frontend should avoid displaying stale data as if it were current.

---

## Theme Support

EduSense supports light/dark interface modes.

The selected theme can be stored locally so that the dashboard remembers the user's preference after refreshing the page.

---

## Developer / Debug Tools

The dashboard includes developer-oriented diagnostics for troubleshooting the connection between the frontend and backend.

The debug panel can expose information such as:

- Backend URL
- Connection status
- Last successful poll
- Last API response
- Error count
- Raw backend JSON

This is intended for development and testing.

---

## Technology

The frontend is designed to run using standard web technologies:

- HTML5
- CSS3
- JavaScript
- Fetch API
- Chart.js where applicable
- Browser Local Storage

No frontend framework is required.

The main dashboard is designed around:

    index.html

---

## Project Structure

A typical EduSense project can be organized as:

    EduSense/
    │
    ├── index.html
    │
    ├── backend/
    │   ├── app.py
    │   ├── face_detect.py
    │   ├── emotion_detection.py
    │   └── ...
    │
    ├── assets/
    │   ├── images/
    │   ├── icons/
    │   └── ...
    │
    └── demo/
        └── demo_server.py

The exact structure may differ depending on the final backend implementation.

---

## Running the Frontend

The dashboard can be opened in a modern web browser.

For local testing, it is recommended to serve the project through a local HTTP server rather than relying on `file://` when browser security restrictions affect API requests or camera resources.

The backend should be running before attempting to connect.

---

## Connecting to the Backend

1. Start the EduSense backend.
2. Find the backend device's local network IP address.
3. Enter the backend URL in the dashboard.
4. Connect to the backend.
5. Confirm that the dashboard reports an active connection.
6. Verify that `/api/data` is returning valid JSON.
7. Confirm that live classroom values appear.
8. Verify the camera stream if enabled.

Example backend:

    http://192.168.1.100:5000

Example API:

    http://192.168.1.100:5000/api/data

---

## Network Requirements

For a local Raspberry Pi deployment:

- The computer and Raspberry Pi should normally be on the same local network.
- The backend port must be reachable.
- The firewall must allow the required connection.
- The API must listen on an accessible network interface.
- Camera stream URLs must also be reachable by the browser.

---

## Important Security Notes

EduSense may process sensitive classroom information.

Do not expose the backend directly to the public internet without appropriate security controls.

Recommended production practices include:

- Authentication
- Access control
- HTTPS
- Secure API endpoints
- Input validation
- Proper CORS configuration
- Protection of student information
- Secure storage of recognition data
- Avoiding unnecessary personal data collection

The dashboard itself should not be treated as a security boundary.

---

## Troubleshooting

### Dashboard says disconnected

Check:

1. Is the backend running?
2. Is the IP address correct?
3. Is the backend port correct?
4. Can the browser reach `/api/data`?
5. Are the computer and backend device on the same network?
6. Is the firewall blocking the connection?

---

### Dashboard connects but values do not appear

Check the response from:

    /api/data

Make sure it returns valid JSON and that the field names match the frontend's expected schema.

---

### Camera does not appear

Check:

- Camera backend is running.
- Camera URL is correct.
- Stream endpoint is accessible.
- Browser can reach the stream.
- The returned URL is compatible with the browser.
- Network/firewall rules are not blocking the stream.

---

### Charts are empty

Check whether the backend is returning valid emotion/attendance data.

The frontend should not populate charts with random values.

---

## Development Philosophy

EduSense follows a clear separation between:

### Frontend

Responsible for:

- User interface
- Visualization
- Controls
- API communication
- Connection state
- Data presentation
- User feedback

### Backend

Responsible for:

- Camera capture
- Sensor input
- Face recognition
- Emotion detection
- Attendance processing
- Engagement analysis
- Noise analysis
- Hardware/system telemetry
- AI inference
- API responses

This separation makes the dashboard easier to test, maintain and upgrade.

---

## Demo vs Production

### Demo Mode

The demo server provides controlled test data so the dashboard can be tested without the complete hardware/AI system.

Useful for:

- UI testing
- API testing
- Presentation
- Development
- Debugging

### Production Mode

The real backend provides live information from:

- Camera
- AI models
- Raspberry Pi
- Sensors
- Classroom analysis

Production values must come from real backend processing.

---

## Current Status

EduSense AI consists of a frontend dashboard and a separate backend architecture.

The frontend is designed to operate as the visualization and control layer while the backend performs the actual classroom monitoring and AI processing.

The demo backend can be used independently to verify frontend functionality before deploying the complete hardware system.

---

## License

This project is intended for educational, experimental and demonstration purposes.

Before deploying EduSense in a real classroom, review applicable privacy, consent, data protection and school policies.

---

## EduSense AI

Smart classroom monitoring and analytics.

Camera → AI → Backend → API → Dashboard

Built as an educational AI + hardware project.