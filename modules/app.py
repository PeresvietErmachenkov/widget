import customtkinter as ctk
from PIL import Image
import modules.find_path as f_path
import modules.api as api
import time
import pynput

app_size = (200, 280)
app = ctk.CTk(fg_color = "#072038")
app.geometry(f"{app_size[0]}x{app_size[1]}+{app.winfo_screenwidth() // 2 - app_size[0] // 2}+{app.winfo_screenheight() // 2 - app_size[1] // 2}") 
app.title("Weather")

TEMP_FONT = ctk.CTkFont(size = 50)
STANDART_FONT = ctk.CTkFont(size = 20)
SMALL_FONT = ctk.CTkFont(size = 12)
STANDART_TEXT_COLOR = "#ffffff" 

TRANSPARENT = app._apply_appearance_mode(['#f2f2f2','#000001'])
app.attributes("-transparentcolor", TRANSPARENT)
app.config(background = TRANSPARENT)
background = ctk.CTkFrame(master = app, width = 200, height = 280, 
                          corner_radius = 10, border_width = 0, 
                          background_corner_colors = (None, None, None, None), bg_color = TRANSPARENT)


image = Image.open(f_path.search_path("images\\icons\\rain_icon.png"))
weather_icon = ctk.CTkLabel(
    master = background, width = 80, height = 80,
    text = " ", image = ctk.CTkImage(image, size = (80, 80)), 
    corner_radius = 0, fg_color = "transparent")

city_label = ctk.CTkLabel(
    master = background, width = 0, height = 30, 
    text = "Space", fg_color = "transparent",
    font = STANDART_FONT, text_color = STANDART_TEXT_COLOR
    )

temp_label = ctk.CTkLabel(
    master = background, width = 70, height = 70, 
    text = "0°C", fg_color = "transparent", 
    font = TEMP_FONT, text_color = STANDART_TEXT_COLOR
)

wind_label = ctk.CTkLabel(
    master = background, width = 0, height = 30,
    text = "Wind speed: 0 M/S", fg_color = "transparent",
    font = SMALL_FONT, text_color = STANDART_TEXT_COLOR
)

time_text = ctk.CTkLabel(
    master = background, width = 0, height = 30, 
    text = "9999999 hours", fg_color = "transparent", 
    font = SMALL_FONT, text_color = STANDART_TEXT_COLOR
)

move_slider = ctk.CTkLabel(
    master = background, width = 100, height = 40,
    text = " ", fg_color = "#a1a1a1", corner_radius = 10 
)

weather_text = ctk.CTkLabel(
    master = background, width = 0, height = 28, 
    text = "possible slight fallout in the form of nuclear bombs",
    fg_color = "transparent", font = STANDART_FONT, text_color = STANDART_TEXT_COLOR
)

mouse_coordinates = [0, 0]
move_click = False
blank_space = (app.winfo_width() - move_slider.cget('width')) // 2
print(f"{blank_space} \n({app.winfo_width()} - {move_slider.cget('width')}) // 2")
max_coordinates = (app.winfo_screenwidth() - app.winfo_width(), app.winfo_screenheight() - 120 - app.winfo_height())
print(max_coordinates)
definition_mouse_and_screen = (0, 0)

def check_move(x, y):
    if move_click:
        app_cors = [x + definition_mouse_and_screen[0], y + definition_mouse_and_screen[1]]
        # print(app_cors)
        if 0 > app_cors[0]:
            app_cors[0] = 0
        elif max_coordinates[0] < app_cors[0]:
            app_cors[0] = max_coordinates[0]
        # print(app_cors)
        if 0 > app_cors[1]:
            app_cors[1] = 0
        elif max_coordinates[1] < app_cors[1]:
            app_cors[1] = max_coordinates[1]
        app.geometry(f"+{app_cors[0]}+{app_cors[1]}")
        

def check_click(x, y, button, pressed):
    global move_click, definition_mouse_and_screen
    # Проверяем, находится ли курсор на слайдере перемещения в момент нажатия
    if pressed:
        if str(button) == "Button.left":
            if (app.winfo_x() + blank_space < x < app.winfo_x() + blank_space + move_slider.winfo_width() and
                app.winfo_y() + app.winfo_height() - move_slider.winfo_height() < y < app.winfo_y() + app.winfo_height()):
                definition_mouse_and_screen = (app.winfo_x() - x, app.winfo_y() - y)
                move_click = True
    else:
        move_click = False

move_listener = pynput.mouse.Listener(check_move, check_click)
move_listener.start()

def open_app():
    app.deiconify()
    app.lower()
    app.after(5000, open_app)
    
def update_temp_label():
    api_data = api.get_api_data()
    # api_data = {"a": "a"}
    if type(api_data) != dict:
        temp_label.configure(True, text = "999°C   Space")
    else:
        try:
            city = api_data["name"]
            weather_icons_variants = {"Clear": "sunny", "Clouds": "cloud", "Rain": "rain"}
            temp = round(api_data['main']['temp'] - 273.15)
            if -15 < temp < 35:
                bg_color = ("#4dbbff", "#2457ff", "#7c849c", "#facc61", "#ffa02b", "#994000")
                bg_color = bg_color[round((temp / 7 + 2) // 1)]
            elif -15 >= temp:
                bg_color = "#c7f2fc"
            elif temp >= 35: 
                bg_color = "#ff2a00"
            print(api_data['weather'][0]['main'])
            weather = api_data["weather"][0]["main"]
            icon_image = weather_icons_variants[api_data['weather'][0]['main']]
            wind_speed = round(api_data['wind']['speed'], 1)
            geolocation = f"{city}, {api_data['sys']['country']}" 
        except:
            temp = 999999
            bg_color = "#c300ff"
            geolocation = "Milky Way, Laniakea"
            wind_speed = "∞"
            icon_image = "placeholder"
            weather = "possible slight fallout in\nthe form of\nnuclear bombs"
        background.configure(True, fg_color = bg_color)
        temp_label.configure(True, text = f"{temp}ºC")
        city_label.configure(True, text = geolocation)
        wind_label.configure(True, text = f"Wind speed: {wind_speed} M/S")
        weather_icon.configure(True, image = ctk.CTkImage(Image.open(f_path.search_path(f"images\\icons\\{icon_image}_icon.png")), size = (80, 80)))
        weather_text.configure(True, text = weather)
    app.after(420000, update_temp_label)

def time_update():
    try:
        # int("a")
        time_text.configure(True, text = f"{time.strftime('%A')}, {time.strftime('%H')}:{time.strftime('%M')}, {time.strftime('%d')} {time.strftime('%B')}")
    except:
        time_text.configure(True, text = "Monday, 25:61, 32 Augustus")
    app.after(30000, time_update)

time_update()
update_temp_label()
open_app()

background.place(x = 0, y = 0)
temp_label.place(x = 75, y = 85)
city_label.place(x = 100, y = 15, anchor = ctk.CENTER)
wind_label.place(x = 100, y = 170, anchor = ctk.CENTER)
weather_icon.place(x = 3, y = 80)
time_text.place(x = 100, y = 45, anchor = ctk.CENTER)
move_slider.place(x = 100, y = 270, anchor = ctk.CENTER)
weather_text.place(x = 100, y = 220, anchor = ctk.CENTER)

app.overrideredirect(1)
app.mainloop()