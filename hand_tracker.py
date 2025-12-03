"""
Hand tracking using classical computer vision techniques
"""

import cv2
import numpy as np
from config import *

class HandTracker:
    def __init__(self):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, KERNEL_SIZE)
        self.previous_center = None
        self.smoothing_factor = 0.7
        
    def preprocess_frame(self, frame):
        """Preprocess frame for better skin detection"""
        # Resize for faster processing
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        
        return blurred
    
    def detect_skin(self, frame):
        """Detect skin-colored regions using HSV thresholding"""
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for skin color
        mask = cv2.inRange(hsv, SKIN_LOWER_HSV, SKIN_UPPER_HSV)
        
        # Apply morphological operations to clean up mask
        mask = cv2.erode(mask, self.kernel, iterations=ITERATIONS)
        mask = cv2.dilate(mask, self.kernel, iterations=ITERATIONS)
        
        # Apply Gaussian blur to mask
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        return mask
    
    def find_hand_contour(self, mask):
        """Find the largest contour (assumed to be hand)"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Filter out small contours (noise)
        if cv2.contourArea(largest_contour) < 1000:
            return None
        
        return largest_contour
    
    def get_hand_center(self, contour):
        """Calculate center point of hand contour"""
        # Calculate moments
        M = cv2.moments(contour)
        
        if M["m00"] == 0:
            return None
            
        # Calculate center coordinates
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        # Apply smoothing if previous center exists
        if self.previous_center is not None:
            cx = int(self.smoothing_factor * cx + (1 - self.smoothing_factor) * self.previous_center[0])
            cy = int(self.smoothing_factor * cy + (1 - self.smoothing_factor) * self.previous_center[1])
        
        self.previous_center = (cx, cy)
        return (cx, cy)
    
    def detect_fingertip(self, contour):
        """Alternative: Try to detect fingertip using convex hull"""
        try:
            # Calculate convex hull
            hull = cv2.convexHull(contour, returnPoints=False)
            
            if hull is None or len(hull) < 3:
                return self.get_hand_center(contour)
            
            # Find convexity defects
            defects = cv2.convexityDefects(contour, hull)
            
            if defects is None:
                return self.get_hand_center(contour)
            
            # Find the farthest point from convex hull defects (often fingertip)
            defects = defects[:, 0]
            farthest_point = None
            max_distance = 0
            
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i]
                if d > max_distance:
                    max_distance = d
                    farthest_point = tuple(contour[f][0])
            
            if farthest_point:
                return farthest_point
        
        except:
            pass
        
        # Fallback to center if fingertip detection fails
        return self.get_hand_center(contour)
    
    def track_hand(self, frame):
        """Main tracking function - returns hand position and visualization"""
        # Preprocess frame
        processed = self.preprocess_frame(frame)
        
        # Detect skin
        skin_mask = self.detect_skin(processed)
        
        # Find hand contour
        contour = self.find_hand_contour(skin_mask)
        
        if contour is None:
            return None, skin_mask
        
        # Get hand position (center or fingertip)
        # Using center for simplicity and stability
        hand_position = self.get_hand_center(contour)
        
        # Draw contour on mask for visualization
        mask_display = cv2.cvtColor(skin_mask, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(mask_display, [contour], -1, (0, 255, 0), 2)
        
        if hand_position:
            cv2.circle(mask_display, hand_position, 10, COLOR_TRACKER, -1)
            cv2.circle(mask_display, hand_position, 15, COLOR_TRACKER, 2)
        
        return hand_position, mask_display