import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import time


cap = cv2.VideoCapture("cctv_feed.mp4")
model = YOLO("yolov8n.pt")
tracker = DeepSort()


suspect_id = None
frame_count = 0
fps = cap.get(cv2.CAP_PROP_FPS) or 30 
delay_frames = int(fps)  
ask_interval = 10  
last_ask_time = time.time()  

print("Starting video:")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        if int(box.cls[0]) == 0:  
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, 'person'))

    
    tracks = tracker.update_tracks(detections, frame=frame)


    current_ids = []
    for track in tracks:
        if not track.is_confirmed():
            continue

        tid = int(track.track_id)
        x1, y1, x2, y2 = map(int, track.to_ltrb())
        current_ids.append(tid)

        
        if suspect_id == tid:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, f"Suspect {tid}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {tid}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    
    if frame_count > delay_frames and len(current_ids) > 0:
        
        if time.time() - last_ask_time > ask_interval:
            print("\nPeople detected with IDs:")
            for tid in current_ids:
                print(f"- ID {tid}")
            while True:
                try:
                    entered = input("Enter suspect ID to track (or leave blank to keep current): ").strip()
                    if entered == "":
                        break
                    entered = int(entered)
                    if entered in current_ids:
                        suspect_id = entered
                        print(f"Now tracking suspect {suspect_id}")
                        break
                    else:
                        print("ID not found. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
            last_ask_time = time.time()

    
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
