"""
FPS monitoring and performance optimization
"""

import time
import cv2
from config import *

class PerformanceMonitor:
    def __init__(self):
        self.frame_count = 0
        self.fps = 0
        self.start_time = time.time()
        self.frame_times = []
        self.target_fps = TARGET_FPS
        
    def update(self):
        """Update FPS calculation"""
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        
        if elapsed > 1.0:  # Update FPS every second
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = time.time()
            
        return self.fps
    
    def check_performance(self):
        """Check if performance meets target"""
        return self.fps >= self.target_fps
    
    def adjust_processing(self, current_fps):
        """Dynamically adjust processing based on current FPS"""
        # Simple adaptive frame skipping
        if current_fps < self.target_fps - 2:
            return 2  # Skip every other frame
        elif current_fps > self.target_fps + 5:
            return 1  # Process all frames
        else:
            return 1  # Default