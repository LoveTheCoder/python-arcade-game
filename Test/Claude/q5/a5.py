def time_conversion(s):
    # Extract components
    hours = int(s[0:2])
    minutes = s[3:5]
    seconds = s[6:8]
    period = s[8:10]
    
    # Convert hours
    if period == "AM":
        if hours == 12:
            hours = "00"
        else:
            hours = str(hours).zfill(2)
    else:  # PM
        if hours != 12:
            hours = str(hours + 12)
        else:
            hours = str(hours)
    
    # Return formatted string
    return f"{hours}:{minutes}:{seconds}"

def main():
    test_times = [
        "12:01:00AM",  # Should return "00:01:00"
        "12:01:00PM",  # Should return "12:01:00"
        "07:05:45PM",  # Should return "19:05:45"
        "11:59:59PM",  # Should return "23:59:59"
        "12:00:00AM",  # Should return "00:00:00"
    ]
    
    for time in test_times:
        print(f"Input: {time}")
        print(f"Output: {time_conversion(time)}\n")

if __name__ == "__main__":
    main()