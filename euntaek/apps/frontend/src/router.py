from typing import Callable, Optional
import flet as ft


class Route:
    path: str
    view: ft.View

    def __init__(self, path: str, view: ft.Control):
        self.path = path
        self.view = ft.View(path, [view])


class Router:
    MAX_HISTORY_LENGTH = 10
    history: list[str]
    history_index: int
    routes: list[Route]
    current_path: str
    page: ft.Page

    @classmethod
    def create(cls, page: ft.Page):
        return cls(page)

    def __init__(self, page: ft.Page):
        self.history = []
        self.history_index = 0
        self.routes = []
        self.current_path = page.route
        self.page = page

    def add_history(self, path: str):
        if len(self.history) == Router.MAX_HISTORY_LENGTH:
            self.history.pop(0)
            self.history.append(path)
        else:
            self.history_index += 1
            self.history.append(path)

    def add_route(self, path: str, view: ft.Control):
        route = Route(path, view)
        self.routes.append(route)

    def navigate(
        self,
        path: str,
        append_history: bool = True,
        callback: Optional[Callable] = None,
    ):
        for route in self.routes:
            if route.path == path:
                self.page.views.clear()
                self.page.views.append(route.view)
                self.page.update()
                route.view.update()

                if append_history:
                    self.add_history(path)
                else:
                    if len(self.history) != self.history_index:
                        self.history = self.history[: self.history_index]

                if callback:
                    callback()

                return

        raise ValueError(f"Route {path} not found")

    def go_back(self):
        if len(self.history) > 1:
            self.history_index -= 1
            self.navigate(self.history[-2], append_history=False)

    def go_forward(self):
        if len(self.history) > 0 and self.history[-1] != self.current_path:
            self.history_index -= 1
            self.navigate(self.history[-1], append_history=False)

    def route(self, path: str):
        def decorator(func):
            self.add_route(path, func())
            return func

        return decorator
