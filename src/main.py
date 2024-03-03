from src.db_func import create_database, create_table_company, create_table_vacancy, insert_company, insert_vacancy
from src.employer_db import DBManager
from src.api_func import get_employers, get_vacancies

# Список компаний
list_employer = ['Скиллтеллект', 'e-Comet', 'CommerceChamp', 'EasyDev', 'АпТрейдер (UpTrader)', 'ZennoLab',
                 'Программные Системы', 'Байсейл', 'Intelligent Analytics', 'Россювелирторг']

# Настройки подключения  для создания базы данных
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'qwerty',
    'host': 'localhost',
    'port': '5432'
}

# Настройки подключения к базе данных hh.ru
db_hhru = {
    'dbname': 'hhru',
    'user': 'postgres',
    'password': 'qwerty',
    'host': 'localhost',
    'port': '5432'
}


def main():
    """ Основная функция программы
    """
    list_vacancies = []
    list_employers = []
    for name_employer in list_employer:
        list_employers += (get_employers(name_employer))
        list_vacancies += (get_vacancies(list_employers[-1]['vacancies_url']))

    create_database('hhru', db_config)
    create_table_company(db_hhru, 'companies')
    create_table_vacancy(db_hhru, 'vacancies')
    insert_company(db_hhru, list_employers, 'companies')
    insert_vacancy(db_hhru, list_vacancies, 'vacancies')

    db = DBManager(**db_hhru)

    print(db.get_companies_and_vacancies_count())
    print(db.get_all_vacancies())
    print(db.get_avg_salary())
    print(db.get_vacancies_with_higher_salary())
    print(db.get_vacancies_with_keyword('BackEnd'))


if __name__ == '__main__':
    main()
