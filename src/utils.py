from typing import Any

import psycopg2
import requests

API_HH_COMPANIES = 'https://api.hh.ru/employers/'
DB_NAME = "data"


def get_companies(companies: list) -> list[dict[str, Any]]:
    """Получение списка работодателей и их вакансий с платформы HeadHunter"""
    companies_list = []
    for company in companies:
        url = f'{API_HH_COMPANIES}{company}'
        companies_response = requests.get(url).json()
        vacancy_response = requests.get(companies_response['vacancies_url']).json()
        companies_list.append({
            'company': companies_response,
            'vacancies': vacancy_response['items']
        })

    return companies_list


def filter_salary(salary):
    """Применяем фильтр для заработной платы"""
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return round((salary['from'] + salary['to']) / 2)
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None


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
                            salary INTEGER,
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
                (company['company']['name'],))
            company_id = int(cur.fetchone()[0])
            for vacancy in company['vacancies']:
                salary = filter_salary(vacancy['salary'])
                cur.execute("""
                INSERT INTO vacancies (company_id, title, salary, url)
                VALUES (%s, %s, %s, %s)""",
                            (company_id, vacancy['name'], salary,
                             vacancy['alternate_url']))
    conn.commit()
    conn.close()
