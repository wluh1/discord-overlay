import json

class Settings():
    def __init__(self):
        self._data = {}

        self.set_opacity(0.3)
        self.set_program_name("Discord")
        self.set_frame_pos(10, 10)
        self.set_image_width(220)
        self.set_image_height(200)
        self.set_auto_height(True)

        self._load_data_from_file()


    def _load_data_from_file(self):
        try:
            with open("data.json", "r") as data_file:
                data = json.loads(data_file.read())
                self._data = data
        except Exception:
            print("No file to load data from.")


    def set_frame_pos(self, x, y):
        self._data["frame_pos"] = (x, y)

    def get_frame_pos(self):
        return self._data["frame_pos"]


    def get_program_name(self):
        return self._data["program_name"]

    def set_program_name(self, program_name):
        self._data["program_name"] = program_name


    def set_image_width(self, width):
        self._data["width"] = width

    def get_image_width(self):
        return self._data["width"]

    def set_image_height(self, height):
        if height < 10:
            height = 10
        self._data["height"] = height

    def get_image_height(self):
        return self._data["height"]

    def get_opacity(self):
        return float(self._data["opacity"]) / 100

    def set_opacity(self, opacity):
        self._data["opacity"] = opacity

    def set_auto_height(self, auto_height):
        self._data["auto_height"] = auto_height

    def get_auto_height(self):
        return self._data["auto_height"]

    def save_data(self):
        with open("data.json", "w") as data_file:
            json.dump(self._data, data_file)


current_settings = Settings()
