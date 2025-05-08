__autor__ = "sychev_denis"
import json
import re


class CountryStatic:
    # Статическое свойство содержащее имя файла
    __filename = "my_countries"
    # Статическое свойство содержащее пустой словарь
    __countries = {}

    # Интерфейс цикла.
    @staticmethod
    def interface():
        print("*" * 30)
        print(f"Выбор действия:\n1 - добавление данных\n2 - удаление данных\n3 - поиск данных\n"
              f"4 - редактирование данных\n5 - просмотр данных\n6 - завершение работы")

    # Цикл по условию задачи, внесенный в статический метод
    @staticmethod
    def cycle():
        while True:
            CountryStatic.interface()
            try:
                num = int(input("Ввод: "))
                if num == 1:
                    CountryStatic.update_data(input("Введите название страны (с заглавной буквы): "),
                                              input("Введите название столицы страны (с заглавной буквы): "))
                elif num == 2:
                    CountryStatic.remove_data(input("Введите название удаляемой страны (с заглавной буквы): "))
                elif num == 3:
                    CountryStatic.search_data(input("Для поиска столицы укажите название страны(с заглавной буквы): "))
                elif num == 4:
                    CountryStatic.edit_data(input("Введите название страны (с заглавной буквы): "),
                                            input("Введите новое название столицы страны (с заглавной буквы): "))
                elif num == 5:
                    CountryStatic.show_data()
                elif num == 6:
                    print("Завершение работы")
                    break
                else:
                    print("Для корректной работы программы укажите число от 1 до 6(включительно)")
            except ValueError:
                print("Некорректный тип данных для ввода")

    # Метод создает имя файла с расширением .json
    @staticmethod
    def json_name(name):
        return f"{name}.json"

    # Метод работает с приходящей строкой названия страны/столицы, удаляет все символы кроме букв и пробела:
    # Возвращает отформатированное имя объекта(если строка не пустая) или имя по умолчанию(Default)
    @staticmethod
    def valid_obj_name(name):
        pattern = r"[a-za-яё']+[\s-]?[a-za-яё']+"
        valid_name = "".join(re.findall(pattern, name.strip().lower())).capitalize()
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

    # Метод десериализации(считывания/распаковки) данных из файла, возвращает Country.countries(словарь страна:столица).
    @staticmethod
    def load():
        try:
            with open(CountryStatic.json_name(CountryStatic.__filename)) as fr:
                CountryStatic.__countries = json.load(fr)
        except FileNotFoundError:
            with open(CountryStatic.json_name(CountryStatic.__filename), "w") as fw:
                json.dump(CountryStatic.__countries, fw, indent=2, ensure_ascii=False)

    # Метод сериализации(записи/упаковки) данных в файл, ничего не возвращает.
    @staticmethod
    def dump():
        with open(CountryStatic.json_name(CountryStatic.__filename), "w") as fw:
            json.dump(CountryStatic.__countries, fw, indent=2, ensure_ascii=False)
            print("Файл сохранен")

    # Метод добавления данных: считывает данные из файла, проверяет на наличие ключа с таким именем,
    # если вводимый ключ не существует:
    # создаст элемент словаря страна: столица, запишет данные в файл.
    @staticmethod
    def update_data(country, capital):
        valid_country = CountryStatic.valid_obj_name(country)
        valid_capital = CountryStatic.valid_obj_name(capital)
        CountryStatic.load()
        if CountryStatic.search(valid_country):
            print(f"У страны {valid_country} уже есть столица! Воспользуйтесь методом редактирования данных"
                  f"(пункт №4 в интерактивном меню)")
        else:
            CountryStatic.__countries.update({valid_country: valid_capital})
            print(
                f"В данные успешно добавлен элемент:\n{{{valid_country}: {CountryStatic.__countries[valid_country]}}}")
            CountryStatic.dump()

    # Метод редактирования данных: считывает данные из файла, проверяет на наличие ключа с таким именем,
    # если вводимый ключ существует:
    # изменит значение(столицу) для указанного ключа(страны), запишет данные в файл.
    @staticmethod
    def edit_data(country, new_capital):
        valid_country = CountryStatic.valid_obj_name(country)
        valid_new_capital = CountryStatic.valid_obj_name(new_capital)
        CountryStatic.load()
        if CountryStatic.search(valid_country):
            print(f"Для страны: {valid_country} -имя столицы: {CountryStatic.__countries[valid_country]} "
                  f"успешно изменено на {valid_new_capital}.")
            CountryStatic.__countries[valid_country] = valid_new_capital
            CountryStatic.dump()
        else:
            CountryStatic.country_not_found(valid_country)
            print(f"Пожалуйста воспользуйтесь методом добавления данных(пункт №1 в интерактивном меню).")

    # Метод удаления данных по ключу(стране): считывает данные, удаляет значение выбранного ключа, записывает данные.
    @staticmethod
    def remove_data(country):
        valid_country = CountryStatic.valid_obj_name(country)
        CountryStatic.load()
        if CountryStatic.search(valid_country):
            dict_to_print = {"страна": valid_country, "столица": CountryStatic.__countries[valid_country]}
            print(f"Элемент {dict_to_print} удален.")
            del CountryStatic.__countries[valid_country]
            CountryStatic.dump()
        else:
            CountryStatic.country_not_found(valid_country)
            print("Невозможно произвести удаление.")

    # Метод для поиска данных, принимает страну(ключ) и выводит ее столицу(значение), если такой ключ есть в словаре.
    @staticmethod
    def search_data(country):
        CountryStatic.load()
        valid_country = CountryStatic.valid_obj_name(country)
        if CountryStatic.search(valid_country):
            print(f"Элемент при считывании данных из файла найден:\n"
                  f"{{страна: {valid_country}, столица: {CountryStatic.__countries[valid_country]}}}")
        else:
            CountryStatic.country_not_found(valid_country)

    # Метод поиска ключа, считывает данные из файла, ищет принимаемое имя ключа в словаре данных:
    # возвращает булево значение
    @staticmethod
    def search(country):
        return country in CountryStatic.__countries

    # Метод просмотра всех данных из файла, считывает и выводит данные из файла, ничего не возвращает.
    @staticmethod
    def show_data():
        CountryStatic.load()
        print(f"Распакованные данные из файла:\n{CountryStatic.__countries}")

