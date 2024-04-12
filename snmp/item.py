import threading
import time
import flet as ft
from snmp.snmp import SNMPClient
from hurry.filesize import size, si
from utils import kilobyte_to_gigabyte


class MachineInfo(ft.UserControl):
    def __init__(self, ip, alias):
        super().__init__()
        self.ip = ip
        self.client = SNMPClient(ip)
        self.alias = alias
        self.counter = 0

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(target=self.update_values, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.running = False

    def update_values(self):
        while self.running:
            self.cpu.value = f"{self.client.get_cpu_usage_1min()}, {self.client.get_cpu_usage_5min()}, {self.client.get_cpu_usage_10min()}"
            self.temp.value = "{:.2f} °C".format(int(self.client.get_cpu_temperature()) / 1000)

            self.counter += 1
            if self.counter == 5:
                network_in = int(self.client.get_internet_traffic_in())
                network_out = int(self.client.get_internet_traffic_out())

                self.network_in.value = "{}/s".format(size( (network_in - self.network_in_prev) / 5 ))
                self.network_out.value = "{}/s".format(size( (network_out - self.network_out_prev) / 5 ))

                self.network_in_prev = network_in
                self.network_out_prev = network_out
                self.counter = 0

            total_ram = int(self.client.get_total_ram())
            avail_ram = int(self.client.get_avail_ram())
            cached_ram = int(self.client.get_cached_ram())
            used_ram = total_ram - avail_ram - cached_ram

            self.total_ram.value = "{:.2f}G".format(kilobyte_to_gigabyte(total_ram))
            self.avail_ram.value = "{:.2f}G".format(kilobyte_to_gigabyte(avail_ram))
            self.used_ram.value = "{:.2f}G".format(kilobyte_to_gigabyte(used_ram))
            self.cached_ram.value = "{:.2f}G".format(kilobyte_to_gigabyte(cached_ram))

            self.update()
            time.sleep(1)

    def build(self):
        self.cpu = ft.Text()
        self.temp = ft.Text()
        self.network_in = ft.Text()
        self.network_out = ft.Text()
        self.total_ram = ft.Text()
        self.avail_ram = ft.Text()
        self.cached_ram = ft.Text()
        self.shared_ram = ft.Text()
        self.used_ram = ft.Text()
        self.cpu_count = ft.Text()

        self.network_in_prev = int(self.client.get_internet_traffic_in())
        self.network_out_prev = int(self.client.get_internet_traffic_out())
        self.cpu_count.value = self.client.get_cpu_count()

        cpu_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("CPU count:", weight=ft.FontWeight.BOLD),
                            self.cpu_count
                        ]
                    ),
                    ft.Text("CPU average usage:", weight=ft.FontWeight.BOLD),
                    self.cpu
                ]),
            padding=10,
            margin = 0,
            height = 100,
            alignment=ft.alignment.center,
        )

        network_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.ARROW_DOWNWARD, size=20),
                            self.network_in
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.ARROW_UPWARD, size=20),
                            self.network_out
                        ]
                    )
                ]),
            padding=10,
            margin = 0,
            height = 100,
            alignment=ft.alignment.center,
        )

        ram_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                        ft.Text("RAM", weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls =[
                                ft.Text("total"),
                                self.total_ram,
                            ],
                        ),
                        ft.Row(
                            controls =[
                            ft.Text("avail"),
                            self.avail_ram,
                            ],
                        ),
                        ft.Row(
                            controls =[
                            ft.Text("cached"),
                            self.cached_ram
                            ],
                        ),
                        ft.Row(
                            controls =[
                            ft.Text("used:"),
                            self.used_ram
                            ],
                        )
                        ]
                    )
                ]
                ),
            padding=10,
            margin = 0,
            height = 150,
            alignment=ft.alignment.center,
        )

        temp_container = ft.Container(
            content = ft.Column(
                controls=[
                    ft.Text("CPU temperature:", weight=ft.FontWeight.BOLD),
                    self.temp
                ]),
            padding=10,
            margin = 0,
            height = 150,
            alignment=ft.alignment.center,
        )

        main_content = ft.Column(
            width=300,
            controls=[
                ft.Text(value="{} / {}".format(self.ip, self.alias), size=20, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        cpu_container,
                        network_container
                    ],
                ),
                ft.Container(
                    bgcolor=ft.colors.BLACK26,
                    border_radius=ft.border_radius.all(30),
                    height=1,
                    alignment=ft.alignment.center,
                    width=300
                ),
                ft.Row(
                    controls=[
                        temp_container,
                        ram_container
                    ],
                )
            ],
            spacing=0,
        )

        return ft.Container(
            content=main_content,
            border=ft.border.all(1, ft.colors.BLACK12),
            bgcolor=ft.colors.BLUE_GREY_100,
            padding=10,
            border_radius=10
        )