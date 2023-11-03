import numpy as np
import pyodbc
from tqdm import tqdm

from file_reader import *

server = 'tcp:miwmjob4me.database.windows.net,1433'
database = 'miwm'
username = 'miwm'
password = 'job4meZPI'
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')

cursor = conn.cursor()


def cut(text, char_limit):
    if len(text) < char_limit:
        return text
    while len(text) > char_limit-1:
        # text = text[:-1]
        if (index := max(text.rfind("."), text.rfind("\n"), text.rfind(","))) != -1:
            text = text[:index]
        else:
            return ""
    return text + "."


def reset_table(table_name, with_id=True):
    cursor.execute(f'DELETE FROM {table_name};')
    if with_id:
        cursor.execute(f"DBCC CHECKIDENT ('{table_name}', RESEED, 0);")


def add_simple_rows(table_name, values):
    for val in values:
        query = f'INSERT INTO {table_name} (name) VALUES (?);'
        cursor.execute(query, val)
        # cursor.execute(f"INSERT INTO {table_name} (name) VALUES ('{val}');")


def add_all_simple_rows():
    reset_table('dbo.levels')
    add_simple_rows('dbo.levels', levels)
    reset_table('dbo.employment_forms')
    add_simple_rows('dbo.employment_forms', forms)
    reset_table('dbo.contract_types')
    add_simple_rows('dbo.contract_types', contract_types)
    reset_table('dbo.industries')
    add_simple_rows('dbo.industries', industries)
    conn.commit()


def reset_employers():
    reset_table('dbo.employers')


def add_employers():
    companies = read_json('../files/companies.json')
    for name, company in companies.items():
        email = company['contact_email']
        locked = 1
        password = '1234'
        telephone = company['contact_phone']
        role = b"\x00\x01\x02\x03\x04"
        address = company['address']
        company_name = name
        description = company['description']
        display_description = description.split('.')[0] if description else 'Najlepsi z najlepszych'
        photo = "https://picsum.photos/100/100"
        query = f'INSERT INTO dbo.employers (email, locked, password, telephone, role, address, company_name, ' \
                f'description, display_description, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?); '
        cursor.execute(query, (email, locked, password, telephone, role, address, company_name, description, display_description, photo))
        # cursor.execute(
        #     f'INSERT INTO dbo.employers (email, locked, password, telephone, role, address, company_name, description, display_description, photo) VALUES ("{email}", {locked}, "{password}", "{telephone}", {role}, "{address}", "{company_name}", "{description}", "{display_description}", "{photo}");')
    conn.commit()


def add_list_values_to_offer(parent_id, table_name, descriptions, max_char):
    for val in descriptions:
        query = f'INSERT INTO {table_name} (description, job_offer_id) VALUES (?, ?)'
        cursor.execute(query, (cut(val, max_char), parent_id))
        # cursor.execute(f"INSERT INTO {table_name} (description, job_offer_id) VALUES ('{val}', {parent_id})")


def add_connections_to_offer(parent_id, table_name, other_id_name, connected_ids):
    # pass
    for val in connected_ids:
        print(parent_id, val, table_name)
        query = f'INSERT INTO {table_name} (job_offer_id, {other_id_name}) VALUES (?, ?)'
        cursor.execute(query, (parent_id, val))
        # cursor.execute(f"INSERT INTO {table_name} (job_offer_id, {other_id_name}) VALUES ({parent_id}, {val});")


def add_list_values_to_employee(parent_id, table_name, descriptions):
    for val in descriptions:
        query = f'INSERT INTO {table_name} (description, employee_id) VALUES (?, ?)'
        cursor.execute(query, (val, parent_id))
        # cursor.execute(f"INSERT INTO {table_name} (description, employee_id) VALUES ('{val}', {parent_id});")


def reset_offers():
    reset_table('dbo.job_offer_levels', False)
    reset_table('dbo.job_offer_employment_forms', False)
    reset_table('dbo.job_offer_contract_types', False)
    reset_table('dbo.job_offer_industries', False)
    reset_table('dbo.job_offer_localizations', False)
    reset_table('dbo.localizations')
    reset_table('dbo.extra_skills')
    reset_table('dbo.requirements')
    reset_table('dbo.job_offers')


