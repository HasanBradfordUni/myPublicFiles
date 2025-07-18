# A simple time calculator that can add and subtract time in minutes, seconds and frames (30 frames in a second).
def time_calculator(time1, time2, operation):
    """
    Calculate the result of adding or subtracting two times.

    :param time1: A tuple (hours, minutes, seconds, frames)
    :param time2: A tuple (hours, minutes, seconds, frames)
    :param operation: 'add' or 'subtract'
    :return: A tuple (hours, minutes, seconds, frames) representing the result
    """
    h1, m1, s1, f1 = time1
    h2, m2, s2, f2 = time2

    # Convert everything to frames
    total_frames1 = h1 * 3600 * 30 + m1 * 60 * 30 + s1 * 30 + f1
    total_frames2 = h2 * 3600 * 30 + m2 * 60 * 30 + s2 * 30 + f2

    if operation == 'add':
        total_frames = total_frames1 + total_frames2
    elif operation == 'subtract':
        total_frames = total_frames1 - total_frames2
    else:
        raise ValueError("Operation must be 'add' or 'subtract'")

    # Convert back to hours, minutes, seconds and frames
    hours = total_frames // (3600 * 30)
    total_frames %= (3600 * 30)
    minutes = total_frames // (60 * 30)
    total_frames %= (60 * 30)
    seconds = total_frames // 30
    frames = total_frames % 30

    print(seconds, frames)

    if frames >= 15:
        seconds += 1
    if seconds >= 60:
        minutes += seconds // 60
        seconds %= 60
    if minutes >= 60:
        hours += minutes // 60
        minutes %= 60

    return f"Time is {hours} hours, {minutes} minutes and {seconds} seconds"

# User Interface
print("Welcome to the Time Calculator!")
print("You can add or subtract two times in the format (hours, minutes, seconds, frames).")

operation_menu = """
1. Add Time
2. Subtract Time
3. Exit
"""
while True:
    print(operation_menu)
    choice = input("Choose an operation (1-3): ")
    if choice == '1':
        print("You chose to add time.")
        time1_hours = int(input("Enter the first time's hours: "))
        time1_minutes = int(input("Enter the first time's minutes: "))
        time1_seconds = int(input("Enter the first time's seconds: "))
        time1_frames = int(input("Enter the first time's frames: "))
        time2_hours = int(input("Enter the second time's hours: "))
        time2_minutes = int(input("Enter the second time's minutes: "))
        time2_seconds = int(input("Enter the second time's seconds: "))
        time2_frames = int(input("Enter the second time's frames: "))
        time1 = tuple([time1_hours, time1_minutes, time1_seconds, time1_frames])
        time2 = tuple([time2_hours, time2_minutes, time2_seconds, time2_frames])
        result = time_calculator(time1, time2, 'add')
        print(f"Result of addition: {result}")
    elif choice == '2':
        time1 = tuple(map(int, input("Enter the first time (hours, minutes, seconds, frames): ").split(',')))
        time2 = tuple(map(int, input("Enter the second time (hours, minutes, seconds, frames): ").split(',')))
        result = time_calculator(time1, time2, 'subtract')
        print(f"Result of subtraction: {result}")
    elif choice == '3':
        print("Exiting the Time Calculator. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")