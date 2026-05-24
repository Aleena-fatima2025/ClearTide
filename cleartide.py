import cv2
import serial
import time
from ultralytics import YOLO

# ==========================================
# 1. INITIALIZATION & SETUP
# ==========================================
# Initialize Serial Communication with Microcontroller (STM32/Arduino)
# Update 'COM3' or '/dev/ttyUSB0' and baudrate to match your hardware setup
try:
    mc_serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    print("[SYSTEM] Serial connection to Microcontroller established.")
except Exception as e:
    print(f"[WARNING] Serial connection failed: {e}. Running in Vision-Only mode.")
    mc_serial = None

# Load the YOLOv8 Nano model (downloads automatically if not present)
# For production, replace 'yolov8n.pt' with your custom-trained marine debris weights (e.g., 'best.pt')
print("[SYSTEM] Loading YOLOv8 AI Model...")
model = YOLO('yolov8n.pt') 

# Initialize the camera (0 is usually the built-in webcam or PiCamera)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("[SYSTEM] Vision System Active. Starting inference loop...")

# ==========================================
# 2. AI INFERENCE & CONTROL LOOP
# ==========================================
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("[ERROR] Failed to grab frame from camera.")
        break

    # Run YOLOv8 inference on the current frame
    # conf=0.5 ensures we only process confident detections
    results = model.predict(source=frame, conf=0.5, verbose=False)
    
    # Extract detection data
    for result in results:
        boxes = result.boxes
        
        for box in boxes:
            # Get bounding box coordinates (x1, y1, x2, y2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Calculate the center point of the detected object
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            
            # Get class ID and confidence score
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model.names[cls_id]

            # ---------------------------------------------------------
            # INDUSTRY 4.0 CONTROL LOGIC: Send data to Microcontroller
            # ---------------------------------------------------------
            # Example protocol: <CLASS_ID, CENTER_X, CENTER_Y>
            # The MCU's PID controller can use Center_X to adjust the steering MV
            if mc_serial:
                data_packet = f"<{cls_id},{center_x},{center_y}>\n"
                mc_serial.write(data_packet.encode('utf-8'))
            
            # Draw visual overlays for remote monitoring/debugging
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1) # Mark center

    # Display the processed frame
    cv2.imshow("Sea-Sweeper AI Vision", frame)

    # Press 'q' to gracefully exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ==========================================
# 3. CLEANUP
# ==========================================
cap.release()
cv2.destroyAllWindows()
if mc_serial:
    mc_serial.close()
print("[SYSTEM] System shutdown complete.")
