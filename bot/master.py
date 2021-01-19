#!/usr/bin/python
import dom_parser
import threading

master_dict = {'http://test.ccds.club':dom_parser.whmcs}

def purchase ():
     domain = raw_input("enter website name: ")
     run_wrapper(master_dict[domain])


def run_wrapper(self):
    prod_info = {}
    for item in self.get_info():
        res = raw_input('enter ' + item + ": ")
        prod_info = dict(prod_info, **{item:res})
    thread_num = raw_input("enter the amount of threads you would like to run: ")
    threads = []
    for x in range(int(thread_num)):
        threads += [threading.Thread(target=self.buy_product, args=(prod_info,))]
        threads[-1].start()
    isRunning = True
    
    while (isRunning):
        isRunning = False
        for thread in threads:
            if (thread.is_alive()):
                isRunning = True
