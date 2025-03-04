import customtkinter as ctk
from PIL import Image, ImageTk
from weather_object import Weather
from planes_object import Planes

FONT_STYLE = 'Microsoft Sans Serif'
TEXT_COLOR = 'white'

def main():
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue") 

window = ctk.CTk()
window.geometry("800x600+500+400")
window.title("RC Weather")
window.resizable(width=False, height=False)
window.iconbitmap('icons/app_icon.ico')

def city_validation_and_destroy_popup():
    global city_name, weather
    city_name = entry.get()
    
    try:
        if weather := Weather(city_name):
            popup.destroy() 
    except:
        error_message = ctk.CTkLabel(popup, text="Not a valid place", font=(FONT_STYLE, 14), text_color=TEXT_COLOR, bg_color='red')
        error_message.pack(pady=10)
        error_message.after(2000, error_message.destroy)
        


### CITY CHOICE POPUP ###
popup = ctk.CTkToplevel(window)
popup.geometry("400x300+500+400")
popup.title("Choose City")
popup.resizable(width=False, height=False)

# Login background
background_image = Image.open("icons/bg_login.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = ctk.CTkLabel(popup, image=background_photo, text="")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Choose place
city = ctk.CTkLabel(popup, text="Choose your flight area (City, District )", font=(FONT_STYLE, 14), text_color=TEXT_COLOR, bg_color='#309eff')
city.pack(pady=10)

entry = ctk.CTkEntry(popup, bg_color='#309eff')
entry.pack(pady=10)

# Choose city button
submit_button = ctk.CTkButton(popup, text="Choose", font=(FONT_STYLE, 14), border_color='white', border_width=1, bg_color='#309eff', command=city_validation_and_destroy_popup)
submit_button.pack(pady=10)
popup.grab_set()
window.wait_window(popup)


planes = Planes(city_name)
    
# Setting the background of the app
background_image = Image.open("icons/bg_app.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = ctk.CTkLabel(window, image=background_photo, text="")
background_label.place(x=0, y=0, relwidth=1, relheight=1)


###CURRENT WEATHER###
#Weather data
current_weather = weather.get_weather_current()

# Flight conditions
label_current_conditions = ctk.CTkLabel(window, text=planes.flight_circumstances(1, current_or_hourly="current"), font=(FONT_STYLE, 20), text_color=TEXT_COLOR, bg_color='#309eff')
label_current_conditions.place(x=410, y=10)
# Icon
icon_image = Image.open(f"icons/{(current_weather[0][5])}.png")
icon_photo = ctk.CTkImage(icon_image, size=(150, 150))
icon_label = ctk.CTkLabel(window, image=icon_photo, fg_color='#309eff', text="")
icon_label.place(x=50, y=25)
# Position
label_position = ctk.CTkLabel(window, text=weather.get_position(), font=(FONT_STYLE, 20), text_color=TEXT_COLOR, bg_color='#309eff')
label_position.place(x=20, y=10)
# Temp
label = ctk.CTkLabel(window, text=(current_weather[0][0]), font=(FONT_STYLE, 40), text_color=TEXT_COLOR, bg_color='#309eff')
label.place(x=75, y=140)
# Wind
label = ctk.CTkLabel(window, text=f"Wind: {(current_weather[0][1])} km/h", font=(FONT_STYLE, 22), text_color=TEXT_COLOR, bg_color='#309eff')
label.place(x=75, y=185)
# Direction
label = ctk.CTkLabel(window, text=f"Direction: {(current_weather[0][2])}", font=(FONT_STYLE, 22), text_color=TEXT_COLOR, bg_color='#309eff')
label.place(x=75, y=210)
# Description
label = ctk.CTkLabel(window, text=f"{(current_weather[0][4]).capitalize()}", font=(FONT_STYLE, 22), text_color=TEXT_COLOR, bg_color='#309eff')
label.place(x=75, y=235)


# Hourly weather data
hourly_weather = weather.get_weather_hourly(9)

### 3 hours forecast ###
label = ctk.CTkLabel(window, text="3-hour forecast", font=(FONT_STYLE, 16), text_color='black', bg_color='#ffb10b')
label.place(x=80, y=320)
icon_image = Image.open(f"icons/{hourly_weather[2][5]}.png")
icon_photo = ctk.CTkImage(icon_image, size=(90, 90))
icon_label = ctk.CTkLabel(window, image=icon_photo, fg_color='#282828', text="")
icon_label.place(x=90, y=360)
label = ctk.CTkLabel(window, text=(hourly_weather[2][0]), font=(FONT_STYLE, 25), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=100, y=430)
label = ctk.CTkLabel(window, text=f"Wind: {hourly_weather[2][1]} km/h", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=90, y=465)
label = ctk.CTkLabel(window, text=f"Direction: {hourly_weather[2][2]}", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=90, y=485)
label = ctk.CTkLabel(window, text=f"{(hourly_weather[2][4]).capitalize()}", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=90, y=505)
label_3h_forecast = ctk.CTkLabel(window, text=planes.flight_circumstances(1,"hourly", 3), font=(FONT_STYLE, 16), text_color='black', bg_color='#ffb10b')
label_3h_forecast.place(x=40, y=555)



### 6 hours forecast ###
label = ctk.CTkLabel(window, text="6-hour forecast", font=(FONT_STYLE, 16), text_color='black', bg_color='#ffb10b')
label.place(x=340, y=320)
icon_image = Image.open(f"icons/{hourly_weather[5][5]}.png")
icon_photo = ctk.CTkImage(icon_image, size=(90, 90))
icon_label = ctk.CTkLabel(window, image=icon_photo, fg_color='#282828', text="")
icon_label.place(x=350, y=360)
label = ctk.CTkLabel(window, text=(hourly_weather[5][0]), font=(FONT_STYLE, 25), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=360, y=430)
label = ctk.CTkLabel(window, text=f"Wind: {hourly_weather[5][1]} km/h", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=350, y=465)
label = ctk.CTkLabel(window, text=f"Direction: {hourly_weather[5][2]}", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=350, y=485)
label = ctk.CTkLabel(window, text=f"{(hourly_weather[5][4]).capitalize()}", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=350, y=505)
label_6h_forecast = ctk.CTkLabel(window, text=planes.flight_circumstances(1,"hourly", 6), font=(FONT_STYLE, 16), text_color='black', bg_color='#ffb10b')
label_6h_forecast.place(x=300, y=555)                                      

### 9 hours forecast ###
label = ctk.CTkLabel(window, text="9-hour forecast", font=(FONT_STYLE, 16), text_color='black', bg_color='#ffb10b')
label.place(x=610, y=320)
icon_image = Image.open(f"icons/{hourly_weather[8][5]}.png") # [8] = 9. hour in hourly prediction
icon_photo = ctk.CTkImage(icon_image, size=(90, 90))
icon_label = ctk.CTkLabel(window, image=icon_photo, fg_color='#282828', text="")
icon_label.place(x=620, y=360)
label = ctk.CTkLabel(window, text=(hourly_weather[8][0]), font=(FONT_STYLE, 25), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=630, y=430)
label = ctk.CTkLabel(window, text=f"Wind: {hourly_weather[8][1]} km/h", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=620, y=465)
label = ctk.CTkLabel(window, text=f"Direction: {hourly_weather[8][2]}", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=620, y=485)
label = ctk.CTkLabel(window, text=f"{(hourly_weather[8][4]).capitalize()}", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color='#282828')
label.place(x=620, y=505)
label_9h_forecast = ctk.CTkLabel(window, text=planes.flight_circumstances(1,"hourly", 9), font=(FONT_STYLE, 16), text_color='black', bg_color='#ffb10b')
label_9h_forecast.place(x=570, y=555)

# List of planes & select plane

def select_plane():
    selected_plane = combo_box.get() 
    selected_plane = selected_plane.split(" | ")
    global plane_id
    plane_id = int(selected_plane[0]) # <<<< important
    selected_plane = selected_plane[1]
    refresh_combo_box()
    result_label.configure(text=f"Plane: {selected_plane}")
    
    label_current_conditions.configure(text=f"{planes.flight_circumstances(plane_id,"current")}")
    label_3h_forecast.configure(text=f"{planes.flight_circumstances(plane_id, "hourly", 3)}")
    label_6h_forecast.configure(text=f"{planes.flight_circumstances(plane_id,"hourly", 6)}")
    label_9h_forecast.configure(text=f"{planes.flight_circumstances(plane_id,"hourly", 9)}")
    
# Actual plane
result_label = ctk.CTkLabel(window, text=(f"Plane: {planes.plane_name(1)}"), font=(FONT_STYLE, 25), text_color="#282828", bg_color="#74beff")
result_label.place(x=500, y=55)    

# Planes list
combo_box = ctk.CTkComboBox(window, values=planes.get_planes_list(), width=290, font=(FONT_STYLE, 16), text_color=TEXT_COLOR, fg_color='#309eff', border_color='white', dropdown_fg_color="#282828", dropdown_text_color=TEXT_COLOR, bg_color="#74beff")
combo_box.place(x=500, y=120, )


# Others
label = ctk.CTkLabel(window, text="Other planes:", font=(FONT_STYLE, 16), text_color=TEXT_COLOR, bg_color="#74beff")
label.place(x=500, y=90)

# Choose plane button
select_button = ctk.CTkButton(window, text="Choose", font=(FONT_STYLE, 16), command=select_plane, bg_color="#74beff", fg_color="#309eff", text_color=TEXT_COLOR, border_width=2, border_color='white')
select_button.place(x=500, y=160)



# ComboBox refresh
def refresh_combo_box():
    combo_box.configure(values=planes.get_planes_list())

# Add new plane popup
def open_add_plane_popup():
    add_popup = ctk.CTkToplevel(window)
    add_popup.geometry("350x200+600+500")
    add_popup.title("Add Plane")
    add_popup.attributes("-topmost", True)
    add_popup.configure(background_image='icons/bg_login_2.jpg')
    label = ctk.CTkLabel(add_popup, text="Enter name,weight with comma (e.g., supercub,50 ):", font=(FONT_STYLE, 14))
    label.pack(pady=10)

    entry = ctk.CTkEntry(add_popup)
    entry.pack(pady=10)

    def add_plane():
        plane_and_weight = entry.get()
        if planes.add_plane(plane_and_weight) == "Successfully added":
            add_popup.destroy()
            refresh_combo_box()
            success_message = ctk.CTkLabel(window, text="Successfully added", font=(FONT_STYLE, 14), text_color=TEXT_COLOR, bg_color='green')
            success_message.place(x=510, y=200)
            success_message.after(3000, success_message.destroy)
        else:
            error_message = ctk.CTkLabel(add_popup, text=planes.add_plane(plane_and_weight), font=(FONT_STYLE, 14), text_color=TEXT_COLOR, bg_color='red')
            error_message.pack(pady=10)
            error_message.after(2000, error_message.destroy)

    add_button = ctk.CTkButton(add_popup, text="Add Plane", command=add_plane)
    add_button.pack(pady=10)

# Remove plane popup
def open_remove_plane_popup():
    remove_popup = ctk.CTkToplevel(window)
    remove_popup.geometry("350x200+600+500")
    remove_popup.title("Remove Plane")
    remove_popup.attributes("-topmost", True)
    
    label = ctk.CTkLabel(remove_popup, text="Enter plane ID or name to remove: ", font=(FONT_STYLE, 14))
    label.pack(pady=10)

    entry = ctk.CTkEntry(remove_popup)
    entry.pack(pady=10)

    def remove_plane():
        id_or_name = entry.get()
        planes.remove_plane(id_or_name)
        remove_popup.destroy()
        refresh_combo_box()
        success_message = ctk.CTkLabel(window, text="List refreshed", font=(FONT_STYLE, 14), text_color=TEXT_COLOR, bg_color='green')
        success_message.place(x=510, y=200)
        success_message.after(3000, success_message.destroy)

    remove_button = ctk.CTkButton(remove_popup, text="Remove Plane", command=remove_plane)
    remove_button.pack(pady=10)

# Add plane button
add_plane_button = ctk.CTkButton(window, text="Add Plane", font=(FONT_STYLE, 16), command=open_add_plane_popup, bg_color="#74beff", fg_color="#309eff", text_color=TEXT_COLOR, border_width=2, border_color='white')
add_plane_button.place(x=650, y=160)

# Remove plane button
remove_plane_button = ctk.CTkButton(window, text="Remove Plane", font=(FONT_STYLE, 16), command=open_remove_plane_popup, bg_color="#74beff", fg_color="#309eff", text_color=TEXT_COLOR, border_width=2, border_color='white')
remove_plane_button.place(x=650, y=200)

window.mainloop()


if __name__ == '__main__':
    main()