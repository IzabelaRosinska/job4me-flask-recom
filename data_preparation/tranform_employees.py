from file_reader import *


def make_dict(employees):
    return {str(i): {'email': employee['email'], "password": employee['password'], "name": employee['name'],
                     "phone": employee['phone'], "branches": employee["branches"], "education": employee['education'],
                     "work_experience": employee['work_experience'], "projects": employees['projects'],
                     "skills": employee['skills'], "about_me": employee['about_me'], "hobbies": employee['hobbies']}
            for i, employee in enumerate(employees)}


def count_length(employees):
    for email, employee in employees.items():
        print(email, '; '.join([f'{key}: {len(val)}' for key, val in employee.items()]))


def fix_it():
    employees = read_json('../files/employees.json')
    cvs = read_jsonl('../files/cv.jsonl')
    for employee, cv in zip(employees.values(), cvs):
        employee['projects'] = cv['projects'] if 'projects' in cv else []
    write_json('../files/employees.json', employees, 2)


fix_it()
