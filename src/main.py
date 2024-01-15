import sys, os
import threading

from utils import *

# Default values
WATCH_INTERVAL = 2.0
LINE_WRAPPING = True
NO_TITLE = False
USAGE = "Usage: pywatch [{-n | --interval} <time_seconds>] [{-h | --help}] [{-w | --no-wrap}] [{-t | --no-title}] <cmd> [args]\n"

# Look for WATCH_INTERVAL in environment
if "WATCH_INTERVAL" in os.environ:
    if is_float(os.environ["WATCH_INTERVAL"]):
        WATCH_INTERVAL = float(os.environ["WATCH_INTERVAL"])

# Process command line arguments
args = sys.argv[1:]
try:
    while args:
        option = args.pop(0)
        if option.startswith("-"):
            if option in ("-n", "--interval"):
                if not args:
                    raise Exception(f"The {option} flag must be followed by a floating-point number.")
                else:
                    option_value = args.pop(0)
                    if is_float(option_value):
                        WATCH_INTERVAL = float(option_value)
                    else:
                        raise Exception(f"Invalid time interval provided.")
            elif option in ("-t", "--no-title"):
                NO_TITLE = True
            elif option in ("-w", "--no-wrap"):
                LINE_WRAPPING = False
            elif option in ("-h", "--help"):
                print(USAGE)
                os._exit(0)
            else:
                raise Exception(f"{option} is not a recognized option.")
        else:
            args.insert(0, option)
            break

    if not args:
        raise Exception(f"Please supply a command to be run.")

except Exception as e:
    print(e, "\n")
    print(USAGE)
    os._exit(1)

# Start a session with the given refresh interval
s = Session(args, WATCH_INTERVAL, no_title=NO_TITLE, wrap=LINE_WRAPPING)

# Start a new thread to refresh command output
t = threading.Thread(target=refresh_cmd, args=(s,), daemon=True)
t.start()

# The main thread will monitor key presses for the active session
try:
    while True:
        key = s.get_key_press()
        if key == ord('q'): # quit
            raise Exception()
        elif key == ord('j'):
            s.scroll(1)
        elif key == ord('k'):
            s.scroll(-1)
        
except BaseException:
    # A catchall that includes KeyboardInterrupt
    s.terminate()
