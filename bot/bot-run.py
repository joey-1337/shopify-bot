#! /usr/bin/python
import bot
import termcolor

cmds = {
        "purchase":bot.master.purchase,
        "exit":quit,
        "quit":quit
}

while True:
    try:
        cmd = raw_input(termcolor.colored("(bot) ", 'cyan'))
        cmds[cmd]()
    except:
        print termcolor.colored("error when executing comamnd " + cmd, 'red')
        
