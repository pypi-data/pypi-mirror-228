from threading import Thread
import argparse
from swmonkey.controller.replay import ReplayController

from swmonkey.monitor.monitor import monkey_monitor
from swmonkey.monkey_test.monkey_test import MonkeyTest
from swmonkey.heartbeat import send_heartbeat, finish_heartbeat
import os
from swmonkey.log.log import logger

DURATION = 10  # Duration in seconds
TIME_DIFF_SCALE = 0.1


def swmonkey():
    '''
    执行monkey测试
    '''
    parser = argparse.ArgumentParser(
        description='A tool for monkey test on Linux GUI')
    parser.add_argument('-d', '--duration', type=int,
                        default=DURATION, help='Duration in seconds')

    parser.add_argument('-r', '--replay', dest='replay', action='store_true',
                        default=None, help='Replay a previous monkey test')
    parser.add_argument('-p', '--path', type=str,
                        default=None, help='Path to the monkey test')
    parser.add_argument('--heartbeat', dest='heartbeat',
                        type=str, default=None, help='Heartbeat server address')
    args = parser.parse_args()

    duration = args.duration
    if duration is not None:
        os.environ['DURATION'] = str(duration)
    heartbeat = args.heartbeat
    if heartbeat is not None:
        os.environ['HEARTBEAT_URL'] = heartbeat
    replay = args.replay
    if replay is not None:
        os.environ['REPLAY'] = str(replay)

    path = args.path
    if path is not None:
        os.environ['LOG_PATH'] = path

    if os.getenv('HEARTBEAT_URL') is not None:
        print("HEARTBEAT_URL: ", os.getenv('HEARTBEAT_URL'))
        start_send_heartbeat()

    if os.getenv('REPLAY') is not None:
        replay_controller = ReplayController()
        replay_controller.run(actions_json_file_path=args.path)
    else:
        duration = int(os.getenv('DURATION'))
        assert duration > 0
        monkey_test = MonkeyTest(duration=duration)
        monkey_test.run()
    if os.getenv('HEARTBEAT_URL') is not None:
        finish_send_heartbeat()


def start_send_heartbeat():
    '''发送心跳信息，运行在独立进程中'''
    heartbeat_thread = Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()


def finish_send_heartbeat():
    finish_heartbeat()


if __name__ == '__main__':
    swmonkey()
