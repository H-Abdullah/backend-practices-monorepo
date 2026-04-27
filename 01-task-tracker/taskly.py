import argparse
import json
import datetime

class TaskVisualizer:
    def visualize_task(self, data):
        self._tabulate_task(data)

    def visualize_task_for_list(self, data, status):
        filtered_data = self._filter_task(data, status)
        self._tabulate_task(filtered_data)

    def _tabulate_task(self, data):
        if not data:
            print("\nNo tasks found.\n")
            return

        print("\n") # For top space

        headers = ["description", "status", "id", "createdAt", "updatedAt"]

        # Calculate column widths
        col_widths = {}

        for header in headers:
            max_width = len(header)
            for row in data:
                max_width = max(max_width, len(str(row[header])))
            col_widths[header] = max_width

        # Print header
        header_row = " | ".join(
            header.upper().center(col_widths[header])
            for header in headers
        )
        print(header_row)

        # Print separator
        separator = "-+-".join(
            "-" * col_widths[header]
            for header in headers
        )
        print(separator)

        # Print rows
        for row in data:
            row_line = " | ".join(
                str(row[header]).ljust(col_widths[header])
                for header in headers
            )
            print(row_line)  

        print("\n") # For bottom space

    def _filter_task(self, data, status):
        if status is None:
            return data
        else:
            filtered_task = [
                task for task in data if task["status"] == status
            ]
    
            return filtered_task

class ArgumentParserHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.subparser = self.initialize_parser()

    def parse_all_arguments(self):

        # calling all args methods
        self.list_subp()
        self.add_subp()
        self.delete_subp()
        self.clear_subp()
        self.update_subp()
        self.mark_in_progress_subp()
        self.mark_done_subp()

        return self.parser.parse_args()
    
    def initialize_parser(self):
        sp = self.parser.add_subparsers(
            dest='command',
            required=True
        )
        return sp

    def display_help_info(self):
        self.parser.print_help()
        
    def list_subp(self):
        list_task = self.subparser.add_parser('list', help='Show all current listed tasks')
        list_task.add_argument(
            "status",
            nargs="?",
            choices=["todo", "in-progress", "done"],
            help="Filter task based on status",
        )

    def add_subp(self):
        add_task = self.subparser.add_parser('add', help='Add new task')
        add_task.add_argument('task')

    def delete_subp(self):
        del_task = self.subparser.add_parser('delete', help='Delete a task')
        del_task.add_argument('id', type=int)

    def clear_subp(self):
        self.subparser.add_parser('clear', help='Clear all task')

    def update_subp(self):
        update_task = self.subparser.add_parser('update', help='Update task name')
        update_task.add_argument('id', type=int)
        update_task.add_argument('new_task_name')

    def mark_in_progress_subp(self):
        mark_in_progress_task = self.subparser.add_parser('mark-in-progress', help='Mark selected task with "IN-PROGRESS"')
        mark_in_progress_task.add_argument('id', type=int)

    def mark_done_subp(self):
        mark_done_task = self.subparser.add_parser('mark-done', help="mark selected task with 'DONE'")
        mark_done_task.add_argument('id', type=int)

