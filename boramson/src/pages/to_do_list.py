# pages/to-do_list.py
import flet as ft
from layout.layout_app_bar_top import layout_app_bar_top
from layout.layout_app_bar_bottom import layout_app_bar_bottom


# 이 main.py의 main 함수가 최종적으로 ft.app의 target이 됩니다.
def to_do_list(page: ft.Page):
    # 1. 먼저 components의 함수를 호출하여 페이지의 기본 레이아웃(앱 바, 드로어 등)을 설정합니다.
    layout_app_bar_top(page)  # page 객체를 전달하여 UI를 구성하게 함
    layout_app_bar_bottom(page)  # page 객체를 전달하여 UI를 구성하게 함

    additional_content = ft.Column(
        [
            ft.Text("Test.", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("이 내용은 main.py에서 추가되었습니다."),
            ft.ElevatedButton(
                "Click me from main.py",
                on_click=lambda e: print("Button in main.py clicked!"),
            ),
            ft.ElevatedButton(
                "About 페이지로 이동", on_click=lambda _: page.go("/about")
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # 기존에 page.add()로 추가된 내용이 있다면 그 아래에 추가됩니다.
    # layout_app_bar_top.py에서 page.add()를 호출하지 않았다면, 이것이 첫 번째 내용이 됩니다.
    page.add(additional_content)

    # page.update()는 main_with_full_layout 내부에서도 호출될 수 있고,
    # 여기서도 필요에 따라 호출할 수 있습니다.
    # 일반적으로는 한 번의 로직 흐름이 끝난 후 마지막에 호출하는 것이 좋습니다.
    page.update()


ft.app(to_do_list)
