# CCTV Suspect Tracking System 

This project enables tracking of a specific person (suspect) in CCTV footage using object detection and multi-object tracking. It uses YOLOv8 for detecting people and Deep SORT for assigning and maintaining consistent tracking IDs across video frames. The user can select a suspect based on the ID, and the system will track that person across the footage.

## Features

- Detects all people in video frames using YOLOv8
- Assigns unique IDs to individuals using Deep SORT
- User can select a suspect by entering their ID
- Tracks and highlights the suspect with a red bounding box
- Others are marked with green bounding boxes

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

3. Wait for green boxes and IDs to appear on the video.
4. Enter the desired suspect ID when prompted in the terminal.
5. The selected suspect will be tracked in red. Press `q` to quit the video.

## Usage Notes

- If no people are detected in the first few frames, the ID prompt will be delayed until valid tracking IDs are available.
- The system currently supports selecting only one suspect. Multiple suspect tracking can be implemented as an enhancement.

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

