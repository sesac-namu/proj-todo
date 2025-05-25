# components/layout_app_bar_top.py
import flet as ft


# 이 파일의 main 함수는 페이지 전체를 구성합니다.
def layout_app_bar_top(page: ft.Page):  # 함수 이름을 변경하여 main.py의 main과 구분
    # --- 페이지 기본 설정 ---
    page.title = "To-do List (Standalone Component)"  # 제목 변경으로 구분

    # =====================================================================
    # Alignment
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # =====================================================================
    # # ##### 테마 변경 기능 정의 #####
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    # =====================================================================
    # ##### 상단 앱 바 (AppBar) 정의 #####
    page.appbar = ft.AppBar(
        title=ft.Text("To-do List"),  # 이 AppBar의 제목
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
        ),
        bgcolor=ft.Colors.BLUE,
        actions=[
            ft.IconButton(icon=ft.Icons.SEARCH),
            ft.IconButton(icon=ft.Icons.FAVORITE),
            ft.IconButton(icon=ft.Icons.DARK_MODE, on_click=toggle_theme),
        ],
    )


# 이 파일이 직접 실행될 때만 ft.app을 호출하도록 하거나, 아예 호출하지 않음
if __name__ == "__main__":
    ft.app(layout_app_bar_top)
