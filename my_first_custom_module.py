__autor__ = "sychev_denis"
# Работа с экземплярами класса: возможность передачи данных/создания свойства self.__data по умолчанию.
# Передача имени для json файла в self.__filename/создание свойства по умолчанию.
import json
import re


class Country:
    # Инициализатор вызывает setter для self.__data и self.__filename(если они приходят при создании экземпляра класса).
    def __init__(self, data=None, filename=None):
        self.data = {} if data is None else data
        self.filename = "default_file_name" if filename is None else filename

    # Метод __call__ позволяет поместить массивный цикл внутрь класса и обратиться к экземпляру как к функции.
    def __call__(self):
        while True:
            Country.interface()
            try:
                num = int(input("Ввод: "))
                if num == 1:
                    self.update_data(input("Введите название страны: "),
                                     input("Введите название столицы страны: "))
                elif num == 2:
                    self.remove_data(input("Введите название удаляемой страны: "))
                elif num == 3:
                    self.search_data(input("Для поиска столицы укажите название страны: "))
                elif num == 4:
                    self.edit_data(input("Введите название страны: "),
                                   input("Введите новое название столицы страны: "))
                elif num == 5:
                    self.show_data()
                elif num == 6:
                    print("Завершение работы")
                    break
                else:
                    print("Для корректной работы программы укажите число от 1 до 6(включительно)")
            except ValueError:
                print("Некорректный тип данных для ввода")

    # Интерфейс цикла.
    @staticmethod
    def interface():
        print("*" * 30)
        print(f"Выбор действия:\n1 - добавление данных\n2 - удаление данных\n3 - поиск данных\n"
              f"4 - редактирование данных\n5 - просмотр данных\n6 - завершение работы")

    # Метод для проверки типа передаваемых данных(если передаваемые данные преобразуются к dict, их возвращает функция,
    # если передаваемые данные не преобразуются к dict- возвращается {}).
    @staticmethod
    def check_data(data):
        try:
            data_to_file = dict(data)
        except (ValueError, TypeError):
            data_to_file = {}
            print("Некорректный тип данных для data.\nДля data установлено значение по умолчанию({}).")
        return data_to_file

    # Метод проверки приходящих значений(имени файла).
    # Возвращает булево значение
    @staticmethod
    def check_string(string):
        return isinstance(string, str)

    # Метод проверки строковых значений для имени файла(проверяет на пустую строку, удаляет лишние символы)
    # Возвращает отредактированную строку/значение по умолчанию, если передана пустая строка.
    @staticmethod
    def valid_filename(filename):
        if len(filename) != 0:
            pattern = r"[\w]+"
            valid_filename = "".join(re.findall(pattern, filename.lower()))
        else:
            print("Имя filename не может быть пустой строкой.\n"
                  "Для filename установлено значение по умолчанию(default_file_name).")
            valid_filename = "default_file_name"
        return valid_filename

    # Метод работает с приходящей строкой названия страны/столицы, удаляет все символы кроме букв и пробела:
    # Возвращает отформатированное имя объекта(если строка не пустая) или имя по умолчанию(Default)
    @staticmethod
    def valid_obj_name(name):
        pattern = r"[a-za-яё']+[\s-]?[a-za-яё']+"
        valid_name = "".join(re.findall(pattern, name.strip().lower())).title()
        if len(valid_name) != 0:
            valid_obj_name = valid_name
        else:
            print("Некорректное название: имя не может быть пустым или состоять только из цифр или спецсимволов!\n"
                  "для указанного объекта задано имя по умолчанию(Default)")
            valid_obj_name = "Default"
        return valid_obj_name

    # Метод выводит сообщение, вызывается если метод search возвращает False
    @staticmethod
    def country_not_found(country):
        print(f"Страна: {country} в считанных из файла данных не найдена.")

    # Геттер self.__data
    @property
    def data(self):
        return self.__data

    # Сеттер self.__data
    @data.setter
    def data(self, data):
        self.__data = Country.check_data(data)

    # Геттер self.__filename
    @property
    def filename(self):
        return self.__filename

    # Сеттер self.__filename
    @filename.setter
    def filename(self, filename):
        if Country.check_string(filename):
            self.__filename = Country.valid_filename(filename)
        else:
            print("Некорректный тип данных для filename.\n"
                  "Для filename установлено значение по умолчанию(default_file_name).")
            self.__filename = "default_file_name"

    # Метод генерации имени файла.json
    def json_name(self):
        return f"{self.__filename}.json"

    # Метод десериализации(считывания/распаковки) данных из файла:
    # возвращает данные в self.data(словарь страна:столица) текущего экземпляра класса.
    def load(self):
        try:
            with open(self.json_name()) as fr:
                self.__data = json.load(fr)
        except FileNotFoundError:
            with open(self.json_name(), "w") as fw:
                json.dump(self.__data, fw, indent=2, ensure_ascii=False)

    # Метод сериализации(записи/упаковки) данных в файл:
    # ничего не возвращает, записывает данные в файл из self.data.
    def dump(self):
        with open(self.json_name(), "w") as fw:
            json.dump(self.__data, fw, indent=2, ensure_ascii=False)
            print("Файл сохранен")

    # Метод добавления данных: считывает данные из файла, проверяет на наличие ключа с таким именем,
    # если вводимый ключ не существует:
    # создаст элемент словаря страна: столица, запишет данные в файл.
    def update_data(self, country, capital):
        self.load()
        valid_country = Country.valid_obj_name(country)
        valid_capital = Country.valid_obj_name(capital)
        if self.search(valid_country):
            print(f"У страны {valid_country} уже есть столица! Воспользуйтесь методом редактирования данных"
                  f"(пункт №4 в интерактивном меню)")
        else:
            self.data.update({valid_country: valid_capital})
            print(f"В данные успешно добавлен элемент:\n{{{valid_country}: {self.__data[valid_country]}}}")
            self.dump()

    # Метод редактирования данных: считывает данные из файла, проверяет на наличие ключа с таким именем,
    # если вводимый ключ существует:
    # изменит значение(столицу) для указанного ключа(страны), запишет данные в файл.
    def edit_data(self, country, new_capital):
        self.load()
        valid_country = Country.valid_obj_name(country)
        valid_new_capital = Country.valid_obj_name(new_capital)
        if self.search(valid_country):
            print(f"Для страны: {valid_country} -имя столицы: {self.__data[valid_country]} "
                  f"успешно изменено на {valid_new_capital}.")
            self.__data[valid_country] = valid_new_capital
            self.dump()
        else:
            Country.country_not_found(valid_country)
            print(f"Пожалуйста воспользуйтесь методом добавления данных(пункт №1 в интерактивном меню).")

    # Метод удаления данных по ключу(стране): считывает данные, удаляет значение выбранного ключа, записывает данные.
    def remove_data(self, country):
        self.load()
        valid_country = Country.valid_obj_name(country)
        if self.search(valid_country):
            dict_to_print = {"страна": valid_country, "столица": self.__data[valid_country]}
            print(f"Элемент {dict_to_print} удален.")
            del self.__data[valid_country]
            self.dump()
        else:
            Country.country_not_found(valid_country)
            print("Невозможно произвести удаление.")

    # Метод для поиска данных, принимает страну(ключ) и выводит ее столицу(значение), если такой ключ есть в словаре.
    def search_data(self, country):
        self.load()
        valid_country = Country.valid_obj_name(country)
        if self.search(valid_country):
            print(f"Элемент при считывании данных из файла найден:\n"
                  f"{{страна: {valid_country}, столица: {self.__data[valid_country]}}}")
        else:
            Country.country_not_found(valid_country)

    # Метод поиска ключа(страны), возвращает булево значение
    def search(self, country):
        return country in self.__data

    # Метод просмотра всех данных из файла, считывает и выводит данные из файла, ничего не возвращает.
    def show_data(self):
        self.load()
        print(f"Распакованные данные из файла:\n{self.__data}")
