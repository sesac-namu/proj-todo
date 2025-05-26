from typing import Callable, Optional
import flet as ft


class Route:
    path: str
    component: ft.Control

    def __init__(self, path: str, component: ft.Control):
        self.path = path
        self.component = component

    def get_view(self):
        return ft.View(self.path, [self.component])


routes: list[Route] = []
history: list[str] = []
MAX_HISTORY_LENGTH = 10
history_index = 0


def add_history(path: str):
    if len(history) == MAX_HISTORY_LENGTH:
        history.pop(0)
        history.append(path)
    else:
        global history_index
        history_index += 1
        history.append(path)


def create_route(path: str, component: ft.Control):
    route = Route(path, component)
    routes.append(route)


def route(path: str):
    def decorator(func):
        create_route(path, func())
        return func

    return decorator


class Router:
    page: ft.Page

    def __init__(self, page: ft.Page):
        self.page = page

    def navigate(
        self,
        path: str,
        append_history: bool = True,
        callback: Optional[Callable] = None,
    ):
        for route in routes:
            if route.path == path:
                self.page.views.clear()
                self.page.views.append(route.get_view())
                self.page.update()

                if append_history:
                    add_history(path)
                else:
                    global history
                    if len(history) != history_index:
                        history = history[:history_index]

                if callback:
                    callback()

                return

        raise ValueError(f"Route {path} not found")


__all__ = ["add_history", "create_route", "route", "Router"]
