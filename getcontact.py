from threading import Lock, Thread
from queue import Queue
import argparse
import shutil
import time
import sys
import os

from getcontact.api import GetContactAPI
from getcontact.excel import XLS
from config import configs

queue = Queue(300)
lock_logger = Lock()
lock_excel = Lock()

G = '\033[38;2;0;255;0m'  # green
Y = '\033[38;2;255;255;0m'  # yellow
R = '\033[38;2;255;0;0m'  # red
W = '\033[38;2;255;255;255m'  # white


def logger(string, verbose):
    if verbose > 0:
        lock_logger.acquire()
        print(string)
        lock_logger.release()


class FillQueue:
    def __init__(self, file_path, separator, verbose, last_number):
        self.separator = separator
        self.verbose = verbose
        self.last_number = last_number
        self.number_parser = self.file_parser()
        self.phones_file = open(file_path, 'r')
        if self.last_number:
            self.skip_last_session_numbers()

        for phone_number in self.number_parser:
            queue.put(phone_number)

    def skip_last_session_numbers(self):
        current_number = self.number_parser.__next__()
        while self.last_number != current_number:
            current_number = self.number_parser.__next__()

    def file_parser(self):
        for line in self.phones_file:
            numbers = line.strip().split(self.separator)
            numbers_count = len(numbers)

            if numbers_count == 1:
                number = numbers[0]
                asterisks_count = number.count('*')

                if '*' in number:
                    variants = 10 ** asterisks_count
                    number = number.replace('*', '{}')
                    for i in range(variants):
                        yield number.format(*str(i).zfill(asterisks_count))
                    continue

                yield number

            elif numbers_count == 2:
                for number in range(int(numbers[0]), int(numbers[1]) + 1):
                    yield '+' + str(number)

            else:
                logger(f'{R}[PARSER]{W} \t {line.strip()}', self.verbose)


class Worker:
    def __init__(self, config, verbose, excel):
        self.config = config
        self.verbose = verbose
        self.excel = excel
        self.get_contact = GetContactAPI(config, verbose, lock_logger)

        while True:
            if queue.empty():
                break
            number = queue.get()
            try:
                self.try_get_info(number)
            except KeyError:
                pass

    def try_get_info(self, number):
        data = self.get_contact.get_information_by_phone(number)
        if data['tags']:
            lock_excel.acquire()
            self.excel.write(', '.join(data["tags"]), number)
            lock_excel.release()
            logger(f'{G}[FOUND]{W} \t {number}', self.verbose)
        else:
            logger(f'{Y}[EMPTY]{W} \t {number}', self.verbose)


def main():
    parser = argparse.ArgumentParser(f"{sys.argv[0]} [options] -f file")
    parser.add_argument('-f', '--file', help='File with number intervals')
    parser.add_argument('-s', '--sep', help='Separator for number intervals (space by default)', default=' ')
    parser.add_argument('-r', '--restore', help='Restores the previous session', action='store_true', default=False)
    parser.add_argument('-v', '--verbose',
                        help='0 = no output; 1 = everything except the captcha; 2 = everything (1 by default)',
                        type=int, default=1)
    arguments = parser.parse_args()

    separator = arguments.sep
    restore_session = arguments.restore
    verbose = arguments.verbose
    file_path = arguments.file
    if not file_path:
        parser.print_help()
        sys.exit(1)
    if not os.path.isfile(file_path):
        sys.stderr.write(f'File not found: {file_path}\n')
        sys.exit(1)
    if os.stat(file_path).st_size == 0:
        sys.stderr.write(f'File is empty: {file_path}\n')
        sys.exit(1)

    excel = XLS(restore_session)
    if restore_session:
        last_number = excel.get_last_number()
        if not last_number:
            sys.stderr.write(f'Xls file from the previous session is empty: {file_path}\n')
            sys.exit(1)
    else:
        last_number = ''

    captcha_path = 'captcha/'
    if not os.path.exists(captcha_path):
        os.mkdir(captcha_path)
    else:
        shutil.rmtree(captcha_path)
        os.mkdir(captcha_path)

    queue_filler = Thread(target=FillQueue, args=[file_path, separator, verbose, last_number])
    queue_filler.start()
    time.sleep(1)

    threads = []
    for config in configs:
        thread = Thread(target=Worker, args=[config, verbose, excel])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
