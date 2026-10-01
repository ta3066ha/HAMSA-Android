import flet as ft

import asyncio

import aiohttp

import jdatetime

import flet_geolocator

from urllib.parse import urlparse, parse_qs

import flet_webview as fw

from datetime import datetime, timedelta

import os

import pandas as pd

import csv

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import classification_report

import numpy as np

**def** main(page: ft.Page):

    page.bgcolor = ft.Colors.BLUE_100

    **def** weater():

        **def** back(event):

            start()

        **def** date_change(event):

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

        **async** **def** G(event):

            geo = flet_geolocator.Geolocator()

            permission = await geo.request_permission()

            print(permission)

            position = await geo.get_current_position()

            la = position.latitude

            lo = position.longitude

            print(la)

            print(lo)

            base_path = os.path.dirname(\_\_file\_\_)

            p = os.path.join(base_path, "loc.csv")

            with open(p, 'w', newline='', encoding='utf-8') as f:

                writer = csv.DictWriter(f, fieldnames=["lat", "lon"])

                writer.writeheader()

                writer.writerow({"lat": la, "lon": lo})      

                print(**f**"Location Updated: Lat={la}, Lon={lo}")

            start() 

        **async** **def** M(event):

            page.clean()

            **def** get_url(event):

                url_str = event.data

                if "hamsa://location" in url_str:

                    try:

                        url = urlparse(url_str)

                        params = parse_qs(url.query)

                        if "lat" in params and "lng" in params:

                            la = params["lat"][0] *# مقدار رو به صورت رشته بگیر (نیاز به تبدیل به float نیست مگر برای محاسبات)*

                            lo = params["lng"][0]

                            base_path = os.path.dirname(\_\_file\_\_)

                            p = os.path.join(base_path, "loc.csv")



                            *# نوشتن مستقیم در فایل (بدون دردسر پانداس)*

                            with open(p, 'w', newline='', encoding='utf-8') as f:

                                writer = csv.DictWriter(f, fieldnames=["lat", "lon"])

                                writer.writeheader()

                                writer.writerow({"lat": la, "lon": lo})

                            print(**f**"Location Updated: Lat={la}, Lon={lo}")

                            *# حالا می‌تونی به صفحه اصلی برگردی*

                            start() 

                    except Exception as e:

                        print(**f**"Error parsing URL: {e}")

            webview = fw\.WebView(

                url="[https://your-location-picker.com](https://your-location-picker.com)", *# آدرسی که لوکیشن رو برمی‌گردونه*

                on_url_change=get_url,

            )

            page.add(webview)

        page.clean()



        base_path = os.path.dirname(\_\_file\_\_)

        img_p = os.path.join(base_path, "hamsa_bg.png")

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

            controls=[ttt,b1,b2],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            spacing=30,

            alignment=ft.MainAxisAlignment.CENTER,

            expand=True

        )

        tt = ft.Container(

            content=c1,

            *#width=page.width,*

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

            controls=[img, tt],

            expand=True,

            fit=ft.StackFit.EXPAND

        )

        page.add(stack1)

    **def** start():

        page.clean()

        T = {}

        W = {}

        H = {}

        P = {}

        **async** **def** p_weater(event):

            print("حالت پیش بینی فعال شد!")

            **async** **def** get_weather(lat, lon, year, month, day, hour):

                url = "[https://archive-api.open-meteo.com/v1/archive](https://archive-api.open-meteo.com/v1/archive)"

                async with aiohttp.ClientSession() as session:

                    for i in range(1, 6):

                        target_year = datetime.now().year - i *# این i باعث میشه هر بار سال عوض بشه*

                        date_str = **f**"{target_year}-{month**:02d**}-{day**:02d**}"

                        params = {

                            "latitude": lat,

                            "longitude": lon,

                            "start_date": date_str,

                            "end_date": date_str, *# برای یک روز خاص*

                            "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m,surface_pressure",

                            "timezone": "auto"

                        }

                        print(**f**"در حال دریافت دیتای سال {target_year}...")

                        async with session.get(url, params=params) as response:

                            if response.status == 200:

                                data = await response.json()

                                *# استخراج دیتای ساعتِ مورد نظر (مثلا ساعت 12)*

                                *# در دیتای آرشیو، لیست hourly ساده‌تر است*

                                hourly_data = data["hourly"]

                                hour_idx = hour *# فرض بر اینکه دیتای ساعت دقیق را برمیگرداند*

                                *# ذخیره در یک دیکشنری*

                                T[i] = hourly_data["temperature_2m"][hour_idx],

                                W[i] = hourly_data["wind_speed_10m"][hour_idx],

                                H[i] = hourly_data["relative_humidity_2m"][hour_idx],

                                P[i] = hourly_data["surface_pressure"][hour_idx]

                                print("تمام شد")

                            else:

                                print(**f**"خطا در دریافت دیتای سال {target_year}")



                    for i in range(6,7):

                        target_year = datetime.now().year *# این i باعث میشه هر بار سال عوض بشه*

                        now1 = datetime.now() 

                        *# ۲. حالا عملیات تفریق را روی شیءِ زمان انجام می‌دهیم (این خودش ماه و سال را هم هوشمندانه مدیریت می‌کند)*

                        yesterday = now1 - timedelta(days=1)

                        *# ۳. حالا از این شیء جدید، هر چیزی بخواهی استخراج می‌کنی*

                        d_t = yesterday.day

                        date_str = **f**"{target_year}-{month**:02d**}-{d_t**:02d**}"

                        params = {

                            "latitude": lat,

                            "longitude": lon,

                            "start_date": date_str,

                            "end_date": date_str, *# برای یک روز خاص*

                            "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m,surface_pressure",

                            "timezone": "auto"

                        }

                        print(**f**"در حال دریافت دیتای دیروز {target_year}...")

                        async with session.get(url, params=params) as response:

                            if response.status == 200:

                                data = await response.json()

                                *# استخراج دیتای ساعتِ مورد نظر (مثلا ساعت 12)*

                                *# در دیتای آرشیو، لیست hourly ساده‌تر است*

                                hourly_data = data["hourly"]

                                hour_idx = hour *# فرض بر اینکه دیتای ساعت دقیق را برمیگرداند*

                                *# ذخیره در یک دیکشنری*

                                T[i] = hourly_data["temperature_2m"][hour_idx],

                                W[i] = hourly_data["wind_speed_10m"][hour_idx],

                                H[i] = hourly_data["relative_humidity_2m"][hour_idx],

                                P[i] = hourly_data["surface_pressure"][hour_idx]

                                print("تمام شد")





                            else:

                                print(**f**"خطا در دریافت دیتای سال {target_year}")

                np.random.seed(42)

                n_samples = 500

                classes1 = ["ابری", "نیمه ابری", "بارانی", "برفی", "بادی با ابر"]

                classes0 = ["صاف", "بادی بدون ابر"]

                params1 = {

                    "ابری":         ([18, 60, 1012, 8], [3, 10, 2, 3]),

                    "نیمه ابری":    ([20, 45, 1013, 6], [2, 8, 2, 2]),

                    "بارانی":       ([14, 85, 1008, 15], [3, 5, 3, 5]),

                    "برفی":         ([2, 90, 1005, 20], [2, 5, 3, 8]),

                    "بادی با ابر":   ([16, 55, 1009, 30], [3, 10, 2, 5]),

                }

                params0 = {

                    "بادی بدون ابر": ([19, 25, 1011, 35], [2, 5, 2, 5]),

                    "صاف":          ([22, 30, 1015, 5], [2, 5, 2, 2])

                }

                X1 = []

                y1 = []

                for idx, (name, (means, stds)) in enumerate(params1.items()):

                    X1.append(np.random.normal(loc=means, scale=stds, size=(n_samples, 4)))

                    y1.append(np.full(n_samples, idx))

                X1 = np.vstack(X1)

                y1 = np.concatenate(y1)

                X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

                scaler = StandardScaler()

                X1_train_scaled = scaler.fit_transform(X1_train)

                X1_test_scaled = scaler.transform(X1_test)

                knn = KNeighborsClassifier(n_neighbors=3)

                knn.fit(X1_train_scaled, y1_train)

                accuracy = knn.score(X1_test_scaled, y1_test)

                X0 = []

                y0 = []

                for idx, (name, (means, stds)) in enumerate(params0.items()):

                    X0.append(np.random.normal(loc=means, scale=stds, size=(n_samples, 4)))

                    y0.append(np.full(n_samples, idx))

                X0 = np.vstack(X0)

                y0 = np.concatenate(y0)

                X0_train, X0_test, y0_train, y0_test = train_test_split(X0, y0, test_size=0.2, random_state=42)

                scaler = StandardScaler()

                X0_train_scaled = scaler.fit_transform(X0_train)

                X0_test_scaled = scaler.transform(X0_test)

                knn0 = KNeighborsClassifier(n_neighbors=3)

                knn0.fit(X0_train_scaled, y0_train)

                print("P:", P)

                prediction1 = knn.predict([[

                    sum(T[i][0] for i in range(1, 6)) / 5,

                    sum(H[i][0] for i in range(1, 6)) / 5,

                    sum(W[i][0] for i in range(1, 6)) / 5,

                    sum(P[i] for i in range(1, 6)) / 5

                ]])

                v1 = classes1[prediction1[0]]

                prediction0 = knn0.predict([[

                    sum(T[i][0] for i in range(1, 6)) / 5,

                    sum(H[i][0] for i in range(1, 6)) / 5,

                    sum(W[i][0] for i in range(1, 6)) / 5,

                    sum(P[i] for i in range(1, 6)) / 5

                ]])

                v0 = classes0[prediction0[0]]

                t11 = ft.Container(

                    content=ft.Text(

                        v1,

                        size=20,

                        weight=ft.FontWeight.BOLD,

                        color="#004080"

                    ),

                    *#width=page.width,*

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

                    *#width=page.width,*

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

                    vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    spacing=10,

                    alignment=ft.MainAxisAlignment.CENTER,

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

                            **f**"{sum(T[i][0] for i in range(1, 6)) / 5}C | {sum(H[i][0] for i in range(1, 6)) / 5}% | {sum(W[i][0] for i in range(1, 6)) / 5}km/h | {sum(T[i][0] for i in range(1, 6)) / 5}hpa",

                            size=20,

                            weight=ft.FontWeight.BOLD,

                            color="#004080"

                        )

                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    spacing=5,

                    alignment=ft.MainAxisAlignment.CENTER,

                    expand=True

                )

                page.update()

            base_path = os.path.dirname(\_\_file\_\_)

            loc = os.path.join(base_path, "loc.csv")

            df = pd.read_csv(loc)

            print(df)

            if df.loc[0, "lon"] == "N" and df.loc[0, "lat"] == "N":

                weater()

            else:

                now = datetime.now()

                y = now\.year

                m = now\.month

                d = now\.day

                h = now\.hour

                lon = df.loc[0, "lon"]

                lat = df.loc[0, "lat"]

                await get_weather(lat,lon,y,m,d,h)



            page.update()

        base_path = os.path.dirname(\_\_file\_\_)

        img_p = os.path.join(base_path, "hamsa_bg.png")

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

            *#width=page.width,*

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

            [ft.Button(

                "مکان ها"

            ),

            ft.Button(

                "بر اساس تاریخ"

            ),

            ft.Button(

                "درباره ما"

            )],

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            spacing=10,

            alignment=ft.MainAxisAlignment.CENTER,

            expand=True

        )

        t2 = ft.Container(

            content=r1,

            *#width=page.width,*

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

                ft.Text("وضعیت را به‌روزرسانی کنید", size=20, color="#004080")

            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            spacing=0,

            alignment=ft.MainAxisAlignment.CENTER,

            expand=True

        )

        t3 = ft.Container(

            content=c1,

            *#width=page.width,*

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

            *#width=page.width,*

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

            controls=[t1,t2,t3,t4,b1],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            spacing=8,

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

        "d": None,

        "h": None,

        "c": None

    }

    start()



if \_\_name\_\_ == "\_\_main\_\_":

    ft.run(main)

