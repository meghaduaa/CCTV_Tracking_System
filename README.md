# CCTV Suspect Tracking System 

This project enables tracking of a specific person (suspect) in CCTV footage using object detection and multi-object tracking. It uses YOLOv8 to detect people and Deep SORT to assign consistent tracking IDs across video frames.

The user can select a suspect to track based on a visible ID assigned to each person. The system then highlights that person throughout the footage and re-prompts every 10 seconds, allowing you to change the suspect being tracked.

## Features

- Detects people in each video frame using YOLOv8
- Assigns unique, consistent tracking IDs using Deep SORT
- Prompts the user to select a suspect ID after the first second
- Re-prompts the user every 10 seconds to reselect or change the suspect
- Selected suspect is shown with a red bounding box
- Other individuals are shown with green bounding boxes

## Technologies Used

- Python 3.8+
- OpenCV
- Ultralytics YOLOv8
- deep_sort_realtime (Deep SORT)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/CCTV_Suspect_Tracking.git
cd CCTV_Suspect_Tracking
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. (Optional) Download YOLOv8 model weights manually if needed:

```bash
from ultralytics import YOLO
YOLO('yolov8n.pt')
```

The script will automatically download the weights if not present.

## Project Structure

```
CCTV_Suspect_Tracking/
├── main.py                # Main tracking script
├── cctv_feed.mp4          # Sample CCTV video (you can replace this)
├── requirements.txt       # List of Python dependencies
├── README.md              # Project description and instructions
```

## How to Run

1. Ensure `cctv_feed.mp4` is in the same folder as `main.py`.
2. Run the script:

```bash
python main.py
```

3.Watch the video:
- After 1 second (≈30 frames), green boxes with unique IDs will appear.
- You will then be prompted in the terminal to enter the ID of the person to track.
4.The selected suspect will be marked with a red bounding box.
- Every 10 seconds, the system will again ask you to reselect (or skip by pressing Enter).
- Others remain highlighted in green.


## Usage Notes

- The system delays prompting for suspect selection until at least 1 second has passed and valid tracking IDs are visible on-screen.
- The suspect can be re-selected every 10 seconds, which is useful if IDs change or if you want to switch targets.
- If you press Enter without typing an ID, the current suspect continues to be tracked.

## Requirements

- Python 3.8 or higher
- opencv-python
- ultralytics
- deep_sort_realtime

You can install all requirements with:

```bash
pip install -r requirements.txt
```

## Future Improvements

- Support for tracking multiple suspects
- Saving the output video with annotations
- Integration with live webcam or real CCTV streams
- Logging of suspect movement

