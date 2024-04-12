import flet as ft

class ErrorAlert(ft.UserControl):
    def __init__(self, title_text, main_text, page):
        super().__init__()
        self.title = title_text
        self.main = main_text
        self.page = page

    def build(self):
        self.dlg = ft.AlertDialog(
            title=ft.Text(self.title),
            content=ft.Text(self.main),
            actions=[
                ft.TextButton("OK", on_click=self.close)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        return self.dlg

    def close(self, e):
        self.dlg.open = False
        self.page.update()

