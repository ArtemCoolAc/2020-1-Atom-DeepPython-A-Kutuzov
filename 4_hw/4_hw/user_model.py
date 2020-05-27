from my_orm import ORMBase, ORMDatabase, IntField, StringField, assign_values
from my_local_settings import connect_to_database


class User(ORMBase):
    """Некоторый пользователь"""
    id = IntField(initial_value=0, maximum_value=2 ** 32)
    name = StringField(maximum_length=200)
    surname = StringField(maximum_length=200)
    height = IntField(maximum_value=300)
    year_born = IntField(maximum_value=2020)

    def __init__(self, *args, **kwargs):
        super().__init__()
        assign_values(self, *args, **kwargs)
        self.__class__.__name__ = 'User'

    def __str__(self):
        return self.to_json()


if __name__ == '__main__':
    A = User(name='Артем', surname='Кутузов', height=190, year_born=1998)
    # print(A)

    connection = connect_to_database()

    B = ORMDatabase(connection)
    print(B)
    C = B.get(User, surname='Кутузов')
    for elem in C:
        print(elem)

    B.update(User, {'name': 'Денис', 'surname': 'Косяков', 'height': 184, 'year_born': 1986}, id=5)
    G = User(name='Гена', surname='Фараонов', height=178, year_born=1992)
    B.create(G)

    E = B.all(User)
    for el in E:
        print(el)
