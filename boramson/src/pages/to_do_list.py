import flet as ft
from layout.layout_app_bar_top import layout_app_bar_top
from utils.to_do import TodoApp


def to_do_list(page: ft.Page):
    layout_app_bar_top(page)

    page.title = "To-Do App"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    todo = TodoApp()

    # add application's root control to the page
    page.add(todo)


ft.app(to_do_list)
