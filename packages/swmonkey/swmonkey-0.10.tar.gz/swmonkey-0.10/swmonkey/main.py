import threading
import argparse
from swmonkey.controller.replay import ReplayController

from swmonkey.monitor.monitor import monkey_monitor
from swmonkey.monkey_test.monkey_test import MonkeyTest

DURATION = 10  # Duration in seconds
TIME_DIFF_SCALE = 0.1


# Start monitor in a sperated thread
# monitor_thread = threading.Thread(target=monkey_monitor, daemon=True)
# monitor_thread.start()

def swmonkey():
    parser = argparse.ArgumentParser(
        description='A tool for monkey test on Linux GUI')
    parser.add_argument('-d', '--duration', type=int,
                        default=DURATION, help='Duration in seconds')

    parser.add_argument('-r', '--replay', dest='replay', action='store_true',
                        default=None, help='Replay a previous monkey test')
    parser.add_argument('-p', '--path', type=str,
                        default=None, help='Path to the monkey test')
    args = parser.parse_args()

    duration = args.duration

    if args.replay:
        replay_controller = ReplayController()
        replay_controller.run(actions_json_file_path=args.path)
    else:
        monkey_test = MonkeyTest(duration=duration)
        monkey_test.run()


if __name__ == '__main__':
    swmonkey()
