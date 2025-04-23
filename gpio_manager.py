from gpiozero import Button

# GPIO Pin Definitions
GPIO_PINS = {
    "down": Button(2, pull_up=False),
    "left": Button(3, pull_up=False),
    "up": Button(4, pull_up=False),
    "right": Button(5, pull_up=False),
    "esc": Button(6, pull_up=False),
    "select": Button(7, pull_up=False),
    "action1": Button(8, pull_up=False),
    "action2": Button(9, pull_up=False),
    "action3": Button(10, pull_up=False),
}

def read_gpio_input():
    """Reads GPIO input states and returns a dictionary of button states."""
    return {key: pin.is_pressed for key, pin in GPIO_PINS.items()}

def cleanup_gpio():
    """Cleans up all GPIO resources."""
    for pin in GPIO_PINS.values():
        pin.close()