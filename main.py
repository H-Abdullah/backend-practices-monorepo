#---------------- imports ----------------
import json
import datetime

#---------------- main functions/classes ----------------
class VisualInterface:
    # visual interface sepatutnya hanya deal dengan json
    pass

class DataHandler:
    def __init__(self, db):
        self.db: Database = db
    
    def process_user_input(self):

        user_input = input()

        # warn user kalau tiada bagi input
        if len(user_input) <= 0:
            print("Please enter a command")
            return

        # ambil first word as key and others as value
        key, *args = user_input.split(" ",1)

        return self.match_user_input(key, args)

    def match_user_input(self, key, args):

        sanitized_key = key.strip().lower()

        match sanitized_key:
            case "quit":
                return sanitized_key
            case "add":
                if len(args) <= 0:
                    print("Please type a task")
                    return
                else:
                    self.add_task(args)
                    return
            case "delete":
                self.delete_all_task()
                return
            case "show":
                self.show_available_tasks()
                return

        print("Please enter available command...")

    def add_task(self, value: list[str]) -> None:

        task = value[0]

        new_task = {
            task: {
                "finished": False,
                "createdAtDate": "",
                "finishedAtDate": ""
            }
        }        
        self.db.update_data(new_task)
    
    def delete_all_task(self):
        self.db.delete_all_data()

    def show_available_tasks(self):
        print(self.db.load_all_data())

    def _get_current_date(self):
        pass
        
    def convert_dict_to_list(self):
        dict_data = self.db.load_all_data()

        list_data = [
            {"task": task_name, **another_values} 
            for task_name, another_values in dict_data.items()
        ]

        return list_data


class Database:
    def __init__(self):
        self.filename: str = "tasks.json"
    
    def create_db(self):
        try:
            with open(self.filename, 'x') as f:
                json.dump({}, f)
                print("Initial database template created")
        except FileExistsError:
            return

    def update_data(self, new_task: dict) -> None:
        with open(self.filename, 'r') as f:
            current_data = json.load(f)

        current_data.update(new_task)

        with open(self.filename, 'w') as f:
            json.dump(current_data, f, indent=2)

    def delete_all_data(self): 
        with open(self.filename, 'w') as f:
            json.dump({}, f)

    def load_all_data(self) -> dict:
        with open(self.filename, 'r') as f:
            return json.load(f)

def main():

    # vi = VisualInterface()
    db = Database()
    dh = DataHandler(db)

    db.create_db()

    script_toggle = True

    while script_toggle:
        result = dh.process_user_input()

        if result == "quit":
            script_toggle = False

    return

if __name__ == "__main__":
    main()


# # ambil input > save > display
# dapt sudah user input
# class Scheduler:
#     def __init__(self):
#         self.task_data = {}

#     def start_script(self, task_backend):

#         task_backend.create_json()


#             user_input = input()

#             # if user doesnt input anything
#             if len(user_input) <= 0: 
#                 print("You typed nothing. Please input a command")
#                 break
            

    
#             key, value = self._cleaned_user_input(user_input)

#             # if user wants to quit the script
#             if key == 'quit':
#                 self.turn_off_script()

#             # if user wants to add tasks
#             if key == 'add':
#                 if len(value) <= 0:
#                     print("add should be paired with task. eg: add doing laundry")
#                     return
#                 else:
#                     self.task_data.update({
#                         'task': f'{value}',
#                         'checked': False,
#                     })

#             task_backend.dict_to_json(self.task_data)

#     # def main(self, user_cmd):

#     #     if len(user_cmd) <= 0:
#     #         return "Please input a command"
        
#     #     key, value = self._cleaned_user_input(user_cmd)

#     #     if key == 'quit':
#     #         return self.turn_off_script
        
#     #     if key == 'add':
#     #         if len(value) <= 0:
#     #             return "Specify the task that you want to add"
#     #         else:
#     #             self.task_data.update({
#     #                 'task': 'value',
#     #                 'checked': False
#     #             })

#     #     return

#         # if key == "quit":
#         #     return self.turn_off_script
#         # elif key == "add":
#         #     return self.add_task(key, value)

#     # def user_input(self, inputted_cmd):
#     #     input = {
#     #         "quit": self.turn_off_script,
#     #         "add": self.add_task(key, value),
#     #         # "delete": "Remove something here",
#     #         #"check": "Check something here",
#     #         #"uncheck": "Uncheck something here",
#     #     }

#     #     key, value = self._cleaned_input(inputted_cmd)

#     #     if len(value) < 1 and key == "quit":
#     #         pass
#     #     elif len(value) < 1:
#     #         print(f"{key} what? Please specify the task!")
#     #         return

#     #     if key in input:
#     #         if key is "add":
#     #             return self.add_task(key, value)
#     #     else:
#     #         return "key not found. type help for more info"

#     def turn_off_script(self):
#         self.is_script_running = False
#         print('exiting script...')
        
#     def add_task(self, key, value):
#         self.task_data.update(key=f"{value}")

#     def _cleaned_user_input(self, user_input):

#         splitted_input = user_input.split(' ')
#         key = self._cleaned_input_key(splitted_input[0])
#         value = " ".join(splitted_input[1:])
    
#         return [key, value]
    
#     def _cleaned_input_key(self, key):
#         return key.strip().lower()


# class TaskBackend:
#     def __init__(self):
#         self.filename = "task.json"

#     def create_json(self):
#         try:
#             with open(self.filename, 'x') as file:
#                 pass
#         except FileExistsError:
#             return "File already exist"
        
#     # def dict_to_json(self, data):
#     #     with open(self.filename, 'a') as f:
#     #         .dumps(data)
        

# #taip add Cuci kain
# #add_task() akan run
# #dalam add_task() akan run backend iaitu append_task()
# def intro_text():
#     intro_text = """
#     Available commands:
#         add - adding new task
#         delete - deleting task
#         check - mark completed task
#         uncheck - unmark checked task
#         help - show this info
    
#     eg: task add medical checkup

#     Insert your command\n\n""" 

#     print(intro_text)
    

# def main():
#     sh = Scheduler()
#     tb = TaskBackend()

#     toggle_script = True
    
#     while toggle_script:
#         sh.start_script()

#     # tb.create_json()
#     # intro_text()

#     # while sh.is_script_running:

#     #     user_cmd = input()
#     #     cmd = sh.main(user_cmd)

#     #     if callable(cmd):
#     #         cmd()
#     #     else:
#     #         print("Looks like none of the method called")
    
#     # tb.dict_to_json(sh.task_data)

# main()



# start script 
#     start looping
#         pilih command
#             command called
#                 if command quit
#                     loop stopped
#                 kalau tidak:
#                     teruskan loop
