from deepsh.built_ins import XSH

env = XSH.env
# adjust some paths
env["PATH"].append("/home/scopatz/sandbox/bin")
env["LD_LIBRARY_PATH"] = ["/home/scopatz/.local/lib", "/home/scopatz/miniconda3/lib"]

# alias to quit AwesomeWM from the terminal
def _quit_awesome(args, stdin=None):
    print("awesome python code")


XSH.aliases["qa"] = _quit_awesome
# setting aliases as list are faster since they don't involve parser.
XSH.aliases["gc"] = ["git", "commit"]

# some customization options, see https://con.sh/envvars.html for details
env["MULTILINE_PROMPT"] = "`·.,¸,.·*¯`·.,¸,.·*¯"
env["DEEPSH_SHOW_TRACEBACK"] = True
env["DEEPSH_STORE_STDOUT"] = True
env["DEEPSH_HISTORY_MATCH_ANYWHERE"] = True
env["COMPLETIONS_CONFIRM"] = True
env["DEEPSH_AUTOPAIR"] = True
