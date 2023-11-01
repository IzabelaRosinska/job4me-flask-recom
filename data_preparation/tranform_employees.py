from file_reader import *


def make_dict(employees):
    return {str(i): {'email': employee['email'], "password": employee['password'], "name": employee['name'],
                     "phone": employee['phone'], "branches": employee["branches"], "education": employee['education'],
                     "work_experience": employee['work_experience'], "skills": employee['skills'],
                     "about_me": employee['about_me'], "hobbies": employee['hobbies']} for i, employee in
            enumerate(employees)}


def count_length(employees):
    for email, employee in employees.items():
        print(email, '; '.join([f'{key}: {len(val)}' for key, val in employee.items()]))


employees = read_json('../files/employees.json')
# employees = read_jsonl('../files/cv.jsonl')

# new_employees = make_dict(employees)
count_length(employees)

# write_json('../files/employees.json', new_employees)
# with open('../files/employees.json', 'w', encoding='utf-8') as file:
#     json.dump(new_employees, file, ensure_ascii=False, indent=2)
