import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load video and models
cap = cv2.VideoCapture("cctv_feed.mp4")
model = YOLO("yolov8n.pt")
tracker = DeepSort()

# Control variables
suspect_id = None
id_selected = False
frame_count = 0
delay_frames = 30  # Delay ~1 second before asking for input

print("Starting video... press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Step 1: Detect people
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        if int(box.cls[0]) == 0:  # class 0 = person
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, 'person'))

    # Step 2: Track people
    tracks = tracker.update_tracks(detections, frame=frame)

    # Step 3: Draw and collect IDs
    current_ids = []
    for track in tracks:
        if not track.is_confirmed():
            continue

        tid = int(track.track_id)
        x1, y1, x2, y2 = map(int, track.to_ltrb())
        current_ids.append(tid)

        # Draw suspect in red
        if suspect_id == tid:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, f"Suspect {tid}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            # Draw others in green
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {tid}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Step 4: Ask for suspect ID after 30 frames & if IDs are shown
    if not id_selected and frame_count > delay_frames and len(current_ids) > 0:
        print("\n👤 People detected with IDs:")
        for tid in current_ids:
            print(f"- ID {tid}")

        while True:
            try:
                entered = input("Enter suspect ID to track: ")
                entered = int(entered)
                if entered in current_ids:
                    suspect_id = entered
                    print(f"Tracking suspect {suspect_id}")
                    break
                else:
                    print("ID not found. Try again.")
            except ValueError:
                print("Please enter a valid number.")
        id_selected = True

    # Step 5: Show video
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
