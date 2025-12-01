#---------------- imports ----------------
from time import sleep

#---------------- main functions/classes ----------------
class Scheduler:
    def __init__(self):
        self.is_script_running = True

    def user_input(self, cmd):
        input = {
            "quit": self.turn_off_script,
            "add": self.test,
            "delete": "Remove something here",
            "check": "Check something here",
            "uncheck": "Uncheck something here",
        }

        text_input = cmd.strip().lower()

        if text_input in input:
            return input[text_input]
        else:
            return "not found"
        
    def turn_off_script(self):
        self.is_script_running = False
        print('exiting script...')
        
    def add_task(self):
        print("adding something")
        

def intro_text():
    intro_text = """
    Available commands:
        add - adding new task
        delete - deleting task
        check - mark completed task
        uncheck - unmark checked task
        help - show this info
    
    eg: task add medical checkup

    Insert your command\n\n""" 

    print(intro_text)
    

def main():
    sh = Scheduler()

    intro_text()

    while sh.is_script_running:

        user_cmd = input()
        cmd = sh.user_input(user_cmd)

        if callable(cmd):
            cmd()
        else:
            print(cmd)

main()