# Made by VladosNX (github.com/vladosnx)
import sys
import zipfile
import json
import os
import shutil
import subprocess

version = '1.3.1' # Saving version to show it later

commandsToLock = [
    'getgit',
    'installf',
    'install',
    'remove'
]

lockfilePath = '/tmp/xlpm.lock'

if not os.path.exists('/etc/xlpm/packages'):
    os.mkdir('/etc/xlpm')
    os.mkdir('/etc/xlpm/packages')

# Class with messages
class Output():
    def __init__(self):
        self.p = print
    def info(self, text):
        self.p('\x1b[44;37mINFO \x1b[0m ' + text)
    def error(self, text): 
        self.p('\x1b[41;37mERROR\x1b[0m ' + text)
    def warn(self, text):
        self.p('\x1b[43;37mWARN \x1b[0m ' + text)
    def done(self, text):
        self.p('\x1b[42;37mDONE \x1b[0m ' + text)
    def debug(self, text):
        self.p('\x1b[46;37mDEBUG\x1b[0m ' + text)

out = Output()
print = None

class Terminates():
#     def code_1(self):
#         sys.exit(1)
#         if os.path.exists(lockfilePath):
#             os.remove(lockfilePath)
#     def code_0(self):
#         sys.exit(0)
#         if os.path.exists(lockfilePath):
#             os.remove(lockfilePath)
    def code(self, returnCode):
        if os.path.exists(lockfilePath) and lockedHere:
            os.remove(lockfilePath)
            # out.info('Lock file is removed!')
        sys.exit(returnCode)
    
terminate = Terminates()

command = None
pkg = None
getgitHere = False

args = sys.argv
args.pop(0)

if len(args) == 0:
    out.info('Showing help page')
    out.info('version - show XLPM installed version')
    out.info('getgit - install package from GitHub')
    out.info('installf - install package from file')
    out.info('remove - remove package')
    out.info('info - get information about package from file')
    out.info('pkginfo - packages list')
    terminate.code(0)

lockedHere = False
lockRequired = False
skipNext = False
for arg in args:
    if skipNext:
        skipNext = False
        continue
    if arg == 'getgit':
        if len(args) < 2:
            out.error('No repository selected')
            terminate.code(1)
        skipNext = True
        command = 'getgit'
        pkg = args[args.index(arg) + 1]
        lockRequired = True
    elif arg == 'installf':
        if len(args) < 2:
            out.error('No package selected')
            terminate
        skipNext = True
        command = 'installf'
        pkg = args[args.index(arg) + 1]
        lockRequired = True
    elif arg == 'remove':
        if len(args) < 2:
            out.error('No package selected')
            terminate.code(1)
        skipNext = True
        command = 'remove'
        pkg = args[args.index(arg) + 1]
        lockRequired = True
    elif arg == 'info':
        if len(args) < 2:
            out.error('No package selected')
            terminate.code(1)
        skipNext = True
        command = 'info'
        pkg = args[args.index(arg) + 1]
        lockRequired = True
    elif arg == 'pkginfo':
        command = 'pkginfo'
    elif arg == 'build':
        command = 'build'
    elif arg == 'version':
        command = 'version'

if lockRequired:
    if os.path.exists(lockfilePath):
        out.error('XLPM is locked. Maybe, XLPM is already running')
        terminate.code(1)
    open(lockfilePath, mode='w+')
    lockedHere = True

# Running commands

if os.getuid() != 0 and command in ['getgit', 'install', 'installf', 'remove'] == False:
    out.error(f"You must be root (you are {os.getlogin()})")
    out.error(f"Try to run: sudo xlpm {command} {pkg if pkg != None else ''}")
    terminate.code(1)

if not os.path.exists('/etc/xlpm/packages'):
    os.mkdir('/etc/xlpm/packages')


