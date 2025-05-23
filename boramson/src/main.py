import flet as ft # Flet 라이브러리를 ft라는 별칭으로 가져옵니다.

# ##### 메인 애플리케이션 함수 정의 #####
def main(page: ft.Page): # Flet 앱의 진입점 함수입니다. page 객체를 인자로 받습니다.
    # --- 페이지 기본 설정 ---
    page.title = "To-do List" # 웹 브라우저 탭 또는 앱 창의 제목을 설정합니다.

    # =====================================================================
    # 페이지 내 컨트롤들의 수직 정렬 방식을 설정합니다. START는 위쪽부터 정렬입니다.
    page.vertical_alignment = ft.MainAxisAlignment.START
    # 페이지 내 컨트롤들의 수평 정렬 방식을 설정합니다. CENTER는 가운데 정렬입니다.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # =====================================================================
    # ##### 네비게이션 드로어 (사이드 메뉴) 관련 기능 및 UI 정의 #####

    # --- 네비게이션 드로어 열기 이벤트 핸들러 ---
    def open_drawer(e): # 이벤트 객체 'e'를 인자로 받습니다 (여기서는 사용되지 않음).
        """네비게이션 드로어를 엽니다."""
        page.drawer.open = True # 페이지의 드로어 속성의 open 상태를 True로 설정합니다.
        page.update() # 페이지 UI를 업데이트하여 변경사항을 반영합니다.

    # --- 네비게이션 드로어 메뉴 선택 이벤트 핸들러 ---
    def on_menu_selected(e): # ft.NavigationDrawerDestinationSelectedEvent 객체 'e'를 인자로 받습니다.
        """네비게이션 드로어에서 메뉴가 선택되었을 때 호출됩니다."""
        selected_label = e.control.label # 선택된 메뉴 항목의 라벨 텍스트를 가져옵니다.
        print(f"Selected menu: {selected_label}") # 콘솔에 선택된 메뉴를 출력합니다 (디버깅/확인용).
        page.drawer.open = False # 드로어를 닫습니다.
        page.update() # 페이지 UI를 업데이트합니다.

    # --- 1. 네비게이션 드로어 UI 구성 ---
    page.drawer = ft.NavigationDrawer(
        controls=[ # 드로어 내부에 표시될 컨트롤(메뉴 항목)들의 리스트입니다.
            ft.Container(height=20), # 메뉴 상단의 약간의 여백을 위한 컨테이너입니다.
            ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Home"), # 홈 메뉴
            ft.NavigationDrawerDestination(icon=ft.Icons.STORE, label="Store"), # 스토어 메뉴
            ft.NavigationDrawerDestination(icon=ft.Icons.SETTINGS, label="Settings"), # 설정 메뉴
            ft.NavigationDrawerDestination(icon=ft.Icons.LOGOUT, label="Logout"), # 로그아웃 메뉴
        ]
    )
    
    # ?! 페이지의 네비게이션 드로어 메뉴 선택 이벤트를 on_menu_selected 함수와 연결합니다.
    page.on_navigation_drawer_destination_selected = on_menu_selected



    # =====================================================================
    # =====================================================================
    # =====================================================================
    # ##### 플로팅 액션 버튼 (FAB) 정의 #####
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, # 버튼에 표시될 아이콘입니다 (더하기 모양).
        shape=ft.CircleBorder() # 버튼의 모양을 원형으로 설정합니다.
    )
    # 플로팅 액션 버튼의 위치를 설정합니다. CENTER_DOCKED는 하단 앱 바 중앙에 걸쳐진 형태입니다.
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    # =====================================================================
    # ##### 테마 변경 기능 정의 #####
    def toggle_theme(e): # 이벤트 객체 'e'를 인자로 받습니다.
        """페이지의 테마를 라이트 모드와 다크 모드 간에 전환합니다."""
        if page.theme_mode == ft.ThemeMode.DARK: # 현재 테마가 다크 모드이면
            page.theme_mode = ft.ThemeMode.LIGHT # 라이트 모드로 변경합니다.
        else: # 그렇지 않으면 (라이트 모드이거나 설정되지 않았으면)
            page.theme_mode = ft.ThemeMode.DARK # 다크 모드로 변경합니다.
        page.update() # 페이지 UI를 업데이트하여 테마 변경을 반영합니다.

    # =====================================================================
    # ##### 상단 앱 바 (AppBar) 정의 #####
    page.appbar = ft.AppBar(
        leading=ft.IconButton( # 앱 바의 왼쪽에 표시될 위젯 (보통 메뉴 버튼).
            icon=ft.Icons.MENU, # 메뉴 아이콘.
            # icon_color=ft.Colors.BLUE, # AppBar는 테마 색상을 따르므로, 필요시 주석 해제 후 색상 지정.
            on_click=open_drawer # 클릭 시 open_drawer 함수를 호출하여 드로어를 엽니다.
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, # 앱 바의 배경색. 테마에 따라 적절한 색상으로 표시됩니다.
        actions=[ # 앱 바의 오른쪽에 표시될 위젯(들)의 리스트 (보통 액션 버튼).
            ft.IconButton(
                icon=ft.Icons.SEARCH, # 검색 아이콘.
                # icon_color=ft.Colors.BLUE # 필요시 색상 지정.
            )
        ],
        title=ft.Text("To-do List"), # 앱 바의 중앙에 표시될 제목입니다.
    )

    # ##### 하단 앱 바 (BottomAppBar) 정의 #####
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.BLUE, # 하단 앱 바의 배경색을 파란색으로 설정합니다.
        shape=ft.NotchShape.CIRCULAR, # 플로팅 액션 버튼을 위한 홈(notch) 모양을 원형으로 설정합니다.
        content=ft.Row( # 하단 앱 바 내부에 컨트롤들을 가로로 배치하기 위한 Row 위젯입니다.
            controls=[
                # 하단 메뉴 버튼: 클릭 시 드로어를 엽니다.
                ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE, on_click=open_drawer),
                ft.Container(expand=True), # 남은 공간을 모두 차지하여 오른쪽 아이콘들을 오른쪽으로 밀어냅니다.
                ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE), # 검색 아이콘 버튼.
                ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE), # 즐겨찾기 아이콘 버튼.
                # 테마 변경 버튼: 클릭 시 toggle_theme 함수를 호출합니다.
                ft.IconButton(icon=ft.Icons.DARK_MODE, icon_color=ft.Colors.WHITE, on_click=toggle_theme)
            ]
        ),
    )

    # =====================================================================
    # =====================================================================
    # =====================================================================
    # ##### 할 일(To-do) 추가 기능 관련 UI 및 이벤트 핸들러 정의 #####

    # --- "Add" 버튼 클릭 이벤트 핸들러 ---
    def add_clicked(e): # 이벤트 객체 'e'를 인자로 받습니다.
        """새로운 할 일을 목록에 추가합니다."""
        if new_task.value: # 입력 필드(new_task)에 값이 있는 경우에만 실행합니다 (빈 값 추가 방지).
            # ft.Checkbox를 생성하여 페이지에 직접 추가합니다. 라벨은 입력 필드의 값으로 설정합니다.
            page.add(ft.Checkbox(label=new_task.value))
            new_task.value = "" # 입력 필드의 내용을 비웁니다.
            new_task.focus() # 입력 필드에 다시 포커스를 줍니다 (사용자 편의).
            page.update() # 페이지 전체 UI를 업데이트하여 새 할 일과 입력 필드 변경사항을 반영합니다.

    # --- 할 일 입력을 위한 TextField 위젯 ---
    new_task = ft.TextField(
        hint_text="What's needs to be done?", # 입력 필드에 아무것도 없을 때 표시될 안내 문구입니다.
        expand=True # Row 내에서 가능한 많은 너비를 차지하도록 합니다.
    )
    # --- "Add" 버튼 위젯 ---
    add_button = ft.ElevatedButton(
        "Add", # 버튼에 표시될 텍스트입니다.
        on_click=add_clicked # 버튼 클릭 시 add_clicked 함수를 호출합니다.
    )

    # --- 입력 필드와 "Add" 버튼을 가로로 배치하기 위한 Row 위젯 ---
    input_row = ft.Row(
        controls=[new_task, add_button], # Row 내부에 배치할 컨트롤들입니다.
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN # 컨트롤들 사이의 공간을 균등하게 배분합니다.
    )
    # 생성된 입력 UI (Row)를 페이지의 메인 컨텐츠 영역에 추가합니다.
    page.add(input_row)


# ##### 애플리케이션 실행 #####
# Flet 앱을 시작합니다. main 함수를 애플리케이션의 루트로 사용합니다.
ft.app(main)