import cv2
import config
from detection import detect_objects
from boundary import define_boundary, is_in_boundary
from alert import enqueue_alert, start_tts_worker, stop_tts_worker
import time

def main():
    # Load video
    cap = cv2.VideoCapture(config.VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Initialize frame counter, FPS calculation, and last alert time
    prev_time = 0
    frame_counter = 0
    last_alert_time = 0

    # Start the TTS worker thread
    start_tts_worker()

    # Define boundary based on the initial frame dimensions (assuming video size remains constant)
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read video.")
        return
    boundary_zone = define_boundary(frame)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1

        # Draw the boundary box on every frame
        x1, y1, x2, y2 = boundary_zone
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green boundary

        # Process 1 in every 3 frames only for detection
        if frame_counter % 3 == 0:
            # Detect objects in the frame
            detected_objects = detect_objects(frame)

            # Check each detected object and add alerts if necessary
            for obj_class, bbox in detected_objects:
                obj_type = "person" if obj_class == 0 else "vehicle" if obj_class in [2, 7] else "unknown"

                # Draw bounding box and label for each detected object
                obj_x1, obj_y1, obj_x2, obj_y2 = bbox
                cv2.rectangle(frame, (int(obj_x1), int(obj_y1)), (int(obj_x2), int(obj_y2)), (255, 0, 0), 2)  # Blue box for detected object
                cv2.putText(frame, obj_type, (int(obj_x1), int(obj_y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Alert only if the object is a person or vehicle, within boundary, and at least 3 seconds have passed
                current_time = time.time()
                if obj_type in ["person", "vehicle"] and is_in_boundary(bbox, boundary_zone):
                    if current_time - last_alert_time >= 3:
                        enqueue_alert(obj_type)
                        last_alert_time = current_time  # Update last alert time

        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)  # Yellow text for FPS

        # Display the frame in original resolution
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Stop the TTS worker thread
    stop_tts_worker()

if __name__ == "__main__":
    main()