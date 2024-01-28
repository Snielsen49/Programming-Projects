import sys
import time

def animate_text(animation_chars, duration):
    # Calculate the end time for the animation
    end_time = time.time() + duration
    
    # Loop until the current time exceeds the end time
    while time.time() < end_time:
        # Iterate through animation characters
        for char in animation_chars:
            # Use \b (backspace) to create an animation effect
            sys.stdout.write('\b' + char)
            sys.stdout.flush()  # Flush the output to make it immediately visible
            time.sleep(0.2)  # Introduce a delay between each animation frame

# List of animation characters
animation_characters = ["|", "/", "-", "\\"]
# Duration of the animation in seconds
animation_duration = 5  

# Print the initial text
print("Hello World!")

# Call the animate_text function to display the animated characters
animate_text(animation_characters, animation_duration)
