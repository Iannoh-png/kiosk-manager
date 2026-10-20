def clean_text(raw_input):
    return raw_input.strip().title()

def get_valid_number(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Invalid input - please enter a whole number.")

def get_menu_choice(prompt, min_value, max_value):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            number = int(value)
            if min_value <= number <= max_value:
                return number
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        else:
            print("Invalid input! Please enter digits only.")
            