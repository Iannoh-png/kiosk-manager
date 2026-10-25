import os


def load_kiosk_details(filename="kiosk.txt"):
    if not os.path.exists(filename):
        return None, None

    file = open(filename, "r")
    lines = file.read().splitlines()
    file.close()

    if len(lines) >= 2:
        return lines[0], lines[1]
    return None, None


def save_kiosk_details(kiosk_name, owner_name, filename="kiosk.txt"):
    file = open(filename, "w")
    file.write(f"{kiosk_name}\n{owner_name}\n")
    file.close()