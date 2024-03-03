import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """  Создает базу данных
    """
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.commit()
    conn.close()


def create_table_company(params: dict, table_name: str = 'companies') -> None:
    """  Создает таблицу для хранения информации о компаниях
    """
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
            DROP TABLE IF EXISTS {table_name};
            CREATE TABLE IF NOT EXISTS {table_name} (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                quantity_vacancies INTEGER NOT NULL
            );
            """)
            conn.commit()


def create_table_vacancy(params: dict, table_name: str = 'vacancies') -> None:
    """  Создает таблицу для хранения информации о вакансиях
    """
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
            DROP TABLE IF EXISTS {table_name};
            CREATE TABLE IF NOT EXISTS {table_name} (
                company_id INTEGER REFERENCES companies(company_id),
                vacancy_name VARCHAR(100) NOT NULL,
                url VARCHAR(100) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER
            );
            """)
            conn.commit()


def insert_company(params: dict, employers: list[dict], table_name: str = 'companies') -> None:
    """ Добавляет информацию о компании в таблицу
    """
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            for company in employers:
                cur.execute(
                    f"INSERT INTO {table_name} (company_id, company_name, quantity_vacancies)"
                    f"VALUES (%s, %s, %s)",
                    (company['company_id'], company['company_name'], company['quantity_vacancies']))
            conn.commit()


def insert_vacancy(params: dict, vacancies: list[dict], table_name: str = 'vacancies') -> None:
    """ Добавляет информацию о вакансии в таблицу
    """
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            for company in vacancies:
                cur.execute(
                    f"INSERT INTO {table_name} (company_id, vacancy_name, url, salary_from, salary_to)"
                    f"VALUES (%s, %s, %s, %s, %s)",
                    (company['company_id'], company['vacancy_name'], company['vacancy_url'],
                     company['salary_from'], company['salary_to']))
            conn.commit()
