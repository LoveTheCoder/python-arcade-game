def convert_12_to_24(time_str):
    am_pm = time_str[-2:]
    hh = int(time_str[:2])
    mm = time_str[3:5]
    ss = time_str[6:8]
    if am_pm == "AM":
        if hh == 12:
            hh = 0
    else:  # PM
        if hh != 12:
            hh += 12
    return f"{hh:02d}:{mm}:{ss}"

if __name__ == "__main__":
    s = input().strip()
    print(convert_12_to_24(s))