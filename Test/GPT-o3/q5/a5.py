def convert_to_military_time(time_str):
    period = time_str[-2:]
    hh, mm, ss = time_str[:-2].split(':')
    hh = int(hh)
    
    if period == 'AM':
        if hh == 12:
            hh = 0
    else:  # PM
        if hh != 12:
            hh += 12
            
    return f"{hh:02d}:{mm}:{ss}"

if __name__ == '__main__':
    time_str = input("Enter time in 12-hour format (hh:mm:ssAM/PM): ")
    print("Military time:", convert_to_military_time(time_str))