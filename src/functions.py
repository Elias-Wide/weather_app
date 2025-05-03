from mtranslate import translate


def get_city_name_en(city_name: str):
    return translate(city_name, "en", "auto")
