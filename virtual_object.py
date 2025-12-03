"""
Virtual object/boundary management
"""

import cv2
import numpy as np
from config import *

class VirtualObject:
    def __init__(self, shape="circle"):
        self.shape = shape
        self.center = VIRTUAL_OBJECT_CENTER
        self.radius = VIRTUAL_OBJECT_RADIUS
        self.width = VIRTUAL_OBJECT_WIDTH
        self.height = VIRTUAL_OBJECT_HEIGHT
        self.color = COLOR_SAFE
        
    def draw(self, frame):
        """Draw virtual object on frame"""
        if self.shape == "circle":
            cv2.circle(frame, self.center, self.radius, self.color, 3)
            # Draw inner warning zone
            cv2.circle(frame, self.center, WARNING_THRESHOLD, COLOR_WARNING, 2)
            # Draw inner danger zone
            cv2.circle(frame, self.center, DANGER_THRESHOLD, COLOR_DANGER, 1)
            
        elif self.shape == "rectangle":
            top_left = (self.center[0] - self.width//2, self.center[1] - self.height//2)
            bottom_right = (self.center[0] + self.width//2, self.center[1] + self.height//2)
            cv2.rectangle(frame, top_left, bottom_right, self.color, 3)
            
        return frame
    
    def calculate_distance(self, hand_position):
        """Calculate distance from hand to virtual object"""
        if hand_position is None:
            return float('inf')
            
        if self.shape == "circle":
            # Distance to circle boundary
            dx = hand_position[0] - self.center[0]
            dy = hand_position[1] - self.center[1]
            distance_to_center = np.sqrt(dx**2 + dy**2)
            return distance_to_center - self.radius
            
        elif self.shape == "rectangle":
            # Distance to rectangle edges
            rect_left = self.center[0] - self.width//2
            rect_right = self.center[0] + self.width//2
            rect_top = self.center[1] - self.height//2
            rect_bottom = self.center[1] + self.height//2
            
            # Find closest point on rectangle
            closest_x = max(rect_left, min(hand_position[0], rect_right))
            closest_y = max(rect_top, min(hand_position[1], rect_bottom))
            
            dx = hand_position[0] - closest_x
            dy = hand_position[1] - closest_y
            
            return np.sqrt(dx**2 + dy**2)
    
    def set_color(self, color):
        """Update object color based on state"""
        self.color = color