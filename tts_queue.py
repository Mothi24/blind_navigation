import queue
import pyttsx3

# Initialize TTS queue and engine
tts_queue = queue.Queue()
engine = pyttsx3.init()

def tts_worker():
    """Function to handle TTS queue and speak messages one at a time."""
    while True:
        message = tts_queue.get()
        if message is None:
            break  # Exit the thread if None is sent to the queue
        engine.say(message)
        engine.runAndWait()
        tts_queue.task_done()
