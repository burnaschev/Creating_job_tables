import time
from typing import Any

import psycopg2
import requests


def get_companies(api_key: str) -> list[dict[str, Any]]:
    """Получение списка работодателей и их вакансий с платформы HeadHunter"""
    companies = []
    for page in range(10):
        time.sleep(1)
        params = {
            'per_page': 100,
            "page": page
        }
        response = requests.get(api_key, params=params)
        items_json = [item for item in response.json()['items'] if int(item['open_vacancies']) > 0]
        companies.extend(items_json)
    return companies[0:10]


def sorted_companies_vacancy(company_list: list) -> list[dict[str, Any]]:
    """Получение списка вакансий работодателей"""
    params = {
        'per_page': 100,
        "page": 0
    }
    for company in company_list:
        time.sleep(1)
        response = requests.get(company['vacancies_url'], params=params)
        items_json = response.json()
        company['vacancies'] = items_json['items']
    return company_list


def create_database(database_name: str, params: dict):
    """Создание базы данных"""
    conn = psycopg2.connect(dbname={database_name}, **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.execute("""
                CREATE TABLE companies (
                    company_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL
                )
            """)

    cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        company_id int REFERENCES companies(company_id),
                        title VARCHAR(255) NOT NULL,
                        salary_to INTEGER,
                        salary_from INTEGER,
                        url TEXT NOT NULL 
                    )
                """)

    cur.close()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    pass
