import flet as ft
import asyncio
import jdatetime
import flet_geolocator
from urllib.parse import urlparse, parse_qs
import flet_webview as fw


def main(page: ft.Page):
    page.bgcolor = ft.Colors.BLUE_100

    def weater():

        def back(event):
            start()

        def date_change(event):
            y = event.control.value.year
            m = event.control.value.month
            d = event.control.value.day

            date["y"] = y
            date["m"] = m
            date["d"] = d

            shamsi_date = jdatetime.date.fromgregorian(
                year=y,
                month=m,
                day=d
            )

            m_j = shamsi_date.month

            if m_j <= 3:
                f = "b"
            elif m_j <= 6:
                f = "t"
            elif m_j <= 9:
                f = "p"
            else:
                f = "z"

            date["f"] = f

            print(shamsi_date)
            print(date)

        async def G(event):
            geo = flet_geolocator.Geolocator()

            permission = await geo.request_permission()
            print(permission)

            position = await geo.get_current_position()

            la = position.latitude
            lo = position.longitude

            print(la)
            print(lo)

            date["la"] = la
            date["lo"] = lo

            print(date)

        async def M(event):
            page.clean()

            def get_url(event):
                print("URL:", event.data)

                url = urlparse(event.data)
                params = parse_qs(url.query)

                lat = float(params["lat"][0])
                lng = float(params["lng"][0])

                date["la"] = lat
                date["lo"] = lng

                print(date)

            webview = fw.WebView(
                expand=True,
                on_url_change=get_url
            )

            webview.load_html("map.html")

            img = ft.Image(
                src="ZajmszIkFo7iL30NxhjwsKjpxA4-9sBmupM1QzmiS92f5PyoDg (1).png",
                expand=True,
                fit=ft.BoxFit.COVER
            )

            page.add(webview)

        page.clean()

        date_picker = ft.DatePicker(
            locale=ft.Locale("fa", "IR"),
            on_change=date_change
        )

        page.show_dialog(date_picker)

        img = ft.Image(
            src="ZajmszIkFo7iL30NxhjwsKjpxA4-9sBmupM1QzmiS92f5PyoDg (1).png",
            expand=True,
            fit=ft.BoxFit.COVER
        )

        b1 = ft.Button(
            "موقعیت من",
            width=200,
            bgcolor=ft.Colors.WHITE,
            on_click=G
        )

        b2 = ft.Button(
            "انتخاب مکان",
            width=200,
            bgcolor=ft.Colors.WHITE,
            on_click=M
        )

        r1 = ft.Row(
            controls=[b2, b1],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        stack1 = ft.Stack(
            controls=[img, r1],
            expand=True,
            fit=ft.StackFit.EXPAND
        )

        page.add(stack1)

    def start():
        page.clean()

        async def p_weater(event):
            t1.content.value = "به صفحه شروع پیش بینی آمدید"

            col.controls.remove(b1)

            print("حالت پیش بینی فعال شد!")

            t1.offset = ft.Offset(0, -4)
            t1.update()

            page.update()

            await asyncio.sleep(2)

            weater()

        img = ft.Image(
            src="ZajmszIkFo7iL30NxhjwsKjpxA4-9sBmupM1QzmiS92f5PyoDg (1).png",
            expand=True,
            fit=ft.BoxFit.COVER
        )

        t1 = ft.Container(
            content=ft.Text(
                "سلام به همسا (هوش مصنوعی سنجش آب و هوا) خوش آمدید",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE
            ),
            padding=20,
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.1,
                ft.Colors.BLUE
            ),
            blur=10,
            border=ft.Border.all(
                2,
                ft.Colors.with_opacity(
                    0.1,
                    ft.Colors.BLUE
                )
            ),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(
                duration=1000,
                curve=ft.AnimationCurve.EASE
            )
        )

        b1 = ft.Button(
            "شروع پیش بینی",
            on_click=p_weater,
            width=200
        )

        col = ft.Column(
            controls=[t1, b1],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        stack = ft.Stack(
            controls=[img, col],
            expand=True,
            fit=ft.StackFit.EXPAND
        )

        page.add(stack)

    date = {
        "y": None,
        "m": None,
        "d": None
    }

    start()


if __name__ == "__main__":
    ft.run(main)