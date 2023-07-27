from src.utils import get_companies, create_database, save_data_to_database
from src.config import config


def main():
    companies = ['195398', '4181', '4484134', '4496', '78638', '4019151', '80660', '6082361', '2489601', '740349']
    department = get_companies(companies)
    params = config()
    create_database(params)
    save_data_to_database(department, params)


if __name__ == "__main__":
    main()
