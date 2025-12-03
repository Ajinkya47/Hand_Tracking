"""
Configuration parameters for the hand tracking POC
"""

import cv2

# Camera settings
CAMERA_ID = 0  # 0 for default webcam
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Skin detection (HSV ranges)
SKIN_LOWER_HSV = (0, 20, 70)    # Lower bound for skin color in HSV
SKIN_UPPER_HSV = (20, 255, 255) # Upper bound for skin color in HSV

# Morphological operations
KERNEL_SIZE = (5, 5)
ITERATIONS = 2

# Virtual object settings
VIRTUAL_OBJECT_CENTER = (320, 240)  # Center of the screen
VIRTUAL_OBJECT_RADIUS = 80          # Circle radius
VIRTUAL_OBJECT_WIDTH = 160          # Alternative: rectangle width
VIRTUAL_OBJECT_HEIGHT = 120         # Alternative: rectangle height

# State thresholds (in pixels)
SAFE_THRESHOLD = 150    # Distance > 150 = SAFE
WARNING_THRESHOLD = 80  # 80 < Distance <= 150 = WARNING
DANGER_THRESHOLD = 30   # Distance <= 80 = DANGER (Added this line)

# Colors (BGR format)
COLOR_SAFE = (0, 255, 0)      # Green
COLOR_WARNING = (0, 255, 255) # Yellow
COLOR_DANGER = (0, 0, 255)    # Red
COLOR_TEXT = (255, 255, 255)  # White
COLOR_TRACKER = (255, 0, 0)   # Blue

# Display settings
TEXT_SCALE = 0.7
TEXT_THICKNESS = 2
FONT = cv2.FONT_HERSHEY_SIMPLEX

# Performance
TARGET_FPS = 8
FRAME_SKIP = 1  # Process every nth frame (for optimization)