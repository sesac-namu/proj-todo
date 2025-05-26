import flet as ft

class MyBox(ft.UserControl):
    def build(self):
        # self.page가 여기서부터 사용 가능
        if self.page.platform == "android":
            icon = ft.icons.ANDROID
        else:
            icon = ft.icons.LAPTOP
        print("🚨 build")
        return ft.Icon(name=icon)

    def did_mount(self):
        print("🟢 페이지에 추가됨!")

    def will_unmount(self):
        print("🔴 페이지에서 제거되기 전!")

    def before_update(self):
        print("🟡 업데이트 직전 (여기서 update() 호출 X)")
