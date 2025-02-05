# adjust some paths
$PATH.append('/home/scopatz/sandbox/bin')
$LD_LIBRARY_PATH = ['/home/scopatz/.local/lib', '/home/scopatz/miniconda3/lib', '']

# alias to quit AwesomeWM from the terminal
def _quit_awesome(args, stdin=None):
    lines = $(ps ux | grep "gnome-session --session=awesome").splitlines()
    pids = [l.split()[1] for l in lines]
    for pid in pids:
        kill @(pid)

aliases['qa'] = _quit_awesome

# some customization options, see https://con.sh/envvars.html for details
$MULTILINE_PROMPT = '`·.,¸,.·*¯`·.,¸,.·*¯'
$DEEPSH_SHOW_TRACEBACK = True
$DEEPSH_STORE_STDOUT = True
$DEEPSH_HISTORY_MATCH_ANYWHERE = True
$COMPLETIONS_CONFIRM = True
$DEEPSH_AUTOPAIR = True