class DataController:
    def __init__(self, aph, td, tv):
        self.tv: TaskVisualizer = tv
        self.aph: ArgumentParserHandler = aph
        self.td: TaskDatabase = td
        self.args = self.aph.parse_all_arguments()

    def run(self):
        
        if self.args.command is None:
            self.aph.display_help_info()

        if self.args.command == 'list':
            self.display_list()

        if self.args.command == 'add':
            self.add_task()

        if self.args.command == 'delete':
            self.delete_task()

        if self.args.command == 'clear':
            self.clear_task()

        if self.args.command == 'update':
            self.update_task()
        
        if self.args.command in ('mark-in-progress', 'mark-done'):
            self.mark_task()

    def display_list(self):
        current_data = self.td.load_all_data()
        self.tv.visualize_task_for_list(current_data, self.args.status)

    def add_task(self):
        if len(self.args.task) <= 5:
            print('Task name must be longer than 5 letters')
            return
        
        isTaskExist = self._task_name_checker()

        if isTaskExist:
            print('Task already exist')
            current_data = self.td.load_all_data()
            self.tv.visualize_task(current_data)
            return
        
        new_task = {
                "description": self.args.task,
                "status": 'todo',
                "id": self._get_task_id(),
                "createdAt": self._get_current_datetime(),
                "updatedAt": self._get_current_datetime(),
        }
            
        self.td.add_data(new_task)

        current_data = self.td.load_all_data()
        self.tv.visualize_task(current_data)

    def delete_task(self):
        
        isTaskExist = self._task_id_checker()

        if isTaskExist:
            self.td.delete_data(self.args.id)
            current_data = self.td.load_all_data()
            self.tv.visualize_task(current_data)
            return
        else:
            print('Task doesnt exist')
            current_data = self.td.load_all_data()
            self.tv.visualize_task(current_data)

    def clear_task(self):
        confirm_delete = False

        if not confirm_delete:
            print('Are you sure to delete all task? (y/n)')
            user_input = input('').lower()

            if user_input == 'n' or user_input == 'no':
                return
            elif user_input == 'y' or user_input == 'yes':
                confirm_delete = True
            else:
                print("Incorrect input. 'y' or 'n' only")
                return
            
        if confirm_delete:
            self.td.reset_all_data()
            current_data = self.td.load_all_data()
            self.tv.visualize_task(current_data)

    def update_task(self):
        isTaskExist = self._task_id_checker()

        if not isTaskExist:
            print('Invalid task. Please choose correct task id')
            current_data = self.td.load_all_data()
            self.tv.visualize_task(current_data)
            return
        
        if len(self.args.new_task_name) <= 5:
            print('Task name must be longer than 5 letters')
            return
    
        self.td.update_data(
            self.args.id, 
            description=self.args.new_task_name,
            updatedAt=self._get_current_datetime())
        current_data = self.td.load_all_data()
        self.tv.visualize_task(current_data)

    def mark_task(self):
        isTaskExist = self._task_id_checker()

        mark_options = {
            "mark-in-progress": "in-progress",
            "mark-done": "done",
        }

        if not isTaskExist:
            print('Invalid task. Please choose correct task id')
            current_data = self.td.load_all_data()
            self.tv.visualize_task(current_data)
            return
        
        mark_type = self.args.command
        self.td.update_data(
            self.args.id, 
            status=mark_options.get(mark_type),
            updatedAt=self._get_current_datetime())
        current_data = self.td.load_all_data()
        self.tv.visualize_task(current_data)


    def _task_name_checker(self):
        current_data = self.td.load_all_data()

        for task in current_data:
            if task['description'] == self.args.task:
                return True
                
        return False
    
    def _task_id_checker(self):
        current_data = self.td.load_all_data()

        for task in current_data:
            if task['id'] == self.args.id:
                return True
                
        return False
    
    def _get_task_id(self):
        current_data = self.td.load_all_data()

        ids = [task["id"] for task in current_data if "id" in task]

        return max(ids, default=0) + 1
    
    def _get_current_datetime(self):
        c_datetime = datetime.datetime.now()
        formatted_c_datetime = c_datetime.strftime("%A, %-d %B %Y, %-I:%M %p")

        return formatted_c_datetime


class TaskDatabase:
    def __init__(self):
        self.filename: str = "tasks.json"
        self.create_db()
    
    def create_db(self):
        try:
            with open(self.filename, 'x') as f:
                json.dump([], f)
                print("Initial database template created")
        except FileExistsError:
            return

    def add_data(self, new_task: dict) -> None:
        current_data = self.load_all_data()

        current_data.append(new_task)

        self.save_all_data(current_data)

    def delete_data(self, task_id: list) -> None:
        current_data = self.load_all_data()

        for index, task in enumerate(current_data):
            if task['id'] == task_id:
                current_data.pop(index)

        self.save_all_data(current_data)

    def update_data(self, task_id, **updates):
        current_data = self.load_all_data()

        ALLOWED_KEYS = ['description', 'status', 'updatedAt']

        for task in current_data:
            if task['id'] == task_id:
                for k,v in updates.items():
                    if k in ALLOWED_KEYS:
                        task[k] = v

        self.save_all_data(current_data)

    def reset_all_data(self):
        with open(self.filename, 'w') as f:
            json.dump([], f)

    def load_all_data(self) -> dict:
        with open(self.filename, 'r') as f:
            return json.load(f)
        
    def save_all_data(self, current_data: dict) -> None:
        with open(self.filename, 'w') as f:
            json.dump(current_data, f, indent=2)        
        
def main():
    tv = TaskVisualizer()
    td = TaskDatabase()
    aph = ArgumentParserHandler()
    dc = DataController(aph, td, tv)

    dc.run()

if __name__ == "__main__":
    main()