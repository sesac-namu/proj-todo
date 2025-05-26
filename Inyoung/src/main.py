import flet as ft
import json
import os

class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete, page):
        super().__init__()
        self.completed = False
        self.is_in_progress = False  # Initialize the attribute
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.page = page
        

        # self.display_task = ft.Checkbox(
        #     value=False, label=self.task_name, on_change=self.status_changed
        # )
        self.display_task = ft.Checkbox(
            value=False, on_change=self.status_changed
        )

        self.todowidget = ft.Row(controls=[
            self.display_task,
            ft.GestureDetector(
                on_tap=self.label_clicked,
                content=ft.Text(value=self.task_name),
            ),
        ])

        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.todowidget,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]


    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        if self.display_task.value:  # Checkbox checked
            if self.is_in_progress:  # If already "In Progress", mark as "Done"
                self.completed = True
                self.is_in_progress = False
                self.display_task.value = True
            else:  # Move to "In Progress"
                self.completed = False
                self.is_in_progress = True
                self.display_task.value = False  # Automatically uncheck after state change
        else:  # Checkbox unchecked
            if self.completed:  # Revert "Done" to "In Progress"
                self.completed = False
                self.is_in_progress = True
            else:  # Reset to "Not Working"
                self.completed = False
                self.is_in_progress = False
        self.task_status_change(self)
        self.update()  # Update the UI

    def delete_clicked(self, e):
        self.task_delete(self)

    def label_clicked(self, e):
        print('label clicked')

        dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete all those files?"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: self.page.close(dlg_modal)),
            ft.TextButton("No", on_click=lambda e: self.page.close(dlg_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
        
        self.page.open(dlg_modal)

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

class TodoApp(ft.Column):
    # application's root control is a Column containing all other controls
    def __init__(self, page):
        super().__init__()
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True
        )
        self.tasks = ft.Column()
        self.page = page

        if (not os.path.exists("tasks.json")) or os.path.getsize('tasks.json'):
            with open('tasks.json', "w") as f:
                json.dump([], f)
        self.DATA_FILE = "tasks.json"  # 데이터를 저장할 파일 경로

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Not Working"), ft.Tab(text="In Progress"), ft.Tab(text="Done")],
        )

        self.items_left = ft.Text("0 items left")

        self.width = 600
        self.controls = [
            ft.Row(
                [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Clear completed", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]
        # 앱 시작 시 데이터 로드
        self.load_tasks()

    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete, self.page)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()
            self.save_tasks()  # 새 데이터 저장

    def save_tasks(self):
        """현재 tasks 데이터를 JSON 파일에 저장."""
        tasks_data = []
        for task in self.tasks.controls:
            tasks_data.append({
                "task_name": task.task_name,
                "completed": task.completed,
                "is_in_progress": task.is_in_progress,
            })
        with open(self.DATA_FILE, "w") as f:
            json.dump(tasks_data, f)

    def load_tasks(self):
        """JSON 파일에서 tasks 데이터를 로드."""
        try:
            with open(self.DATA_FILE, "r") as f:
                tasks_data = json.load(f)
                for data in tasks_data:
                    task = Task(
                        data["task_name"],
                        self.task_status_change,
                        self.task_delete,
                        self.page,
                    )
                    task.completed = data["completed"]
                    task.is_in_progress = data["is_in_progress"]
                    self.tasks.controls.append(task)
                self.update()
        except FileNotFoundError:
            print("No saved tasks found. Starting fresh.")
        except json.JSONDecodeError:
            print("Error reading tasks file. Starting fresh.")

    def task_status_change(self, task):
        self.update()
        self.save_tasks()  # 상태 변경 후 저장

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()
        self.save_tasks()  # 상태 변경 후 저장

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)
        self.save_tasks()  # 상태 변경 후 저장

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            # Update visibility based on the selected tab and task state
            task.visible = (
                (status == "Not Working" and not task.completed and not task.is_in_progress)
                or (status == "In Progress" and task.is_in_progress)
                or (status == "Done" and task.completed)
            )
            # Count tasks that are not completed and not in progress
            if not task.completed and not task.is_in_progress:
                count += 1
        self.items_left.value = f"{count} active item(s) left"

def main(page: ft.Page):
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    page.dialog = None
    # create app control and add it to the page
    page.add(TodoApp(page))


ft.app(main)
