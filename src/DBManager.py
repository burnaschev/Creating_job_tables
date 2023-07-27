import psycopg2
from src.config import config


class DBManager:
    """Класс для работы с базой данных вакансий."""
    def __init__(self, data_base, params=config()):
        self.data_base = data_base
        self.params = params

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            con = psycopg2.connect(dbname=self.data_base, **self.params)
            with con.cursor() as cur:
                cur.execute("""SELECT companies.company_title, COUNT(vacancies.vacancy_id) as vacancies_count
                FROM companies
                JOIN vacancies USING(company_id)
                GROUP BY companies.company_title; 
                            """)
                rows = cur.fetchall()
                return rows
        finally:
            con.close()

    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        try:
            con = psycopg2.connect(dbname=self.data_base, **self.params)
            with con.cursor() as cur:
                cur.execute("""SELECT companies.company_title, vacancies.vacancy_title, vacancies.salary, vacancies.url
                FROM companies
                JOIN vacancies USING(company_id)
                ORDER BY vacancies.salary DESC;
                """)
                rows = cur.fetchall()
                return rows
        finally:
            con.close()

    def get_avg_salary(self) -> list[tuple]:
        """Получает среднюю зарплату по вакансиям."""
        try:
            con = psycopg2.connect(dbname=self.data_base, **self.params)
            with con.cursor() as cur:
                cur.execute("""SELECT ROUND(AVG(vacancies.salary)) AS average_salary
                FROM vacancies;
                """)
                rows = cur.fetchall()
                return rows
        finally:
            con.close()

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        try:
            con = psycopg2.connect(dbname=self.data_base, **self.params)
            with con.cursor() as cur:
                cur.execute("""SELECT vacancies.* FROM vacancies
                WHERE vacancies.salary > (SELECT ROUND(AVG(vacancies.salary)) FROM vacancies)
                ORDER BY vacancies.salary DESC;
                """)
                rows = cur.fetchall()
                return rows
        finally:
            con.close()

    def get_vacancies_with_keyword(self, vacancy_name: str) -> list[tuple]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        try:
            con = psycopg2.connect(dbname=self.data_base, **self.params)
            with con.cursor() as cur:
                cur.execute(f"""SELECT * 
                FROM vacancies
                WHERE lower(vacancy_title) LIKE '%{vacancy_name.lower()}%'
                OR lower(vacancy_title) LIKE '%{vacancy_name.lower()}'
                OR lower(vacancy_title) LIKE '{vacancy_name.lower()}%'
                """)
                rows = cur.fetchall()
                return rows
        finally:
            con.close()
