
import os
import time
import humanfriendly

import util

MAX_FILE_SIZE = 100000000

while True:
    _text = input('Enter file text > ')
    filename = input('Enter save file name > ')
    _text += '\n' if util.query_yes_no('Use new lines?') else ''
    while True:
        try:
            _in = input('Enter File Size > ')

            b = util.strToBytes(_in)

            if b <= 0:
                raise ValueError('Size must be bigger than 0.')
            elif b > MAX_FILE_SIZE:
                raise ValueError(f'Size must be less than than {util.bytesToStr(MAX_FILE_SIZE)}.')
            
            break
        except ValueError as e:
            # print(f'Enter a valid size. {_in} is not a valid size.')
            print(e)

    # correct = input(f'{util.bytesToStr(MAX_FILE_SIZE)} of\n{_text}\n. Is this right?')
    correct = util.query_yes_no(f'\n{util.bytesToStr(b)} of\n{_text}\nIs this right?')
    if correct:
        break

t1 = time.time()

print('Compiling...')

sizeOfText = util.utf8len(_text)
final = ''.join([_text for i in range(b // sizeOfText)])

print('Saving...')

with open(filename, 'w') as f:
    f.write(final)

t2 = time.time()
t = t2 - t1

filesize = os.path.getsize(filename)

print(f'Done in {humanfriendly.format_timespan(t)}.')
print(f'Actual file size: {util.bytesToStr(filesize)}.')