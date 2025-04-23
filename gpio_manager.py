from gpiozero import Button

# GPIO Pin Definitions
GPIO_PINS = {
    "down": Button(2, pull_down=True),
    "left": Button(3, pull_down=True),
    "up": Button(4, pull_down=True),
    "right": Button(5, pull_down=True),
    "esc": Button(6, pull_down=True),
    "select": Button(7, pull_down=True),
    "action1": Button(8, pull_down=True),
    "action2": Button(9, pull_down=True),
    "action3": Button(10, pull_down=True),
}

def read_gpio_input():
    """Reads GPIO input states and returns a dictionary of button states."""
    return {key: pin.is_pressed for key, pin in GPIO_PINS.items()}

def cleanup_gpio():
    """Cleans up all GPIO resources."""
    for pin in GPIO_PINS.values():
        pin.close()