import re
import flet as ft
from item import MachineInfo
from dialog_window import ErrorAlert
from utils import check_valid_ip

class App(ft.UserControl):
    def __init__(self, path, page):
        super().__init__()
        self.path_to_config = path
        self.machines = self.read_config(self.path_to_config)
        self.page = page

    def build(self):
        self.add_item_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, height=35, on_click=self.add_item, bgcolor=ft.colors.BLUE
        )
        self.ip_input = ft.TextField(hint_text="ip", width=200, height=35, text_align=ft.TextAlign.CENTER, text_size=14)
        self.alias_input = ft.TextField(hint_text="alias", width=200, height=35, text_align=ft.TextAlign.CENTER, text_size=14)

        self.items = ft.Row(
            wrap=True,
            spacing=10,
            run_spacing=10,
            controls=self.machines,
            width=1600,
        )

        self.new_input = ft.Row(
            width=600,
            spacing=10,
            controls=[self.ip_input, self.alias_input, self.add_item_button],
        )

        return ft.Column(controls=[self.new_input, self.items])

    def add_item(self, e):
        if not check_valid_ip(self.ip_input.value):
            self.open_error_dialog(e, "Invalid IP", "Please enter valid IP adress")
            return

        new_machine = MachineInfo(self.ip_input.value, self.alias_input.value)
        if not new_machine.client.check_connection():
            self.open_error_dialog(e, "Error connection", "Please check your machine connection")
            return

        self.machines.append(new_machine)
        with open(self.path_to_config, 'a') as file:
            file.write(f"\n{new_machine.ip} {new_machine.alias}\n")
        self.update()

    def open_error_dialog(self, e, err_text, main_text):
        self.err_dialog = ft.AlertDialog(
            title=ft.Text(err_text),
            content=ft.Text(main_text),
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.err_dialog
        self.err_dialog.open = True
        self.page.update()

    def read_config(self, file_path):
        machines = []
        with open(file_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 1:
                    ip = values[0]
                    alias = ""
                elif len(values) == 2:
                    ip = values[0]
                    alias = values[1]
                else:
                    continue
                if not check_valid_ip(ip):
                    continue
                machine = MachineInfo(ip, alias)
                machines.append(machine)
        return machines

def main(page: ft.Page):

    page.add(
        App("config.txt", page)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)