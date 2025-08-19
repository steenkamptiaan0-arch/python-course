import time
import random
import threading


def slow_print(text, delay=0.03):
    """Print text slowly for fun effect"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def stopwatch():
    slow_print("\n⏱️ Stopwatch Mode ⏱️")
    slow_print("Press Enter to start the stopwatch.")
    input()
    start_time = time.time()
    stop_flag = [False]

    def wait_for_enter():
        input()
        stop_flag[0] = True

    threading.Thread(target=wait_for_enter).start()

    while not stop_flag[0]:
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        hours, mins = divmod(mins, 60)
        print(f"\rTime elapsed: {hours:02d}:{mins:02d}:{secs:02d}", end="")
        time.sleep(1)

    elapsed = time.time() - start_time
    mins, secs = divmod(int(elapsed), 60)
    hours, mins = divmod(mins, 60)
    slow_print(f"\n🛑 Stopwatch stopped! Total time: {hours:02d}:{mins:02d}:{secs:02d}")


def countdown_timer():
    slow_print("\n⏳ Countdown Timer Mode ⏳")
    total_seconds = int(input("Enter countdown time in seconds: "))
    
    try:
        while total_seconds > 0:
            mins, secs = divmod(total_seconds, 60)
            hours, mins = divmod(mins, 60)
            print(f"\rTime remaining: {hours:02d}:{mins:02d}:{secs:02d}", end="")
            time.sleep(1)
            total_seconds -= 1
        slow_print("\n🎉 Time's up! Ding ding! 🔔")
        slow_print(random.choice([
            "Great job! You made it! 🎊",
            "Boom! Countdown finished! 💥",
            "Timer complete! Well done! ✅"
        ]))
    except KeyboardInterrupt:
        slow_print("\n🛑 Countdown stopped early!")


# Main loop
slow_print("🎉 Welcome to the Fun Timer App! 🎉")
time.sleep(0.5)

while True:
    slow_print("\nChoose a mode:")
    slow_print("1. Stopwatch ⏱️\n2. Countdown Timer ⏳")
    
    try:
        choice = int(input("Select an option (1-2): "))
    except:
        slow_print("❌ Invalid input, please enter 1 or 2.")
        continue

    if choice == 1:
        stopwatch()
    elif choice == 2:
        countdown_timer()
    else:
        slow_print("❌ Invalid choice! Try again.")
        continue

    # Continue?
    cont = input("\nDo you want to use the timer again? (yes/no): ").strip().lower()
    if cont not in ["yes", "y"]:
        slow_print("\n👋 Thanks for using the Fun Timer App! Bye! 🎉")
        break