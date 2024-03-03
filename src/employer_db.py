import psycopg2


class DBManager:
    """ Класс для работы с базой данных.
    """

    def __init__(self, dbname: str, user: str, password: str,
                 host: str = 'localhost', port: int = 5432,
                 table_companies: str = 'companies',
                 table_vacancies: str = 'vacancies') -> None:
        """ Инициализирует подключение к базе данных
        """
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.table_companies = table_companies
        self.table_vacancies = table_vacancies

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """ Получает список всех компаний и количество вакансий у каждой компании
        """
        with self.conn:
            self.cur.execute(f"SELECT company_name, quantity_vacancies FROM {self.table_companies}")
            return self.cur.fetchall()

    def get_all_vacancies(self) -> list[tuple[str, str, int or None, int or None, str]]:
        """  Получает список всех вакансий с указанием названия компании,
             названия вакансии, зарплаты и ссылки на вакансию
        """
        with self.conn:
            self.cur.execute(f""" SELECT company_name, vacancy_name, salary_from, salary_to, url
                                  FROM {self.table_companies}
                                  RIGHT JOIN {self.table_vacancies} USING(company_id)
                                  """)
            return self.cur.fetchall()

    def get_avg_salary(self) -> list[tuple[float, float]]:
        """ Получает среднюю зарплату по вакансиям
        """
        with self.conn:
            self.cur.execute(f""" SELECT AVG(salary_from), AVG(salary_to)
                                  FROM {self.table_vacancies}
                                  WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                                  """)
            return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self) -> list[tuple[str, int, int]]:
        """  Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        with self.conn:
            self.cur.execute(f""" SELECT vacancy_name, salary_from, salary_to
                                  FROM {self.table_vacancies}
                                  WHERE salary_from > (SELECT AVG(salary_from) FROM {self.table_vacancies} 
                                  WHERE salary_to > (SELECT AVG(salary_to) FROM {self.table_vacancies}
                                  WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL))
                                  """)
            return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[str]]:
        """  Получает список всех вакансий, в названии которых содержатся переданные ключевые слова
        """
        with self.conn:
            self.cur.execute(f""" SELECT vacancy_name
                                  FROM {self.table_vacancies}
                                  WHERE LOWER(vacancy_name) LIKE LOWER('%{keyword}%')
                                  """)
            return self.cur.fetchall()
