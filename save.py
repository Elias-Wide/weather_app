import os

with open("weather.txt", "w", encoding="utf-8") as file:
    for file_in_dir in os.listdir("src/assets/weather_icons/"):
        file.write(f"{file_in_dir}+\n".replace(".svg", ""))
    