def add_offers(with_embeddings=False):
    offers = read_json('../files/offers.json')
    embeddings = read_json('../files/offers_embeddings.json')
    companies = read_json('../files/companies.json')
    i = 0
    companies_dict = {name: str(i := i + 1) for name in companies}
    localizations = {}
    loc_index = 0
    for j, (offer, offer_embeddings) in tqdm(enumerate(zip(offers.values(), embeddings.values()))):
        description = offer['description']
        duties = offer['duties']
        offer_name = offer['name']
        salary_from = offer['min_salary']
        salary_to = offer['max_salary'] if 'max_salary' in offer else None
        working_time = offer['working_time']
        employer_id = companies_dict[offer['company']]
        if with_embeddings:
            duties_embeddings = np.array(offer_embeddings['duties'], dtype=np.float32).tobytes() if 'duties' in offer_embeddings else None
            description_embeddings = np.array(offer_embeddings['description'], dtype=np.float32).tobytes() if 'description' in offer_embeddings else None
            skills_embeddings = np.array(offer_embeddings['requirements+extra_skills'], dtype=np.float32).tobytes() if 'requirements+extra_skills' in offer_embeddings else None
            query = f'INSERT INTO dbo.job_offers (description, duties, offer_name, salary_from, salary_to, ' \
                    f'working_time, employer_id, duties_embeddings, description_embeddings, skills_embeddings) ' \
                    f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
            cursor.execute(query, (cut(description, 490), cut(duties, 990), offer_name, salary_from, salary_to, working_time, employer_id, duties_embeddings, description_embeddings, skills_embeddings))
            # cursor.execute(
            #     f'INSERT INTO dbo.offers (description, duties, offer_name, salary_from, salary_to, working_time, '
            #     f'employer_id, duties_embeddings, description_embeddings, skills_embeddings) VALUES ("{description}", '
            #     f'"{duties}", "{offer_name}", {salary_from}, {salary_to}, "{working_time}", {employer_id}, '
            #     f'{duties_embeddings}, {description_embeddings}, {skills_embeddin gs})')
        else:
            query = f'INSERT INTO dbo.offers (description, duties, offer_name, salary_from, salary_to, working_time, ' \
                    f'employer_id) VALUES (?, ?, ?, ?, ?, ?, ?);'
            cursor.execute(query, (description, duties, offer_name, salary_from, salary_to, working_time, employer_id))
            # cursor.execute(
            #     f'INSERT INTO dbo.offers (description, duties, offer_name, salary_from, salary_to, working_time, '
            #     f'employer_id) VALUES ("{description}", "{duties}", "{offer_name}", {salary_from}, {salary_to}, '
            #     f'"{working_time}", {employer_id})')
        for localization in offer['localizations']:
            if localization not in localizations:
                query = f'INSERT INTO dbo.localizations (city) VALUES (?);'
                cursor.execute(query, localization)
                # cursor.execute(f"INSERT INTO dbo.localizations (city) VALUES ('{localization}');")
                loc_index += 1
                localizations[localization] = loc_index
            add_connections_to_offer(j + 1, 'dbo.job_offer_localizations', 'localization_id',
                                     [localizations[localization]])

        add_list_values_to_offer(j + 1, 'dbo.extra_skills', offer['extra_skills'], 180)
        add_list_values_to_offer(j + 1, 'dbo.requirements', offer['requirements'], 220)
        add_connections_to_offer(j + 1, 'dbo.job_offer_levels', 'level_id',
                                 [levels.index(level) + 1 for level in offer['levels']])
        add_connections_to_offer(j + 1, 'dbo.job_offer_contract_types', 'contract_type_id',
                                 [contract_types.index(val) + 1 for val in offer['contract_types']])
        add_connections_to_offer(j + 1, 'dbo.job_offer_employment_forms',
                                 'employment_form_id', [forms.index(val) + 1 for val in offer['forms']])
        add_connections_to_offer(j + 1, 'dbo.job_offer_industries', 'industry_id',
                                 [industries.index(val) + 1 for val in offer['branches']])
        conn.commit()


def reset_employees():
    reset_table('dbo.projects')
    reset_table('dbo.education')

    reset_table('dbo.experience')
    reset_table('dbo.skills')
    reset_table('dbo.employees')


def add_employees():
    employees = read_json('../files/employees.json')

    for i, employee in enumerate(employees.values()):
        email = employee['email']
        locked = 1
        password = employee['password']
        telephone = employee['phone']
        role = b"\x00\x01\x02\x03\x04"
        about_me = employee['about_me']
        contact_email = employee['contact_email']
        first_name = employee['name'].split(' ')[0]
        interests = employee['hobbies']
        last_name = employee['name'].split(' ')[1]
        query = f"INSERT INTO dbo.employees (email, locked, password, telephone, role, about_me, contact_email, first_name, interests, last_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        cursor.execute(query, (email, locked, password, telephone, role, about_me, contact_email, first_name, interests, last_name))
        # cursor.execute(
        #     f'INSERT INTO dbo.employees (email, locked, password, telephone, role, about_me, contact_email, '
        #     f'first_name, interests, last_name) VALUES ("{email}", {locked}, "{password}", "{telephone}", {role}, '
        #     f'"{about_me}", "{contact_email}", "{first_name}", "{interests}", "{last_name}");')
        add_list_values_to_employee(i + 1, 'dbo.education', employee['education'])
        add_list_values_to_employee(i + 1, 'dbo.projects', employee['projects'])
        add_list_values_to_employee(i + 1, 'dbo.experience', employee['work_experience'])
        add_list_values_to_employee(i + 1, 'dbo.skills', employee['skills'])


def reset_verification_tokens():
    reset_table('dbo.verification_token')


# def add_offer_connectors():
#     offers = read_json('../files/offers.json')
#     select_query = "SELECT id, city FROM dbo.localizations;"
#     data_dict = {}
#     cursor.execute(select_query)
#     for row in cursor:
#         id, city = row.id, row.city
#         data_dict[city] = id
#     for i, offer in enumerate(offers.values()):



levels = ['Stażysta', 'Junior', 'Mid', 'Senior', "Menedżer"]
forms = ['praca stacjonarna', 'praca hybrydowa', 'praca zdalna']
contract_types = ['umowa o pracę', 'kontrakt B2B', 'umowa zlecenie', 'umowa o staż']
industries = ['IT', 'Sprzedaż', 'Administracja Biura', 'Zdrowie']

# reset_verification_tokens()
# reset_employees()
reset_offers()
# reset_employers()
# add_all_simple_rows()
# add_employers()
add_offers(True)
# add_employees()

conn.commit()

# add_simple_rows('dbo.contract_types', contract_types)

# new_name = 'umowa o staż'
# insert_query = f"INSERT INTO dbo.contract_types (name) VALUES ('{new_name}')"
# cursor.execute(insert_query)
# conn.commit()

# reset_table('dbo.contract_types')

# cursor.execute("SELECT * FROM dbo.contract_types")
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)

conn.close()
