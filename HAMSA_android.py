import flet as ft
import asyncio
import aiohttp
import jdatetime
import flet_geolocator
from urllib.parse import urlparse, parse_qs
import flet_webview as fw
from datetime import datetime, timedelta
import os
import csv

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

import numpy as np


def main(page: ft.Page):

    page.bgcolor = ft.Colors.BLUE_100

    # --------------------------------------------------
    # مسیر فایل loc.csv
    # --------------------------------------------------
    def get_loc_path():

        data_dir = os.getenv("FLET_APP_STORAGE_DATA")

        if not data_dir:
            data_dir = os.path.dirname(__file__)

        os.makedirs(data_dir, exist_ok=True)

        loc_path = os.path.join(data_dir, "loc.csv")

        # اگر loc.csv قبلاً ساخته نشده باشد،
        # فایل اولیه پروژه را کپی می‌کنیم.
        if not os.path.exists(loc_path):

            bundled_loc = os.path.join(
                os.path.dirname(__file__),
                "loc.csv"
            )

            if os.path.exists(bundled_loc):

                with open(
                    bundled_loc,
                    "r",
                    encoding="utf-8"
                ) as src:
                    content = src.read()

                with open(
                    loc_path,
                    "w",
                    encoding="utf-8"
                ) as dst:
                    dst.write(content)

            else:

                with open(
                    loc_path,
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write("lat,lon\nN,N\n")

        return loc_path

    # --------------------------------------------------
    # صفحه انتخاب مکان
    # --------------------------------------------------
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

        # --------------------------------------------------
        # گرفتن موقعیت فعلی کاربر
        # --------------------------------------------------
        async def G(event):

            geo = flet_geolocator.Geolocator()

            permission = await geo.request_permission()

            print(permission)

            position = await geo.get_current_position()

            la = position.latitude
            lo = position.longitude

            print(la)
            print(lo)

            # مسیر قابل نوشتن loc.csv
            p = get_loc_path()

            with open(
                p,
                "w",
                newline="",
                encoding="utf-8"
            ) as f:

                writer = csv.DictWriter(
                    f,
                    fieldnames=["lat", "lon"]
                )

                writer.writeheader()

                writer.writerow({
                    "lat": la,
                    "lon": lo
                })

            print(
                f"Location Updated: Lat={la}, Lon={lo}"
            )

            start()

        # --------------------------------------------------
        # انتخاب مکان از WebView
        # --------------------------------------------------
        async def M(event):

            page.clean()

            def get_url(event):

                url_str = event.data

                if "hamsa://location" in url_str:

                    try:

                        url = urlparse(url_str)

                        params = parse_qs(
                            url.query
                        )

                        if (
                            "lat" in params
                            and "lng" in params
                        ):

                            la = params["lat"][0]
                            lo = params["lng"][0]

                            # مسیر قابل نوشتن loc.csv
                            p = get_loc_path()

                            with open(
                                p,
                                "w",
                                newline="",
                                encoding="utf-8"
                            ) as f:

                                writer = csv.DictWriter(
                                    f,
                                    fieldnames=[
                                        "lat",
                                        "lon"
                                    ]
                                )

                                writer.writeheader()

                                writer.writerow({
                                    "lat": la,
                                    "lon": lo
                                })

                            print(
                                f"Location Updated: "
                                f"Lat={la}, Lon={lo}"
                            )

                            start()

                    except Exception as e:

                        print(
                            f"Error parsing URL: {e}"
                        )

            webview = fw.WebView(
                url="https://your-location-picker.com",
                on_url_change=get_url,
            )

            page.add(webview)

        page.clean()

        base_path = os.path.dirname(__file__)

        img_p = os.path.join(
            base_path,
            "hamsa_bg.png"
        )

        img = ft.Image(
            src=img_p,
            expand=True,
            fit=ft.BoxFit.COVER
        )

        ttt = ft.Text(
            "چون اولین بارتان است باید مکان بدهید",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#004080"
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

        c1 = ft.Column(
            controls=[
                ttt,
                b1,
                b2
            ],
            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
            spacing=30,
            alignment=(
                ft.MainAxisAlignment.CENTER
            ),
            expand=True
        )

        tt = ft.Container(
            content=c1,
            padding=10,
            expand=True,
            alignment=ft.alignment.Alignment(0, 0),
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.1,
                ft.Colors.BLUE
            ),
            blur=10,
            border=ft.Border.all(
                2,
                ft.Colors.with_opacity(
                    1,
                    ft.Colors.WHITE
                )
            ),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(
                duration=1000,
                curve=ft.AnimationCurve.EASE
            )
        )

        stack1 = ft.Stack(
            controls=[
                img,
                tt
            ],
            expand=True,
            fit=ft.StackFit.EXPAND
        )

        page.add(stack1)

    # --------------------------------------------------
    # صفحه اصلی برنامه
    # --------------------------------------------------
    def start():

        page.clean()

        T = {}
        W = {}
        H = {}
        P = {}

        # --------------------------------------------------
        # پیش‌بینی آب‌وهوا
        # --------------------------------------------------
        async def p_weater(event):
            
            print("حالت پیش بینی فعال شد!")

            # --------------------------------------------------
            # دریافت اطلاعات آب‌وهوا
            # --------------------------------------------------
            async def get_weather(
                lat,
                lon,
                year,
                month,
                day,
                hour
            ):

                url = (
                    "https://archive-api.open-meteo.com/v1/archive"
                )

                async with aiohttp.ClientSession() as session:

                    # ------------------------------------------
                    # دریافت اطلاعات 5 سال گذشته
                    # ------------------------------------------
                    for i in range(1, 6):

                        target_year = (
                            datetime.now().year - i
                        )

                        date_str = (
                            f"{target_year}-"
                            f"{month:02d}-"
                            f"{day:02d}"
                        )

                        params = {

                            "latitude": lat,

                            "longitude": lon,

                            "start_date": date_str,

                            "end_date": date_str,

                            "hourly": (
                                "temperature_2m,"
                                "wind_speed_10m,"
                                "relative_humidity_2m,"
                                "surface_pressure"
                            ),

                            "timezone": "auto"
                        }

                        print(
                            f"در حال دریافت دیتای سال "
                            f"{target_year}..."
                        )

                        async with session.get(
                            url,
                            params=params
                        ) as response:

                            if response.status == 200:

                                data = await response.json()

                                hourly_data = data["hourly"]

                                hour_idx = hour

                                T[i] = (
                                    hourly_data[
                                        "temperature_2m"
                                    ][hour_idx]
                                )

                                W[i] = (
                                    hourly_data[
                                        "wind_speed_10m"
                                    ][hour_idx]
                                )

                                H[i] = (
                                    hourly_data[
                                        "relative_humidity_2m"
                                    ][hour_idx]
                                )

                                P[i] = (
                                    hourly_data[
                                        "surface_pressure"
                                    ][hour_idx]
                                )

                                print("تمام شد")

                            else:

                                print(
                                    f"خطا در دریافت دیتای "
                                    f"سال {target_year}"
                                )

                    # ------------------------------------------
                    # دریافت دیتای دیروز
                    # ------------------------------------------

                    yesterday = (
                        datetime.now()
                        - timedelta(days=1)
                    )

                    target_year = yesterday.year

                    d_t = yesterday.day

                    date_str = (
                        f"{target_year}-"
                        f"{month:02d}-"
                        f"{d_t:02d}"
                    )

                    params = {

                        "latitude": lat,

                        "longitude": lon,

                        "start_date": date_str,

                        "end_date": date_str,

                        "hourly": (
                            "temperature_2m,"
                            "wind_speed_10m,"
                            "relative_humidity_2m,"
                            "surface_pressure"
                        ),

                        "timezone": "auto"
                    }

                    print(
                        f"در حال دریافت دیتای دیروز "
                        f"{target_year}..."
                    )

                    async with session.get(
                        url,
                        params=params
                    ) as response:

                        if response.status == 200:

                            data = await response.json()

                            hourly_data = data["hourly"]

                            hour_idx = hour

                            T[6] = (
                                hourly_data[
                                    "temperature_2m"
                                ][hour_idx]
                            )

                            W[6] = (
                                hourly_data[
                                    "wind_speed_10m"
                                ][hour_idx]
                            )

                            H[6] = (
                                hourly_data[
                                    "relative_humidity_2m"
                                ][hour_idx]
                            )

                            P[6] = (
                                hourly_data[
                                    "surface_pressure"
                                ][hour_idx]
                            )

                            print("تمام شد")

                        else:

                            print(
                                "خطا در دریافت دیتای دیروز"
                            )

                # --------------------------------------------------
                # ساخت دیتای آموزشی
                # --------------------------------------------------

                np.random.seed(42)

                n_samples = 500

                classes1 = [
                    "ابری",
                    "نیمه ابری",
                    "بارانی",
                    "برفی",
                    "بادی با ابر"
                ]

                classes0 = [
                    "صاف",
                    "بادی بدون ابر"
                ]

                params1 = {

                    "ابری": (
                        [18, 60, 1012, 8],
                        [3, 10, 2, 3]
                    ),

                    "نیمه ابری": (
                        [20, 45, 1013, 6],
                        [2, 8, 2, 2]
                    ),

                    "بارانی": (
                        [14, 85, 1008, 15],
                        [3, 5, 3, 5]
                    ),

                    "برفی": (
                        [2, 90, 1005, 20],
                        [2, 5, 3, 8]
                    ),

                    "بادی با ابر": (
                        [16, 55, 1009, 30],
                        [3, 10, 2, 5]
                    )
                }

                params0 = {

                    "بادی بدون ابر": (
                        [19, 25, 1011, 35],
                        [2, 5, 2, 5]
                    ),

                    "صاف": (
                        [22, 30, 1015, 5],
                        [2, 5, 2, 2]
                    )
                }

                # --------------------------------------------------
                # مدل اول
                # --------------------------------------------------

                X1 = []
                y1 = []

                for idx, (
                    name,
                    (means, stds)
                ) in enumerate(params1.items()):

                    X1.append(
                        np.random.normal(
                            loc=means,
                            scale=stds,
                            size=(n_samples, 4)
                        )
                    )

                    y1.append(
                        np.full(
                            n_samples,
                            idx
                        )
                    )

                X1 = np.vstack(X1)

                y1 = np.concatenate(y1)

                X1_train, X1_test, y1_train, y1_test = (
                    train_test_split(
                        X1,
                        y1,
                        test_size=0.2,
                        random_state=42
                    )
                )

                scaler1 = StandardScaler()

                X1_train_scaled = (
                    scaler1.fit_transform(X1_train)
                )

                X1_test_scaled = (
                    scaler1.transform(X1_test)
                )

                knn = KNeighborsClassifier(
                    n_neighbors=3
                )

                knn.fit(
                    X1_train_scaled,
                    y1_train
                )

                accuracy = knn.score(
                    X1_test_scaled,
                    y1_test
                )

                print(
                    "Accuracy model 1:",
                    accuracy
                )

                # --------------------------------------------------
                # مدل دوم
                # --------------------------------------------------

                X0 = []
                y0 = []

                for idx, (
                    name,
                    (means, stds)
                ) in enumerate(params0.items()):

                    X0.append(
                        np.random.normal(
                            loc=means,
                            scale=stds,
                            size=(n_samples, 4)
                        )
                    )

                    y0.append(
                        np.full(
                            n_samples,
                            idx
                        )
                    )

                X0 = np.vstack(X0)

                y0 = np.concatenate(y0)

                X0_train, X0_test, y0_train, y0_test = (
                    train_test_split(
                        X0,
                        y0,
                        test_size=0.2,
                        random_state=42
                    )
                )

                scaler0 = StandardScaler()

                X0_train_scaled = (
                    scaler0.fit_transform(X0_train)
                )

                X0_test_scaled = (
                    scaler0.transform(X0_test)
                )

                knn0 = KNeighborsClassifier(
                    n_neighbors=3
                )

                knn0.fit(
                    X0_train_scaled,
                    y0_train
                )

                accuracy0 = knn0.score(
                    X0_test_scaled,
                    y0_test
                )

                print(
                    "Accuracy model 0:",
                    accuracy0
                )

                # --------------------------------------------------
                # میانگین آب‌وهوا
                # --------------------------------------------------

                avg_T = (
                    sum(T[i] for i in range(1, 6))
                    / 5
                )

                avg_H = (
                    sum(H[i] for i in range(1, 6))
                    / 5
                )

                avg_W = (
                    sum(W[i] for i in range(1, 6))
                    / 5
                )

                avg_P = (
                    sum(P[i] for i in range(1, 6))
                    / 5
                )

                print("T:", T)
                print("H:", H)
                print("W:", W)
                print("P:", P)

                # --------------------------------------------------
                # پیش‌بینی مدل اول
                # --------------------------------------------------

                input_data = np.array([
                    [
                        avg_T,
                        avg_H,
                        avg_W,
                        avg_P
                    ]
                ])

                input_scaled1 = (
                    scaler1.transform(input_data)
                )

                prediction1 = knn.predict(
                    input_scaled1
                )

                v1 = classes1[
                    prediction1[0]
                ]

                # --------------------------------------------------
                # پیش‌بینی مدل دوم
                # --------------------------------------------------

                input_scaled0 = (
                    scaler0.transform(input_data)
                )

                prediction0 = knn0.predict(
                    input_scaled0
                )

                v0 = classes0[
                    prediction0[0]
                ]

                # --------------------------------------------------
                # نمایش نتیجه
                # --------------------------------------------------

                t11 = ft.Container(
                    content=ft.Text(
                        v1,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#004080"
                    ),
                    padding=10,
                    expand=1,
                    alignment=ft.alignment.Alignment(0, 0),
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(
                        0.1,
                        ft.Colors.BLUE
                    ),
                    blur=10,
                    border=ft.Border.all(
                        2,
                        ft.Colors.with_opacity(
                            1,
                            ft.Colors.WHITE
                        )
                    ),
                    offset=ft.Offset(0, 0),
                    animate_offset=ft.Animation(
                        duration=1000,
                        curve=ft.AnimationCurve.EASE
                    )
                )

                t00 = ft.Container(
                    content=ft.Text(
                        v0,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#004080"
                    ),
                    padding=10,
                    expand=1,
                    alignment=ft.alignment.Alignment(0, 0),
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(
                        0.1,
                        ft.Colors.BLUE
                    ),
                    blur=10,
                    border=ft.Border.all(
                        2,
                        ft.Colors.with_opacity(
                            1,
                            ft.Colors.WHITE
                        )
                    ),
                    offset=ft.Offset(0, 0),
                    animate_offset=ft.Animation(
                        duration=1000,
                        curve=ft.AnimationCurve.EASE
                    )
                )

                r1 = ft.Row(
                    [t00, t11],
                    vertical_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),
                    spacing=10,
                    alignment=(
                        ft.MainAxisAlignment.CENTER
                    ),
                    expand=True
                )

                t3.content = ft.Column(
                    [
                        ft.Text(
                            ":وضعیت امروز",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#004080"
                        ),

                        r1,

                        ft.Text(
                            f"{round(avg_T, 1)}C | "
                            f"{round(avg_H, 1)}% | "
                            f"{round(avg_W, 1)}km/h | "
                            f"{round(avg_P, 1)}hpa",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#004080"
                        )
                    ],

                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),

                    spacing=5,

                    alignment=(
                        ft.MainAxisAlignment.CENTER
                    ),

                    expand=True
                )

                page.update()

            # --------------------------------------------------
            # خواندن loc.csv
            # --------------------------------------------------

            loc = get_loc_path()

            try:

                with open(
                    loc,
                    "r",
                    newline="",
                    encoding="utf-8"
                ) as f:

                    reader = csv.DictReader(f)

                    row = next(
                        reader,
                        None
                    )

                if row is None:

                    weater()

                    return

                lat = row["lat"]
                lon = row["lon"]

                print(
                    "Location from CSV:"
                )

                print(
                    "Lat:",
                    lat
                )

                print(
                    "Lon:",
                    lon
                )

                # هنوز مکان تعیین نشده
                if (
                    lat == "N"
                    and lon == "N"
                ):

                    weater()

                    return

                # تبدیل مختصات به عدد
                lat = float(lat)
                lon = float(lon)

            except Exception as e:

                print(
                    "Error reading location:",
                    e
                )

                weater()

                return

            now = datetime.now()

            y = now.year
            m = now.month
            d = now.day
            h = now.hour

            await get_weather(
                lat,
                lon,
                y,
                m,
                d,
                h
            )

            page.update()

        # --------------------------------------------------
        # صفحه اصلی
        # --------------------------------------------------

        base_path = os.path.dirname(__file__)

        img_p = os.path.join(
            base_path,
            "hamsa_bg.png"
        )

        img = ft.Image(
            src=img_p,
            expand=True,
            fit=ft.BoxFit.COVER
        )

        t1 = ft.Container(
            content=ft.Text(
                "به نام خدا",
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#004080"
            ),
            padding=10,
            expand=1,
            alignment=ft.alignment.Alignment(0, 0),
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.1,
                ft.Colors.BLUE
            ),
            blur=10,
            border=ft.Border.all(
                2,
                ft.Colors.with_opacity(
                    1,
                    ft.Colors.WHITE
                )
            ),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(
                duration=1000,
                curve=ft.AnimationCurve.EASE
            )
        )

        r1 = ft.Row(
            [
                ft.Button("مکان ها"),
                ft.Button("بر اساس تاریخ"),
                ft.Button("درباره ما")
            ],
            vertical_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        t2 = ft.Container(
            content=r1,
            expand=1,
            padding=10,
            alignment=ft.alignment.Alignment(0, 0),
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.1,
                ft.Colors.BLUE
            ),
            blur=10,
            border=ft.Border.all(
                2,
                ft.Colors.with_opacity(
                    1,
                    ft.Colors.WHITE
                )
            ),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(
                duration=1000,
                curve=ft.AnimationCurve.EASE
            )
        )

        c1 = ft.Column(
            [
                ft.Text(
                    "وضعیت را به‌روزرسانی کنید",
                    size=20,
                    color="#004080"
                )
            ],
            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        t3 = ft.Container(
            content=c1,
            expand=3,
            padding=10,
            alignment=ft.alignment.Alignment(0, 0),
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.1,
                ft.Colors.BLUE
            ),
            blur=10,
            border=ft.Border.all(
                2,
                ft.Colors.with_opacity(
                    1,
                    ft.Colors.WHITE
                )
            ),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(
                duration=1000,
                curve=ft.AnimationCurve.EASE
            )
        )

        t4 = ft.Container(
            expand=4,
            padding=10,
            alignment=ft.alignment.Alignment(0, 0),
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.1,
                ft.Colors.BLUE
            ),
            blur=10,
            border=ft.Border.all(
                2,
                ft.Colors.with_opacity(
                    1,
                    ft.Colors.WHITE
                )
            ),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(
                duration=1000,
                curve=ft.AnimationCurve.EASE
            )
        )

        b1 = ft.Button(
            "به‌روزرسانی",
            on_click=p_weater,
            width=page.width,
            expand=1
        )

        col = ft.Column(
            controls=[
                t1,
                t2,
                t3,
                t4,
                b1
            ],
            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        stack = ft.Stack(
            controls=[
                img,
                col
            ],
            expand=True,
            fit=ft.StackFit.EXPAND
        )

        page.add(stack)

    # --------------------------------------------------
    # تاریخ
    # --------------------------------------------------

    date = {
        "y": None,
        "m": None,
        "d": None,
        "h": None,
        "c": None
    }

    # شروع برنامه
    start()


if __name__ == "__main__":
    ft.run(main)
