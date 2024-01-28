import sys
import time

def animate_text(animation_chars, duration):
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for char in animation_chars:
            sys.stdout.write('\b' + char)
            sys.stdout.flush()
            time.sleep(0.2)


animation_characters = ["|", "/", "-", "\\"]
animation_duration = 5  # in seconds

print("Hello World!"  )
animate_text(animation_characters, animation_duration)