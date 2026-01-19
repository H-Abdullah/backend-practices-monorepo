#---------------- imports ----------------
import json
import datetime
from tabulate import tabulate

#---------------- main functions/classes ----------------
class VisualInterface:
    # visual interface sepatutnya hanya deal dengan json
    def tabulate_data(self, data: list[dict]) -> None:

        table = tabulate(
            data,
            headers="keys",
            tablefmt="rounded_grid",
            stralign="center",
        )
        
        print(table)
    
    def display_info_text(self) -> None:

        BOLD = '\033[1m'
        ITALIC = '\033[3m'
        END = '\033[0m'

        COMMANDS = [
            ("quit", "Exit the program"),
            ("add <task-name>", "Add a new task"),
            ("delete <task-name>", "Delete an existing task"),
            ("show", "Show all tasks"),
            ("help", "Display this help message"),
        ]

        EXAMPLES = [
            ("add go gym after work"),
            ("delete do laundry at 7am"),
        ]

        print() # newline
        print(f"{BOLD}Task Tracker CLI{END}")
        print(f"{ITALIC} Manage your daily tasks from the terminal{END}")
        print() # newline
        print(f"{BOLD}Usage:{END}")
        for key, msg in COMMANDS:
            print(f"    {key:<30}{ITALIC}{msg}{END}")

        print() # newline
        print(f"{BOLD}Examples:{END}")
        for example in EXAMPLES:
            print(f"    {example}")
        print() # newline

class DataHandler:
    def __init__(self, db, vi):
        self.db: Database = db
        self.vi: VisualInterface = vi
    
    def process_user_input(self):

        user_input = input(">> ",)

        # warn user kalau tiada bagi input
        if len(user_input) <= 0:
            print("Please enter a command")
            return

        # ambil first word as key and others as value
        key, *args = user_input.split(" ",1)

        return self.match_user_input(key, args)

    def match_user_input(self, key: list, args: list):

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
                    self.visualize_all_tasks()
                    return
                
            case "delete":
                if not len(args):
                    print("Please specify a task to delete")
                    return
                
                isTaskExist = self.check_task_existence(args)

                if isTaskExist:
                    self.delete_task(args)
                    self.visualize_all_tasks()
                    return
                else:
                    print(f"'{args[0]}' task doesnt exist")
                    print()
                    self.visualize_all_tasks()
                    return
            case "show":
                self.visualize_all_tasks()
                return

        print("Please enter available command...")

    def add_task(self, value: list[str]) -> None:

        task = value[0]
        new_task = {
            task: {
                "FINISHED": False,
            }
        }        
        self.db.update_data(new_task)
    
    def delete_task(self, task: list):
        self.db.delete_data(task)

    def visualize_all_tasks(self) -> None:
        converted_data = self.convert_dict_to_list()
        self.vi.tabulate_data(converted_data)

    def check_task_existence(self, task):
        data = self.db.load_all_data()

        if task[0] in data:
            return True
        else:
            return False

    def _get_current_date(self):
        pass
        
    def convert_dict_to_list(self):
        dict_data = self.db.load_all_data()

        if not dict_data:
            list_data = [{"TASK": "No task added yet", "FINISHED": "-"}]
        else:
            list_data = [
            {"TASK": task_name, **another_values} 
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
        current_data = self.load_all_data()

        current_data.update(new_task)

        self.save_all_data(current_data)

    def delete_data(self, task: list) -> None:
        current_data = self.load_all_data()

        current_data.pop(task[0])

        self.save_all_data(current_data)

    def load_all_data(self) -> dict:
        with open(self.filename, 'r') as f:
            return json.load(f)
        
    def save_all_data(self, current_data: dict) -> None:
        with open(self.filename, 'w') as f:
            json.dump(current_data, f, indent=2)

def main():

    vi = VisualInterface()
    db = Database()
    dh = DataHandler(db, vi)

    db.create_db()
    vi.display_info_text()

    script_toggle = True

    while script_toggle:
        result = dh.process_user_input()

        if result == "quit":
            script_toggle = False

    return

if __name__ == "__main__":
    main()