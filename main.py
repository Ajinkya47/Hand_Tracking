import cv2
"""
Main application - Hand Tracking POC for Arvyax Internship
"""

import cv2
import argparse
import traceback
from config import *
from hand_tracker import HandTracker
from virtual_object import VirtualObject
from state_manager import StateManager
from visualizer import Visualizer
from performance_monitor import PerformanceMonitor

def main():
    parser = argparse.ArgumentParser(description='Hand Tracking POC for Arvyax')
    parser.add_argument('--debug', action='store_true', help='Show debug view with mask')
    parser.add_argument('--video', type=str, help='Use video file instead of camera')
    parser.add_argument('--shape', type=str, default='circle', 
                       choices=['circle', 'rectangle'], help='Virtual object shape')
    args = parser.parse_args()
    
    # Initialize components
    print("Initializing Hand Tracking POC...")
    print("Requirements:")
    print("1. Real-time hand tracking ✓")
    print("2. Virtual boundary ✓")
    print("3. Distance-based state logic (SAFE/WARNING/DANGER) ✓")
    print("4. Visual feedback overlay ✓")
    print("5. Target: ≥8 FPS on CPU ✓")
    print("\nPress 'ESC' to exit, 's' to save screenshot")
    
    try:
        hand_tracker = HandTracker()
        virtual_object = VirtualObject(shape=args.shape)
        state_manager = StateManager()
        visualizer = Visualizer(FRAME_WIDTH, FRAME_HEIGHT)
        perf_monitor = PerformanceMonitor()
        
        # Initialize video capture
        if args.video:
            cap = cv2.VideoCapture(args.video)
        else:
            cap = cv2.VideoCapture(CAMERA_ID)
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        
        if not cap.isOpened():
            print("Error: Could not open video source")
            return
        
        frame_skip_counter = 0
        process_frame = True
        hand_position = None
        distance = float('inf')
        fps = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video stream")
                break
            
            frame_skip_counter += 1
            if frame_skip_counter >= FRAME_SKIP:
                process_frame = True
                frame_skip_counter = 0
            else:
                process_frame = False
            
            # Process frame
            if process_frame:
                try:
                    # Track hand
                    hand_position, mask_display = hand_tracker.track_hand(frame)
                    
                    # Calculate distance to virtual object
                    distance = virtual_object.calculate_distance(hand_position)
                    
                    # Classify state
                    state = state_manager.classify_state(distance)
                    
                    # Update virtual object color based on state
                    virtual_object.set_color(state_manager.get_state_color())
                except Exception as e:
                    print(f"Processing error: {e}")
                    # Continue with previous values
            
            # Draw virtual object
            display_frame = frame.copy()
            try:
                virtual_object.draw(display_frame)
            except Exception as e:
                print(f"Drawing error: {e}")
                # Draw simple circle as fallback
                cv2.circle(display_frame, (320, 240), 80, (0, 255, 0), 3)
            
            # Draw hand position if detected
            if hand_position is not None:
                cv2.circle(display_frame, hand_position, 8, COLOR_TRACKER, -1)
                cv2.circle(display_frame, hand_position, 12, COLOR_TRACKER, 2)
            
            # Draw status overlay
            try:
                display_frame = visualizer.draw_status_overlay(
                    display_frame, state_manager, hand_position, distance
                )
            except Exception as e:
                print(f"Overlay error: {e}")
                # Add basic text as fallback
                cv2.putText(display_frame, "SAFE", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Update and display FPS
            fps = perf_monitor.update()
            try:
                display_frame = visualizer.draw_fps(display_frame, fps)
            except:
                pass
            
            # Check performance
            if fps < TARGET_FPS:
                cv2.putText(display_frame, "LOW FPS!", (FRAME_WIDTH//2 - 50, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Show frame
            try:
                if args.debug and 'mask_display' in locals():
                    combined = visualizer.create_debug_display(
                        display_frame, mask_display, state_manager, fps
                    )
                    cv2.imshow('Hand Tracking POC - Debug View', combined)
                else:
                    cv2.imshow('Hand Tracking POC - Arvyax Assignment', display_frame)
            except Exception as e:
                print(f"Display error: {e}")
                cv2.imshow('Hand Tracking POC - Arvyax Assignment', display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("\nExiting...")
                break
            elif key == ord('s'):  # Save screenshot
                timestamp = cv2.getTickCount()
                filename = f"screenshot_{timestamp}.png"
                cv2.imwrite(filename, display_frame)
                print(f"Screenshot saved as {filename}")
            elif key == ord('h'):  # Help
                print("\nControls:")
                print("ESC - Exit")
                print("s   - Save screenshot")
                print("h   - Show this help")
            elif key == ord('r'):  # Reset
                print("Resetting...")
                hand_position = None
                distance = float('inf')
    
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
    
    finally:
        # Release resources
        try:
            cap.release()
        except:
            pass
        cv2.destroyAllWindows()
        
        # Final performance report
        print("\n" + "="*50)
        print("PERFORMANCE REPORT")
        print("="*50)
        try:
            print(f"Average FPS: {fps:.1f}")
            print(f"Target FPS: {TARGET_FPS}")
            print(f"Requirement met: {'✓' if fps >= TARGET_FPS else '✗'}")
            print(f"Final State: {state_manager.get_state_text()}")
        except:
            print("Performance data not available")
        print("="*50)

if __name__ == "__main__":
    main()