from gpiozero import Button
from time import sleep

# GPIO Pin Definitions
GPIO_PINS = {
    "down": Button(2, pull_up=True),
    "left": Button(3, pull_up=True),
    "up": Button(4, pull_up=True),
    "right": Button(5, pull_up=True),
    "esc": Button(6, pull_up=True),
    "select": Button(7, pull_up=True),
    "action1": Button(8, pull_up=True),
    "action2": Button(9, pull_up=True),
    "action3": Button(10, pull_up=True),
}

def read_gpio_input():
    """Reads GPIO input states with improved debounce logic and returns a dictionary of button states."""
    initial_states = {key: pin.is_pressed for key, pin in GPIO_PINS.items()}
    sleep(0.05)  # Debounce delay (50ms)
    final_states = {key: pin.is_pressed for key, pin in GPIO_PINS.items()}

    # Only return states that remained consistent during the debounce period
    return {key: state for key, state in final_states.items() if state == initial_states[key]}

def cleanup_gpio():
    """Cleans up all GPIO resources."""
    for pin in GPIO_PINS.values():
        pin.close()