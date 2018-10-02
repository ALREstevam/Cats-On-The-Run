import subprocess
from colorama import Fore, Back, Style
from threading import Thread
from confs import confs
import time

print_count = 0

def split_list(alist, wanted_parts = 1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]

class CatcherTester(Thread):
    def __init__(self, tid, tname, confs, conf_start):
        Thread.__init__(self)
        self.tid = tid
        self.tname = tname
        self.results = []
        self.confs = confs
        self.conf_start = conf_start



    def run(self):
        global print_count
        conf_count = self.conf_start
        successes = 0
        fails = 0

        for conf in self.confs:
            game_output = \
            subprocess.Popen(
            [
                'python',
                'game.py',
                conf[0],
                conf[1],
                conf[2],
                'conf{}'.format(conf_count)
            ],stdout=subprocess.PIPE).communicate()[0].decode('utf-8').rstrip()

            colorama_color = Fore.GREEN if game_output == '1' else Fore.RED
            if game_output == '1':
                successes += 1
            else:
                fails += 1

            print('[{}] {} [conf{:03}] [  RESULT: {} ] {} [...] [{}]'.format(self.tname ,colorama_color, conf_count, game_output, Style.RESET_ALL, print_count))
            print_count += 1
            self.results.append({'result': game_output, 'conf': 'conf{:03}'.format(conf_count),'conf_num':conf_count , 'thread' : self.tname})
            conf_count += 1

def load_bar(done, total):
    done_of = '{}/{}'.format(done, total)
    done_percent = (done/total) * 100
    done_percent_txt = '{:.2f}%'.format(done_percent)
    bar = '[{:<50s}]'.format('█' * int(done_percent//2))
    return bar + ' ' + done_of + ' ' + done_percent_txt

def thread_creator(confs, threads):
    splitted_lists = split_list(confs, threads)
    created_threads = []
    t_count = 0
    arr_size_acum = 0

    for sub_list in splitted_lists:
        thread = CatcherTester(t_count, 'Thread#{:03}'.format(t_count), sub_list, arr_size_acum)
        arr_size_acum += len(sub_list)
        t_count += 1
        created_threads.append(thread)
        thread.start()

    joined_results = []
    for t in created_threads:
        t.join()
        print('THREAD `{}` ENDED'.format(t.tname))
        joined_results.extend(t.results)

    joined_results = sorted(joined_results, key=lambda elem: elem['conf_num'], reverse=False)

    print('\n\n' + '=' * 100 + '\n\n')

    success_count = 0
    fail_count = 0
    for result in joined_results:
        game_output = result['result']
        colorama_color = Fore.GREEN if game_output == '1' else Fore.RED

        success_count += 1 if game_output == '1' else 0
        fail_count += 1 if game_output == '0' else 0

        print('[{}] {} [{}] [ RESULT: {} ] {} {}'
              .format(
                result['thread'],
                colorama_color,
                result['conf'],
                result['result'],
                Style.RESET_ALL,
                load_bar(fail_count+success_count, len(joined_results))
                )
            )
        time.sleep(0.1)

    print('\n\n')
    print('{}\tSUCCESSES: {}{}'.format(Fore.GREEN, success_count, Style.RESET_ALL))
    print('{}\tFAILS: {}{}'.format(Fore.RED, fail_count, Style.RESET_ALL))
    print('\tTOTAL: {}'.format(success_count + fail_count))

#thread_creator([confs[27]], 1)#Tests first only
#thread_creator(confs[0:len(confs)//4], 2)#Tests first 25% only
thread_creator(confs, 2)#Tests all