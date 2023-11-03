import random

from file_reader import *


def add_contact_email():
    employees = read_json('../files/employees.json')
    for employee in employees.values():
        employee['contact_email'] = '.'.join(employee['name'].lower().split(' ')) + '@' + random.choice(['gmail.com', 'op.pl', 'wp.pl'])
    write_json('../files/employees.json', employees, 2)


add_contact_email()
