# main.py
import flet as ft
from pages.to_do_list import to_do_list


def main(page: ft.Page):
    to_do_list(page)


if __name__ == "__main__":
    ft.app(main)
