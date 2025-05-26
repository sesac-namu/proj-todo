# components/layout_app_bar_bottom.py
import flet as ft


# ##### 플로팅 액션 버튼 (FAB) 정의 #####
def layout_app_bar_bottom(page: ft.Page):

    # Alignment
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Folating Action button
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        shape=ft.CircleBorder(),
        # on_click 핸들러는 필요하다면 여기에 정의된 다른 함수와 연결 가능
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_FLOAT


if __name__ == "__main__":
    ft.app(layout_app_bar_bottom)
