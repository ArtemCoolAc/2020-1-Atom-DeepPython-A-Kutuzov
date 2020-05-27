import json


class Field:
    """ Базовый класс всех типов полей. Каждому полю требуется начальное значение """

    def __init__(self, initial_value=None):
        self.initial_value = initial_value

    def validate(self, value):
        """ Проверка валидности значения для поля """
        return True


class StringField(Field):
    """ Поле строка. Можно проверить на длину строки """

    def __init__(self, initial_value=None, maximum_length=None):
        super().__init__(initial_value)

        self.maximum_length = maximum_length

    def validate(self, value):
        """ Проверка на валидность поля строки """
        if super().validate(value):
            return (value is None) or (isinstance(value, str) and self._validate_length(value))
        else:
            return False

    def _validate_length(self, value):
        """ Проверка что длина строки не больше максимальной """
        return (self.maximum_length is None) or (len(value) <= self.maximum_length)


class IntField(Field):
    """ Поле целое число и опциональная """

    def __init__(self, initial_value=None, maximum_value=None):
        super().__init__(initial_value)

        self.maximum_value = maximum_value

    def validate(self, value):
        """ Проверка валидности целого числа и вхождения в диапазон (-oo;max] """
        if super().validate(value):
            return (value is None) or (isinstance(value, int) and self._validate_value(value))
        else:
            return False

    def _validate_value(self, value):
        """ Check if integer falls in desired range """
        return (self.maximum_value is None) or (value <= self.maximum_value)


class ORMMeta(type):
    """ Метакласс нашей ОРМ """

    def __new__(self, name, bases, namespace):
        fields = {
            name: field
            for name, field in namespace.items()
            if isinstance(field, Field)
        }

        new_namespace = namespace.copy()

        # Remove fields from class variables
        for name in fields.keys():
            del new_namespace[name]

        new_namespace['_fields'] = fields

        return super().__new__(self, name, bases, new_namespace)


class ORMBase(metaclass=ORMMeta):
    """ Пользовательский интерфейс для базового класса ОРМ """

    def __init__(self, json_input=None):
        for name, field in self._fields.items():
            setattr(self, name, field.initial_value)

        # If there is a JSON supplied, we'll parse it
        if json_input is not None:
            json_value = json.loads(json_input)

            if not isinstance(json_value, dict):
                raise RuntimeError("Заявленный JSON должен быть словарем")

            for key, value in json_value.items():
                setattr(self, key, value)

    def __setattr__(self, key, value):
        """ Сеттер """
        if key in self._fields:
            if self._fields[key].validate(value):
                super().__setattr__(key, value)
            else:
                raise AttributeError('Неправильное значение "{}" для поля "{}"'.format(value, key))
        else:
            raise AttributeError('Неизвестное поле "{}"'.format(key))

    def to_json(self):
        """ Конвертация объекта в JSON """
        new_dictionary = {}

        for name in self._fields.keys():
            new_dictionary[name] = getattr(self, name)

        return json.dumps(new_dictionary, ensure_ascii=False)


class ORMDatabase:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.objects = dict()

    def read_all(self, name):
        class_name = str(name).split('.')[1][:-2]
        return self.objects[class_name]

    def create(self, object):
        """ Создание таблицы при её отсутствии и добавление объекта в любом случае"""
        print(object.__class__.__name__)
        mapping = {'StringField': 'VARCHAR', 'IntField': 'INTEGER'}
        command = f"""CREATE TABLE IF NOT EXISTS public.{object.__class__.__name__} (
        {", ".join([f"{key} {mapping[value.__class__.__name__]}" for key, value in object._fields.items()])}
        )"""
        print(command)
        self.cursor.execute(command)
        self.connection.commit()
        self.insert(object)

    def insert(self, obj):
        """ Вставка данных"""
        self.cursor.execute(f"SELECT max(id) "
                            f"FROM public.{obj.__class__.__name__.lower()}")
        table_id = self.cursor.fetchone()[0]
        if table_id is None:
            table_id = 0
        table_id += 1
        obj.id = table_id
        command = f"""INSERT INTO public.{obj.__class__.__name__} 
        values  ('{"', '".join([str(value) for value in obj.__dict__.values()])}');"""
        print(command)
        self.cursor.execute(command)
        self.connection.commit()

    def delete(self, name, **conditions):
        """ Удаление данных """
        class_name = str(name).split('.')[1][:-2]
        command = f'''DELETE FROM public.{class_name} 
        WHERE ( {" AND ".join([f"{key}='{value}'" for key, value in conditions.items()])} )'''
        self.cursor.execute(command)
        self.connection.commit()

    def get(self, name, **conditions):
        """ Получение первого совпадающего с условием значения """
        class_name = str(name).split('.')[1][:-2]
        command = f'''SELECT * FROM public.{class_name} 
        WHERE ( {" AND ".join([f"{key}='{value}'" for key, value in conditions.items()])} )'''
        print(f'Команда на единичиный селект: {command}')
        self.cursor.execute(command)
        self.connection.commit()
        query_result = self.cursor.fetchall()
        return [name(*ret) for ret in query_result]

    def all(self, name):
        """ Вывод всех данных """
        class_name = str(name).split('.')[1][:-2]
        command = f'SELECT * FROM public.{class_name}'
        print(command)
        self.cursor.execute(command)
        self.connection.commit()
        data = self.cursor.fetchall()
        return [name(*ret) for ret in data]

    def drop(self, name):
        """ Удаление таблицы """
        class_name = str(name).split('.')[1][:-2]
        command = f'DROP TABLE public.{class_name.lower()};'
        self.cursor.execute(command)
        self.connection.commit()

    def update(self, name, update_data, **columns_where):
        """ Обновление таблицы (с названиями столбцов) """
        class_name = str(name).split('.')[1][:-2]
        columns, data = [list(update_data.keys()), list(update_data.values())]
        command = f"""UPDATE public.{class_name} 
        SET {", ".join([f"{column} = '{value}'" for column, value in update_data.items()])} 
        WHERE {" AND ".join([f"{column_where} = '{value_where}'" for column_where, value_where in columns_where.items()])}"""
        print(f'Команда для обновления: {command}')
        self.cursor.execute(command)
        self.connection.commit()


def assign_values(obj, *args, **kwargs):
    if len(args) == len(obj.__dict__.keys()):
        for value, field in zip(args, obj.__dict__.keys()):
            obj.__dict__[field] = value
    for field, value in kwargs.items():
        if field in obj.__dict__.keys():
            obj.__dict__[field] = value
