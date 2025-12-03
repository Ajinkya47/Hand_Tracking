"""
State management for SAFE/WARNING/DANGER classification
"""

from config import *
from enum import Enum

class State(Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    DANGER = "DANGER"

class StateManager:
    def __init__(self):
        self.current_state = State.SAFE
        self.state_counter = 0
        self.state_persistence = 5  # Frames to persist state
        
    def classify_state(self, distance):
        """Classify interaction state based on distance"""
        if distance > SAFE_THRESHOLD:
            new_state = State.SAFE
        # FIX: Ensure WARNING state covers the gap between SAFE and DANGER
        # DANGER state now only triggers when distance <= DANGER_THRESHOLD (30px)
        elif distance > DANGER_THRESHOLD:
            new_state = State.WARNING
        else:
            new_state = State.DANGER
        
        # Add some hysteresis to prevent flickering
        if new_state != self.current_state:
            self.state_counter += 1
            if self.state_counter >= self.state_persistence:
                self.current_state = new_state
                self.state_counter = 0
        else:
            self.state_counter = 0
        
        return self.current_state

    def get_state_color(self):
        """Get color corresponding to current state"""
        if self.current_state == State.SAFE:
            return COLOR_SAFE
        elif self.current_state == State.WARNING:
            return COLOR_WARNING
        else:  # DANGER
            return COLOR_DANGER
    
    def get_state_text(self):
        """Get text representation of current state"""
        return self.current_state.value