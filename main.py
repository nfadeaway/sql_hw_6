import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import *


def find_publisher(publisher_key):
    if publisher_key.isdigit():
        q = session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Book.id == Stock.id_book). \
            join(Publisher, Publisher.id == Book.id_publisher).filter(Publisher.id == publisher_key)
    else:
        q = session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Book.id == Stock.id_book). \
            join(Publisher, Publisher.id == Book.id_publisher).filter(Publisher.name == publisher_key)
    # print(q)
    print(f'Магазины, продающие книги издателя {publisher_key}')
    for s in q.all():
        print(s.id, s.name)


if __name__ == '__main__':

    database_management_system = 'postgresql'
    db_login = 'postgres'
    db_password = '55555'
    db_server_adress = 'localhost'
    db_server_port = '5432'
    db_name = 'bookshop'
    engine = sqlalchemy.create_engine(f'{database_management_system}://{db_login}:{db_password}@{db_server_adress}:'
                                      f'{db_server_port}/{db_name}')
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for row in range(len(data)):
        if data[row]['model'] == 'publisher':
            session.add(Publisher(id=data[row]['pk'], name=data[row]['fields']['name']))
        elif data[row]['model'] == 'book':
            session.add(Book(id=data[row]['pk'], title=data[row]['fields']['title'],
                             id_publisher=data[row]['fields']['id_publisher']))
        elif data[row]['model'] == 'shop':
            session.add(Shop(id=data[row]['pk'], name=data[row]['fields']['name']))
        elif data[row]['model'] == 'stock':
            session.add(Stock(id=data[row]['pk'], id_shop=data[row]['fields']['id_shop'],
                              id_book=data[row]['fields']['id_book'], count=data[row]['fields']['count']))
        elif data[row]['model'] == 'sale':
            session.add(Sale(id=data[row]['pk'], price=data[row]['fields']['price'],
                             date_sale=data[row]['fields']['date_sale'], count=data[row]['fields']['count'],
                             id_stock=data[row]['fields']['id_stock']))
    session.commit()

    find_publisher(input('Введите идентификатор издателя или его название: '))

    session.close()
