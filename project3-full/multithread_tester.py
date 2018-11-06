import subprocess
import time
from threading import Thread
from colorama import Fore, Style
from util.confs2 import confs
import beep_test

import time
from datetime import timedelta
start_time = time.monotonic()




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
        print('Thread {} starting'.format(self.tname))
        global print_count
        conf_count = self.conf_start
        successes = 0
        fails = 0

        for conf in self.confs:
            print('{} : CALLING `game.py` for conf{}'.format(self.tname, conf_count))
            game_output = \
            subprocess.Popen(
            [
                'python',
                'game_1.py',
                conf[0],
                conf[1],
                conf[2],
                'conf{}'.format(conf_count)
            ],stdout=subprocess.PIPE).communicate()[0].decode('utf-8').rstrip()

            print(game_output)

            game_output = game_output[-1]

            if game_output == '1':
                beep_test.not_sound()
            else:
                beep_test.yes_sound()



            print('{} : conf{} DONE'.format(self.tname, conf_count))

            colorama_color = Fore.RED if game_output == '1' else Fore.GREEN
            if game_output == '1':
                fails += 1
            else:
                successes += 1

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
    print('Dividing the data for each thread')
    splitted_lists = split_list(confs, threads)
    print('DONE.')

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
    file = open('results.txt' , 'w', encoding='utf-8')
    for result in joined_results:
        game_output = result['result']
        colorama_color = Fore.GREEN if game_output == '0' else Fore.RED

        success_count += 1 if game_output == '0' else 0
        fail_count += 1 if game_output == '1' else 0

        result_str = ('[{}] {} [{}] [ RESULT: {} ] {} {}'
              .format(
                result['thread'],
                colorama_color,
                result['conf'],
                'CAT' if 0 else 'CATCHER',
                Style.RESET_ALL,
                load_bar(fail_count+success_count, len(joined_results))
                )
            )

        file.write('{}\n'.format(result_str))



        time.sleep(0.1)

    result_str = ('\n\n')
    result_str += ('{}\tSUCCESSES: {} ({:.2f}% success rate){}'.format(Fore.GREEN, success_count, (success_count/(success_count + fail_count)) * 100 ,Style.RESET_ALL))
    result_str += ('{}\tFAILS: {}{}'.format(Fore.RED, fail_count, Style.RESET_ALL))
    result_str += ('\tTOTAL: {}'.format(success_count + fail_count))

    print('{}\n'.format(result_str))
    file.write('{}\n'.format(result_str))
    file.close()

#thread_creator([conf_generator.confs()][0], 1)#Tests first only
#thread_creator(conf_generator.confs(), 4)#Tests all

thread_creator([confs[50]], 1)#Tests first only
#thread_creator(confs[0:len(confs)//5], 3)#Tests first 25% only
#thread_creator(confs, threads=2)#Tests all

beep_test.sound()

end_time = time.monotonic()

print('Duration {}'.format(
    timedelta(seconds=end_time - start_time)
))


#input('press enter to end')