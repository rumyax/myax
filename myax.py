import os
import json
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.join(BASE, 'conf.json')

try:
    with open(CONF) as f:
        conf = json.load(f)
except FileNotFoundError:
    conf = {}

RUN = conf.get('run', {})


def usage():
    print('Usage: myax {run|open|i|back|init|commit|post|amend|push}')
    print('    run <key>  - Run the command associated with the key from conf.json')
    print('    open <key> - Open the directory associated with the key from conf.json in VS Code')
    print('    i          - Install npm packages (removes node_modules and package-lock.json first)')
    print('    back       - Restore git repository to a clean state, excluding .env files')
    print('    init       - Initialize a new git repository and make the initial commit')
    print('    commit     - Stage all changes and commit with a user-provided message')
    print('    post       - Push the current branch to the remote repository, setting upstream if necessary')
    print('    amend      - Stage all changes and amend the last commit without changing its message')
    print('    push       - Amend the last commit and force push to the remote repository')


def printError(msg):
    print(f'>>> ERROR :: {msg}')


def run(cmd):
    print(f'$ {cmd}')
    subprocess.run(cmd, shell=True, check=True)


def myax(arg):
    if arg == 'run' or arg == 'open':
        if len(sys.argv) < 3:
            print(f'>>> What to {arg}?!')
            return
        key = sys.argv[2]
        target = RUN.get(key)
        if not target:
            printError('key not found')
            return
        target_path = target.get('path')
        if target_path:
            if not os.path.isdir(target_path):
                printError('path not found')
                return
            os.chdir(target_path)
        if arg == 'open':
            run('code .')
        else:
            cmd = target.get('cmd', 'npm run dev')
            run(cmd)

    elif arg == 'i':
        if os.path.isdir('node_modules'):
            shutil.rmtree('node_modules')
        if os.path.isfile('package-lock.json'):
            os.remove('package-lock.json')
        run('npm install')

    elif arg == 'back':
        run('git restore --staged .')
        run('git restore .')

        env_files = []
        for root, _, files in os.walk('.'):
            for f in files:
                if f.endswith('.env'):
                    env_files.append(os.path.join(root, f))

        exclude = ''.join(f' -e {f}' for f in env_files)
        run(f'git clean -d -f -q -x{exclude}')

    elif arg == 'init':
        run('git init')
        run('git add .')
        run('git commit -m "init"')

    elif arg == 'commit':
        run('git add .')
        run(f'git commit -m "{input('>>> COMMIT MESSAGE :: ')}"')

    elif arg == 'post':
        branch = subprocess.check_output('git branch --show-current', shell=True, text=True).strip()
        if branch:
            run(f'git push --set-upstream origin "{branch}"')
        else:
            printError('branch not found')

    elif arg == 'amend':
        run('git add .')
        run('git commit --amend --no-edit')

    elif arg == 'push':
        myax('amend')
        run('git push --force')

    else:
        usage()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        try:
            myax(sys.argv[1])
        except KeyboardInterrupt:
            print('>>> CANCELED')