def installf():
    iff = '/tmp/xlpm-installf'
    if not os.path.exists(pkg):
        out.error(f'File not found: {pkg}')
        exit(1)
    os.mkdir(iff)
    pkgFile = zipfile.ZipFile(pkg)
    pkgFile.extractall(iff)
    configPath = f"{iff}/{subprocess.getoutput('ls /tmp/xlpm-installf')}/xlp_config.json"
    if not os.path.exists(configPath):
        out.error(f"Package doesn't have config file")
        shutil.rmtree(iff)
        terminate.code(1)
    configFile = open(configPath)
    config = json.loads(configFile.read())
    configFile.close()

    pkgName = config['name']
    pkgVersion = config['version']
    pkgExec = config['exec']
    execList = pkgExec.split('|')
    pkgFolders = config['folders']
    out.info(f'{pkgName} V{pkgVersion}')
    os.remove(configPath)
    packageFilesPath = iff + '/' + subprocess.getoutput(f'ls {iff}')
    os.chdir(packageFilesPath)
    for folder in pkgFolders: 
        folderLink = pkgFolders[folder]
        pkgInfoFiles = ''

        os.chdir(packageFilesPath + f'/{folder}')
        fileList = subprocess.getoutput(f'ls {packageFilesPath}/{folder}').split('\n')
        for f in fileList:
            localPath = f'{folder}/{f}'
            realPath = f'{folderLink}/{f}'
            os.system(f'cp -r {f} {folderLink}')
            if localPath in execList:
                os.system(f'chmod +x {realPath}')
                out.debug(f'{realPath} from {localPath} is now executable')
            pkgInfoFiles = pkgInfoFiles + realPath + '\n'
        out.debug(f'Copied files from {folder} to {folderLink}')

    pkgInfoFile = open(f'/etc/xlpm/packages/{pkgName}', 'w+')
    pkgInfoFile.write(pkgInfoFiles)
    pkgInfoFile.close()
    # os.system('echo -n "$(ls)" > /etc/xlpm/packages/' + pkgName)
    # for file in pkgExec.split('|'):
    #    os.system('chmod +x /usr/bin/' + file)
    os.chdir('/')
    shutil.rmtree(iff)
    out.done(f'Successfully installed {pkgName} V{pkgVersion}')
    if getgitHere == True:
        os.system('rm -rf /tmp/getgit')
    terminate.code(0)

if command == 'getgit':
    if len(pkg.split('/')) != 2:
        out.error('Incorrect repository format')
        terminate.code(1)
    if os.path.exists('/tmp/getgit'):
        out.error('GetGit cannot be executed, because the temp folder is')
        out.error('already exists. Maybe it means that the same command of XLPM')
        out.error('is already running.')
        out.error('If you are sure that this is bug, run this command:')
        out.error('sudo xlpm clearcache')
        terminate.code(1)
    out.info(f'Getting {pkg.split("/")[1]}')
    os.mkdir('/tmp/getgit')
    os.chdir('/tmp/getgit')
    os.system(f'git clone https://github.com/{pkg}')
    if os.path.exists(pkg.split('/')[1]) == False:
        out.error('Repo wasn\'t cloned')
        out.error('GetGit failed')
        terminate.code(1)
    iff = '/tmp/xlpm-getgit'
    folder = pkg.split('/')[1]
    os.chdir(folder)
    pkg = 'app.xlp'
    getgitHere = True
    installf()
    os.system('rm -rf /tmp/getgit')
    terminate.code(0)
if command == 'installf':
    installf()
    terminate.code(0)

if command == 'remove':
    if not os.path.exists('/etc/xlpm/packages/' + pkg):
        out.error('No package installed')
        exit(1)
    
    filesFile = open('/etc/xlpm/packages/' + pkg)
    files = filesFile.read()
    filesFile.close()

    for file in files.split('\n'):
        os.system('rm -rf ' + file)

    os.remove('/etc/xlpm/packages/' + pkg)

    out.done(f"Removed {pkg}")

    terminate.code(0)
if command == 'info':
    if not os.path.exists(pkg):
        out.error(f"File not found: {pkg}")
        exit(1)
    
    iff = '/tmp/xlpm-info'
    os.mkdir(iff)
    pkgFile = zipfile.ZipFile(pkg)
    pkgFile.extractall(iff)
    if not os.path.exists(f"{iff}/{subprocess.getoutput('ls /tmp/xlpm-info')}"):
        os.error('Package doesn\'t have config file')
        shutil.rmtree(iff)
    configFile = open(f"{iff}/{subprocess.getoutput('ls /tmp/xlpm-info')}/xlp_config.json")
    config = json.loads(configFile.read())
    configFile.close()
    pkgName = config['name']
    pkgVersion = config['version']
    out.info(f"{pkgName} V{pkgVersion}")
    shutil.rmtree(iff)

if command == 'pkginfo':
    out.p(subprocess.getoutput('ls /etc/xlpm/packages'))

if command == 'build':
    if not os.path.exists(f"{pkg}/xlp_config.json"):
        out.error('It seems you forgot about config file')
        sys.exit(1)
    
    os.system(f"zip -r {pkg}.xlp {pkg}")
    out.done(f"Built to {pkg}.xlp")

if command == 'version':
    out.info(f'XLPM V{version}')

terminate.code(0)