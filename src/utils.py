import time
from typing import Any

import psycopg2
import requests

API_HH_COMPANIES = 'https://api.hh.ru/employers'
TIME = 0.1
DB_NAME = "data"


def get_companies() -> list[dict[str, Any]]:
    """Получение списка работодателей и их вакансий с платформы HeadHunter"""
    companies = []
    for page in range(10):
        time.sleep(TIME)
        params = {
            'per_page': 100,
            "page": page
        }
        response = requests.get(API_HH_COMPANIES, params=params)
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
        time.sleep(TIME)
        response = requests.get(company['vacancies_url'], params=params)
        items_json = response.json()
        company['vacancies'] = items_json['items']
    return company_list


def create_database(params: dict) -> None:
    """Создание базы данных"""
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cur.execute(f"CREATE DATABASE {DB_NAME}")
    conn.close()

    conn = psycopg2.connect(dbname=DB_NAME, **params)
    with conn.cursor() as cur:
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
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], params: dict) -> None:
    """Добавление информаций по вакансиям в таблицу"""
    conn = psycopg2.connect(dbname=DB_NAME, **params)

    with conn.cursor() as cur:
        for company in data:
            cur.execute(
                """
                INSERT INTO companies (title)
                VALUES (%s)
                RETURNING company_id
                """,
                (company['name'],))
            company_id = int(cur.fetchone()[0])
            for vacancy in company['vacancies']:
                cur.execute("""
                INSERT INTO vacancies (company_id, title, salary_to, salary_from, url)
                VALUES (%s, %s, %s, %s, %s)""",
                            (company_id, vacancy['name'],
                             int(vacancy['salary']['from']) if vacancy['salary']['from'] else None,
                             int(vacancy['salary']['to']) if vacancy['salary']['to'] else None,
                             vacancy['alternate_url']))
    conn.commit()
    conn.close()
