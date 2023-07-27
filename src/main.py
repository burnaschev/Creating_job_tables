from src.DBManager import DBManager
from src.config import config
from src.utils import get_companies, create_database, save_data_to_database

PARAMS = config()
DB_NAME = 'data'


def main():
    companies = ['195398', '4181', '4484134', '4496', '78638', '4019151', '80660', '6082361', '2489601',
                 '740349']  # id компаний
    department = get_companies(companies)  # Получение списка работодателей и их вакансий с платформы HeadHunter
    create_database(DB_NAME, PARAMS)  # Создание базы данных
    save_data_to_database(department, DB_NAME, PARAMS)  # Добавление информаций по вакансиям и компаниям в таблицы"


db = DBManager(DB_NAME)

if __name__ == "__main__":
    main()
    print(db.get_all_vacancies())
