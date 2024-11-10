import os
import sys

if len(sys.argv) < 2:
    input('Incorrect request')
    sys.exit(1)

command = sys.argv[1]
pkg = sys.argv[2]

if command == 'getgit':
    print(f'You\'re installing {pkg} with XLPM GetGit')
    ans = input('Confirm action [Y/N] ')
    if ans in ['y', 'Y']:
        os.system(f'sudo xlpm getgit {pkg}')
    else:
        sys.exit(0)
    input('Press ENTER to exit...')