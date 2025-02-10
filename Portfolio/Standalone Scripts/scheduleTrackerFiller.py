import re
import time
import pyperclip
import pyautogui

def read_schedule(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def count_items_per_day(text):
    week_day_counts = {}
    current_week = ""
    current_day = ""
    
    for line in text.split("\n"):
        line = line.strip()
        
        # Determine the week
        if line.startswith("Week"):
            current_week = line.split(" ")[1]
        
        # Determine the day
        elif line.endswith(":") and not line.startswith("Week"):
            current_day = line.replace(":", "").strip()
        
        # Count items for the current day
        else:
            if current_week and current_day:
                key = f"Week {current_week} {current_day}"
                if key not in week_day_counts:
                    week_day_counts[key] = 0
                if line:
                    week_day_counts[key] += 1
                #print(f"Day: {key}, Count: {week_day_counts[key]}")
    
    return week_day_counts

def copy_to_clipboard_with_delay(day_counts):
    weeks = day_counts
    end_days = ["Week 1 Sunday", "Week 2 Saturday", "Week 3 Saturday", "Week 4 Saturday"]
    for day, count in weeks.items():
        pyperclip.copy(str(count))
        pyautogui.hotkey('ctrl', 'v')
        print(f"Copied {count} for {day}")
        pyautogui.press('down')
        if day in end_days:
            print("End of week")
            time.sleep(5)
            print("Moving on to new week")
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('down')

if __name__ == "__main__":
    file_path = 'WEEKLYSCHEDULES.TXT'
    print("Reading schedule...")
    time.sleep(2)
    content = read_schedule(file_path)
    day_counts = count_items_per_day(content)
    copy_to_clipboard_with_delay(day_counts)