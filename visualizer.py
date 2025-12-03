"""
Visualization and overlay rendering
"""

import cv2
import numpy as np
from config import *

class Visualizer:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        
    def draw_status_overlay(self, frame, state_manager, hand_position, distance):
        """Draw status overlay on frame"""
        # Draw state text
        state_text = f"STATE: {state_manager.get_state_text()}"
        cv2.putText(frame, state_text, (10, 30), FONT, TEXT_SCALE, 
                   state_manager.get_state_color(), TEXT_THICKNESS)
        
        # Draw distance information if hand is detected
        if hand_position is not None and distance != float('inf'):
            dist_text = f"Distance: {int(distance)}px"
            cv2.putText(frame, dist_text, (10, 60), FONT, 0.5, COLOR_TEXT, 1)
            
            # Draw line from hand to object center
            cv2.line(frame, hand_position, VIRTUAL_OBJECT_CENTER, (255, 255, 255), 1)
        
        # Draw danger warning if in DANGER state
        if state_manager.get_state_text() == "DANGER":
            # BUG FIX: Must assign the result back to 'frame'
            frame = self.draw_danger_warning(frame)
        
        return frame
    
    def draw_danger_warning(self, frame):
        """Draw prominent DANGER warning"""
        # Create semi-transparent red overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.frame_width, self.frame_height), 
                  COLOR_DANGER, -1)
        
        # This function creates a NEW frame, so we must return it
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Draw large DANGER text
        text = "DANGER DANGER"
        text_size = cv2.getTextSize(text, FONT, 1.5, 3)[0]
        text_x = (self.frame_width - text_size[0]) // 2
        text_y = (self.frame_height + text_size[1]) // 2
        
        cv2.putText(frame, text, (text_x, text_y), FONT, 1.5, 
                   COLOR_TEXT, 3, cv2.LINE_AA)
        cv2.putText(frame, text, (text_x, text_y), FONT, 1.5, 
                   COLOR_DANGER, 2, cv2.LINE_AA)
        
        # Draw blinking effect
        import time
        if int(time.time() * 2) % 2 == 0:
            cv2.circle(frame, VIRTUAL_OBJECT_CENTER, 10, COLOR_DANGER, -1)
        
        return frame
    
    def draw_fps(self, frame, fps):
        """Draw FPS counter"""
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(frame, fps_text, (self.frame_width - 100, 30), 
                   FONT, 0.5, COLOR_TEXT, 1)
        return frame
    
    def create_debug_display(self, main_frame, mask_frame, state_manager, fps):
        """Create side-by-side debug display"""
        # Resize mask to match main frame
        mask_resized = cv2.resize(mask_frame, (self.frame_width, self.frame_height))
        
        # Create combined display
        combined = np.hstack((main_frame, mask_resized))
        
        # Add separator line
        cv2.line(combined, (self.frame_width, 0), 
                (self.frame_width, self.frame_height), (255, 255, 255), 2)
        
        # Add debug info
        debug_text = f"State: {state_manager.get_state_text()} | FPS: {fps:.1f}"
        cv2.putText(combined, debug_text, (10, self.frame_height - 10), 
                   FONT, 0.5, COLOR_TEXT, 1)
        
        return combined