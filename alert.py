import queue
from tts_queue import tts_queue, tts_worker
import threading

# Start the TTS worker thread
tts_thread = None

def start_tts_worker():
    global tts_thread
    tts_thread = threading.Thread(target=tts_worker, daemon=True)
    tts_thread.start()

def stop_tts_worker():
    tts_queue.put(None)  # Signal the TTS thread to exit
    tts_thread.join()

def enqueue_alert(obj_type):
    """Add message to the TTS queue based on object type."""
    message = f"{obj_type} in front"
    tts_queue.put(message)
