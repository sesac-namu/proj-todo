# navigation/nav_drawer.py
import flet as ft  # Flet 라이브러리를 ft라는 별칭으로 가져옵니다.


# 네비게이션 드로어를 설정하고 관련 핸들러를 반환하는 함수 정의
def nav_drawer(page: ft.Page):
    """
    페이지에 네비게이션 드로어를 설정하고,
    드로어를 열기 위한 이벤트 핸들러를 반환합니다.
    이 함수는 page.drawer 및 관련 이벤트 핸들러를 직접 설정합니다.
    """

    # --- 드로어 메뉴 선택 시 실행될 내부 이벤트 핸들러 함수 ---
    # 이 함수는 nav_drawer 함수 내부에 정의되어 클로저(closure)를 형성합니다.
    # 즉, 이 함수는 자신이 정의된 환경(nav_drawer 함수의 page 변수)에 접근할 수 있습니다.
    def _on_menu_selected(
        e: ft.ControlEvent,
    ):  # 'e'는 Flet 컨트롤 이벤트를 나타내는 객체입니다.
        selected_label = (
            e.control.label
        )  # 이벤트가 발생한 컨트롤(NavigationDrawerDestination)의 label 속성을 가져옵니다.
        print(
            f"nav_drawer.py: Menu selected - {selected_label}"
        )  # 선택된 메뉴의 라벨을 콘솔에 출력합니다.

        # 여기에 각 메뉴 선택 시 수행할 실제 동작을 추가할 수 있습니다.
        # 예: if selected_label == "Home": page.go("/") # 페이지 라우팅
        # 예: if selected_label == "Settings": open_settings_dialog() # 설정 다이얼로그 열기

        page.drawer.open = False  # 드로어를 닫습니다.
        page.update()  # 페이지 UI를 업데이트하여 변경사항(드로어 닫힘)을 반영합니다.

    # --- 페이지의 네비게이션 드로어 UI 구성 및 할당 ---
    # page 객체의 drawer 속성에 ft.NavigationDrawer 컨트롤 인스턴스를 할당합니다.
    # 이렇게 하면 이 드로어가 해당 페이지의 기본 드로어가 됩니다.
    page.drawer = ft.NavigationDrawer(
        controls=[  # 드로어 내부에 표시될 컨트롤(메뉴 항목)들의 리스트입니다.
            ft.Container(height=20),  # 메뉴 상단의 약간의 여백을 위한 컨테이너입니다.
            # 각 메뉴 항목은 ft.NavigationDrawerDestination 컨트롤로 정의됩니다.
            ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Home"),  # 홈 메뉴
            ft.NavigationDrawerDestination(
                icon=ft.Icons.STORE, label="Store"
            ),  # 스토어 메뉴
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SETTINGS, label="Settings"
            ),  # 설정 메뉴
            ft.NavigationDrawerDestination(
                icon=ft.Icons.LOGOUT, label="Logout"
            ),  # 로그아웃 메뉴
        ]
    )
    # --- 페이지의 네비게이션 드로어 메뉴 선택 이벤트와 핸들러 연결 ---
    # page 객체의 on_navigation_drawer_destination_selected 이벤트가 발생하면(사용자가 드로어 메뉴를 선택하면)
    # 위에서 정의한 _on_menu_selected 함수가 호출되도록 설정합니다.
    page.on_navigation_drawer_destination_selected = _on_menu_selected

    # --- 드로어를 열기 위한 이벤트 핸들러 함수 ---
    # 이 함수는 외부(예: AppBar의 메뉴 버튼)에서 호출될 수 있도록 정의됩니다.
    def open_drawer_handler(
        e: ft.ControlEvent,
    ):  # 'e'는 이벤트 객체 (여기서는 버튼 클릭 이벤트 등)
        if page.drawer:  # 페이지에 드로어가 실제로 설정되어 있는지 확인합니다.
            page.drawer.open = True  # 드로어의 open 상태를 True로 설정하여 엽니다.
            page.update()  # 페이지 UI를 업데이트하여 드로어가 열린 것을 반영합니다.
        else:
            # 만약 어떤 이유로 page.drawer가 설정되지 않았다면 오류 메시지를 출력합니다.
            # (이 코드 흐름상으로는 page.drawer가 항상 설정되어 있어야 하지만, 방어적인 코드)
            print("nav_drawer.py: Error - Drawer not initialized on the page.")

    # --- 드로어 열기 핸들러 반환 ---
    # 이 함수(nav_drawer)를 호출한 곳에서 open_drawer_handler 함수를 사용할 수 있도록 반환합니다.
    # 예를 들어, AppBar의 메뉴 버튼 클릭 이벤트에 이 핸들러를 연결할 수 있습니다.
    return open_drawer_handler
