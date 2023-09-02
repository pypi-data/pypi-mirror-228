#!/usr/bin/python3
# coding: utf-8
# -*- coding: utf-8 -*-

try:
    from urllib.parse import unquote
except ImportError:
    pass
except ImportError:
    from urlparse import unquote

try:
    import multiprocessing.shared_memory as shm
    from multiprocessing import shared_memory
except NameError:
    pass
except ImportError:
    pass


import requests
import argparse
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler
from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Thread
import sys
import os
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time


def main():
    def banner():
        banner_text = """
            ██████╗ ██╗███████╗██╗  ██╗ ██╗  ██╗██╗   ██╗██████╗ 
            ██╔══██╗██║██╔════╝██║ ██╔╝ ██║  ██║██║   ██║██╔══██╗
            ██████╔╝██║███████╗█████╔╝  ███████║██║   ██║██████╔╝
            ██╔══██╗██║╚════██║██╔═██╗  ██╔══██║██║   ██║██╔══██╗
            ██║  ██║██║███████║██║  ██╗ ██║  ██║╚██████╔╝██████╔╝
            ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 

            version : v.0.1
            Gathering a URL 
            instagram : @sabarish_h4ck3r / created by sabarish
        """
        print(banner_text)


    proxy = {'http': 'http://127.0.0.1:8080'}

    gen_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                 'Accept-Language':'en-US;',
                 'Accept-Encoding': 'gzip, deflate',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;',
                 'Connection':'close'}


    concurrent = 1000
    scheduler = BackgroundScheduler()
    batch_size = 100

    parser = argparse.ArgumentParser('fetching URLs to any domains 😈 ',description=banner())
    parser.add_argument('-f', '--file', help='specific url file contain the many url files')
    parser.add_argument('-e','--exclude', help= 'extensions to exclude')
    parser.add_argument('-d','--domain' , help = 'Domain name of the target [ex : google.com]')
    parser.add_argument('-t', '--thread', type=int, default=1000, help="to boost the request")
    parser.add_argument('-l','--level' ,  help = 'to set level for fetching URLs', default=1)
    parser.add_argument('-m', '--multiplex', help='specific to different proxy default local proxy')
    parser.add_argument('-v', '--verbose', help='to print the all request')
    args = parser.parse_args()

    try:
        if args.thread:
            executor = ThreadPoolExecutor(args.thread)
    except threading:
        pass
    except RuntimeError:
        pass

    def send_req(naa):
        try:
            r = requests.get(naa, headers=gen_headers)
            content = r.content
            response = unquote(content)
            print(response)
            
            #print(response)
        except ImportError:
            pass
        except TypeError:
            pass
        except ValueError:
            pass
        except HTTPError:
            pass
        except ConnectionError:
            pass
        except threading:
            pass
        except RuntimeError:
            pass
        except RuntimeWarning:
            pass
        except TimeoutError:
            pass
        except requests.ConnectTimeout:
            pass
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass	
        except KeyboardInterrupt:
            quit()
        except requests.exceptions.MissingSchema:
            pass
        except AttributeError:
            pass
        except OSError:
            pass 

    try:
        shm1 = shared_memory.SharedMemory(name=send_req, create=True, size=2084)
        shm1.buf
    except NameError:
         pass
    except TypeError:
        pass

    def domain():
        if args.domain:
            urls = ("https://web.archive.org/cdx/search/cdx?url=*.{}/*&output=txt&fl=original&collapse=urlkey&page=/".format(args.domain))
            executor.submit(send_req, urls)
        else:
            urls = ("https://web.archive.org/cdx/search/cdx?url={}/*&output=txt&fl=original&collapse=urlkey&page=/".format(args.domain))
            executor.submit(send_req, urls)
    
    
    def checkHttp(url):
        if("http://" not in url and "https://" not in url):
            return "https://%s" %url
        return url
    
    if args.domain:
        checkHttp(args.domain)
        domain()

    def file_url():
        with open(args.file, 'r') as f:
            lines = f.readlines()
            return lines

    def files():
        if args.file: # making a request
            try:
                list_url = file_url()
                for url in list_url:
                    urls = ("https://web.archive.org/cdx/search/cdx?url=*.{}/*&output=txt&fl=original&collapse=urlkey&page=/".format(url))
                    r = requests.get(urls, headers=gen_headers)
    #                executor.submit(send_req, url)
#                   executor.submit(send_req, url)
                    contents = r.content
                    responses = unquote(contents)
                    print(responses)
            except ImportError:
                pass
            except TypeError:
                pass
            except ValueError:
                pass
            except HTTPError:
                pass
            except ConnectionError:
                pass
            except threading:
                pass
            except RuntimeError:
                pass
            except RuntimeWarning:
                pass
            except TimeoutError:
                pass
            except requests.ConnectTimeout:
                pass
            except requests.ConnectionError:
                pass
            except requests.Timeout:
                pass	
            except KeyboardInterrupt:
                quit()
            except requests.exceptions.MissingSchema:
                pass
            except AttributeError:
                pass
            except OSError:
                pass
    
    if args.file:
        files()


    def milliseconds():
        time.sleep(1)
        t = time.time()
        t_ms = int(t * 1000)
        return t_ms

    def time1():
        t = milliseconds()
        w = milliseconds() - t
        time.sleep(1)
        print("\n Total execution time : {} ms \n".format((w)))
        sys.exit()

    time1 ()

    try:
        if args.verbose:
            pass
    except RuntimeError:
        pass

       

    def checkFilename(filename):
        while(True):
            if(len(filename) > 0):
                if(filename[0] == '\''): 
                    filename = filename[1:]
                if(filename[len(filename)-1] == '\''): 
                    filename = filename[:-1]
                if(os.path.exists(filename)):
                    return filename

#    if args.file:
#        try:
#            dam = checkFilename(args.file)
#            print("\n file are checking right now...")
#            list = file_url()
#            print(list)
#            for url_line in list:
#                unrule = f"https://web.archive.org/cdx/search/cdx?url=*.{url_line}/*&output=txt&fl=original&collapse=urlkey&page=/"
#                executor.submit(send_req, unrule)
#        except TypeError:
#            pass

    black_list = []
    if args.exclude:
        if "," in args.exclude:
            black_list = args.exclude.split(",")
            for i in range(len(black_list)):
                black_list[i] = "." + black_list[i]
        else:
            black_list.append("." + args.exclude)
    else: 
        black_list = []

    shm = shared_memory.SharedMemory(name=files, create=True, size=2048)
    shm.buf

    scheduler.start()

    try:
        executor = ThreadPoolExecutor(1000)
    except TypeError:
        pass
    except threading:
        pass
    except RuntimeError:
        pass

    try:
        for i in range(concurrent):
            t = Thread(target=files())
            t.daemon = True
            t.start()
    except TypeError:
        pass
    except ValueError:
            pass
    except HTTPError:
            pass
    except ConnectionError:
            pass
    except threading:
            pass
    except RuntimeError:
            pass
    except RuntimeWarning:
            pass
    except TimeoutError:
            pass
    except requests.ConnectTimeout:
            pass
    except requests.ConnectionError:
            pass
    except requests.Timeout:
            pass	
    except KeyboardInterrupt:
            quit()
    except requests.exceptions.MissingSchema:
            pass
    except AttributeError:
            pass
    except OSError:
            pass



if __name__ == "__main__":
    main()
