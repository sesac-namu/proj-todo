from typing import Any, Literal, Optional
import flet as ft
from router import Router
import requests

API_ROUTE = "http://localhost:3000"
TOKEN_KEY = "token"


def fetch(
    url: str,
    rest_api: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
    json: Optional[Any] = {},
    headers: Optional[dict] = {"Content-Type": "application/json"},
    cookies: Optional[dict] = None,
):
    match rest_api:
        case "GET":
            return requests.get(
                f"{API_ROUTE}{url}", headers=headers, json=json, cookies=cookies
            )
        case "POST":
            return requests.post(
                f"{API_ROUTE}{url}", headers=headers, json=json, cookies=cookies
            )
        case "PUT":
            return requests.put(
                f"{API_ROUTE}{url}", headers=headers, json=json, cookies=cookies
            )
        case "PATCH":
            return requests.patch(
                f"{API_ROUTE}{url}", headers=headers, json=json, cookies=cookies
            )
        case "DELETE":
            return requests.delete(
                f"{API_ROUTE}{url}", headers=headers, json=json, cookies=cookies
            )


def main(page: ft.Page):
    router = Router.create(page)

    def logout():
        page.session.remove(TOKEN_KEY)
        logout_button.visible = False
        login_signup_buttons.visible = True

        router.navigate("/login")

    navbar = ft.Row(
        [
            ft.FloatingActionButton(
                "Home",
                icon=ft.Icons.HOME,
                on_click=lambda e: router.navigate("/", callback=load_todos),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    logout_button = ft.FloatingActionButton(
        "Logout",
        icon=ft.Icons.LOGOUT,
        on_click=lambda e: logout(),
        visible=page.session.contains_key(TOKEN_KEY),
    )
    login_signup_buttons = ft.Row(
        [
            ft.FloatingActionButton(
                "Login",
                icon=ft.Icons.LOGIN,
                on_click=lambda e: router.navigate("/login"),
            ),
            ft.FloatingActionButton(
                "Sign Up",
                icon=ft.Icons.PERSON_ADD,
                on_click=lambda e: router.navigate("/signup"),
            ),
        ],
        visible=not page.session.contains_key(TOKEN_KEY),
    )

    navbar.controls.append(login_signup_buttons)
    navbar.controls.append(logout_button)

    def Layout(contents: ft.Control):
        return ft.SafeArea(
            ft.Container(
                ft.Column(
                    [
                        ft.Container(navbar, margin=ft.margin.only(bottom=10)),
                        contents,
                    ]
                ),
                expand=True,
            )
        )

    todo_list = ft.ListView(spacing=20)
    stats = ft.Text("0 / 0", size=24)
    title = ft.TextField(label="Title", data="")
    contents = ft.TextField(label="Contents", data="")
    contents_dialog_contents = ft.Column([])
    contents_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Text("Todo"),
                ft.IconButton(
                    ft.Icons.CLOSE, on_click=lambda e: page.close(contents_dialog)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        content=contents_dialog_contents,
        alignment=ft.alignment.center,
        on_dismiss=lambda e: clear_contents_dialog(),
    )

    def clear_contents_dialog():
        contents_dialog_contents.controls.clear()

    def open_contents_dialog(title: str, contents: str):
        contents_dialog_contents.controls.append(ft.Text(title))
        contents_dialog_contents.controls.append(ft.Text(contents))
        page.open(contents_dialog)

    def clear_todo_form():
        title.data = ""
        contents.data = ""
        title.value = ""
        contents.value = ""
        title.update()
        contents.update()

    def create_todo(
        id: str, title: str = "", contents: str = "", checked: bool = False
    ):
        checkbox = ft.Checkbox(
            data=checked, value=checked, on_change=lambda e: update_checked(e)
        )
        item_title = ft.TextField(
            value=title, label="Title", data=title, on_change=lambda e: update_title(e)
        )
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e: delete())
        todo_item = ft.ListTile(
            title=item_title,
            leading=checkbox,
            trailing=delete_button,
            data=id,
            hover_color=ft.Colors.ON_PRIMARY,
            on_click=lambda e: open_contents_dialog(item_title.data or "", contents),
        )

        def update_title(e: ft.ControlEvent):
            fetch(
                f"/todos/update/title/by_id/{id}",
                "PATCH",
                {"title": e.data},
                cookies={"session": page.session.get(TOKEN_KEY)},
            )

            if checkbox.value:
                item_title.color = "green"
            else:
                item_title.color = "black"
            item_title.update()

        def update_checked(e: ft.ControlEvent):
            fetch(
                f"/todos/update/checked/by_id/{id}",
                "PATCH",
                {"checked": e.data},
                cookies={"session": page.session.get(TOKEN_KEY)},
            )

            s = stats.value
            if s is not None:
                ss = s.split(" / ")

                if e.data == "true":
                    ss[0] = str(int(ss[0]) + 1)
                else:
                    ss[0] = str(int(ss[0]) - 1)
                stats.value = " / ".join(ss)
            stats.update()

        def delete():
            if (
                fetch(
                    f"/todos/delete/by_id/{id}",
                    "DELETE",
                    cookies={"session": page.session.get(TOKEN_KEY)},
                ).status_code
                != 200
            ):
                return

            todo_list.controls.remove(todo_item)
            todo_list.update()

            s = stats.value
            if s is not None:
                ss = s.split(" / ")
                ss[1] = str(int(ss[1]) - 1)
                if checked:
                    ss[0] = str(int(ss[0]) - 1)
                stats.value = " / ".join(ss)
            stats.update()

        todo_list.controls.append(todo_item)

    def add_todo(e):
        value = title.value
        if not value or value == "":
            return
        else:
            res = fetch(
                "/todos/create/",
                "POST",
                {"title": value, "contents": contents.value},
                cookies={"session": page.session.get(TOKEN_KEY)},
            )

            if res.status_code != 200:
                return

            id = res.json()["data"]["id"]

            create_todo(
                id,
                value,
                "" if contents.value is None else contents.value,
                False,
            )

            todo_list.update()
            clear_todo_form()

            s = stats.value
            if s is not None:
                ss = s.split(" / ")
                ss[1] = str(int(ss[1]) + 1)
                stats.value = " / ".join(ss)
            stats.update()

            home_view.update()

    def fetch_todos():
        res = fetch(
            "/todos/get", "GET", {}, cookies={"session": page.session.get(TOKEN_KEY)}
        )

        if res.status_code != 200:
            return None

        return res.json()

    def load_todos():
        res = fetch_todos()

        if res is None:
            return

        if not res["ok"]:
            return

        todo_list.controls.clear()

        checked = 0

        for todo in res["data"]:
            create_todo(
                todo["id"],
                todo["title"],
                todo["contents"],
                todo["checked"],
            )

            if todo["checked"]:
                checked += 1

        todo_list.update()

        stats.value = f"{checked} / {len(res['data'])}"
        stats.update()

    home_view = ft.Column(
        [
            title,
            contents,
            ft.Row(
                [
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=add_todo,
                    ),
                    stats,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            todo_list,
        ]
    )

    @router.route("/")
    def Home():
        return Layout(home_view)

    login_username = ft.TextField(label="Username", data="")
    login_password = ft.TextField(label="Password", data="", password=True)

    login_clear_button = ft.TextButton(
        "Clear",
        icon=ft.Icons.CLEAR,
        on_click=lambda e: login_clear(),
    )
    login_submit_button = ft.FilledButton(
        "Login",
        icon=ft.Icons.LOGIN,
        on_click=lambda e: login_submit(),
    )

    login_failed = ft.Text("Login failed", color="red", visible=False)

    def login_clear():
        login_username.data = ""
        login_password.data = ""
        login_username.value = ""
        login_password.value = ""
        login_view.update()

    def login_submit():
        username = login_username.value
        password = login_password.value

        if password == "" or username == "":
            return

        res = fetch("/login", "POST", {"username": username, "password": password})

        if not res.status_code == 200:
            login_failed.visible = True
            login_view.update()
            return

        new_token = res.json()["data"]["token"]

        login_view.update()

        page.session.set(TOKEN_KEY, new_token)

        logout_button.visible = True
        login_signup_buttons.visible = False

        router.navigate("/", callback=load_todos)

    login_view = ft.Column(
        [
            ft.Text("Login"),
            login_username,
            login_password,
            ft.Row(
                [
                    login_clear_button,
                    login_submit_button,
                    login_failed,
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
    )

    @router.route("/login")
    def Login():
        return Layout(login_view)

    signup_username = ft.TextField(label="Username", data="")
    signup_password = ft.TextField(label="Password", data="", password=True)
    signup_email = ft.TextField(label="Email", data="")

    signup_failed = ft.Text("Signup failed", color="red", visible=False)

    def clear_signup():
        signup_username.data = ""
        signup_password.data = ""
        signup_email.data = ""
        signup_username.value = ""
        signup_password.value = ""
        signup_email.value = ""
        signup_view.update()

    def on_signup_submit_click():
        signup_failed.visible = False

        new_username = signup_username.value
        new_password = signup_password.value
        new_email = signup_email.value

        res = fetch(
            "/signup",
            "POST",
            {
                "username": new_username,
                "password": new_password,
                "email": new_email,
            },
        )

        if not res.status_code == 200:
            signup_failed.visible = True
            signup_view.update()
        else:
            router.navigate("/login")

    signup_clear = ft.TextButton(
        "Clear", icon=ft.Icons.CLEAR, on_click=lambda e: clear_signup()
    )
    signup_submit = ft.FilledButton(
        "Signup", icon=ft.Icons.PERSON_ADD, on_click=lambda e: on_signup_submit_click()
    )

    signup_view = ft.Column(
        [
            ft.Text("Signup"),
            signup_username,
            signup_password,
            signup_email,
            ft.Row(
                [signup_clear, signup_submit, signup_failed],
                alignment=ft.MainAxisAlignment.END,
            ),
        ]
    )

    @router.route("/signup")
    def Signup():
        return Layout(signup_view)

    router.navigate("/login")


ft.app(main)
