from typing import List, Dict, Any

import requests


def get_employers(title: str) -> list[dict[str, Any]]:
    """ Получает список всех компаний и количество вакансий у каждой компании
    """
    url = "https://api.hh.ru/employers"
    params = {
        'text': title,
        'only_with_vacancies': True,
        'page': 0,
        'per_page': 100,
        'locale': 'RU',
        'host': 'hh.ru'
    }
    response = requests.get(url, params=params)
    repos = response.json()

    employers = []
    for repo in repos['items']:
        if repo['name'] == title:
            employers.append({
                'company_id': repo['id'],
                'company_name': repo['name'],
                'quantity_vacancies': repo['open_vacancies'],
                'vacancies_url': repo['vacancies_url']
            })
    return employers


def get_vacancies(url: str) -> list[dict[str, Any]]:
    """  Получает список всех вакансий с указанием названия компании,
         названия вакансии, зарплаты и ссылки на вакансию
    """
    response = requests.get(url)
    repos = response.json()

    vacancies = []
    for repo in repos['items']:
        if repo['salary'] is not None:
            vacancies.append({
                'company_id': repo['employer']['id'],
                'vacancy_name': repo['name'],
                'vacancy_url': repo['alternate_url'],
                'salary_from': repo['salary']['from'],
                'salary_to': repo['salary']['to']
            })
        else:
            vacancies.append({
                'company_id': repo['employer']['id'],
                'vacancy_name': repo['name'],
                'vacancy_url': repo['alternate_url'],
                'salary_from': None,
                'salary_to': None
            })
    return vacancies
