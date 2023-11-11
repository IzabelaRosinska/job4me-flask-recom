# import numpy as np
# import pyodbc
#
#
# def put_offer_list_values(cursor, offer, offer_id):
#     cursor.execute(f'SELECT description FROM dbo.extra_skills WHERE job_offer_id = {offer_id};')
#     offer['extra_skills'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT description FROM dbo.requirements WHERE job_offer_id = {offer_id};')
#     offer['requirements'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT name FROM dbo.industries i JOIN dbo.job_offer_industries oi ON oi.industry_id = i.id WHERE '
#                    f'oi.job_offer_id = {offer_id};')
#     offer['branches'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT level_id FROM dbo.job_offer_levels WHERE job_offer_id = {offer_id};')
#     offer['levels'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT contract_type_id FROM dbo.job_offer_contract_types WHERE job_offer_id = {offer_id};')
#     offer['contract_types'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT employment_form_id FROM dbo.job_offer_employment_forms WHERE job_offer_id = {offer_id};')
#     offer['forms'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT localization_id FROM dbo.job_offer_localizations WHERE job_offer_id = {offer_id};')
#     offer['localizations'] = [data[0] for data in cursor.fetchall()]
#
#
# def put_all_offers_list_values(cursor, offers):
#     cursor.execute(f'SELECT job_offer_id, description FROM dbo.extra_skills;')
#     for row in cursor.fetchall():
#         offers[row[0]]['extra_skills'] = row[1]
#     cursor.execute(f'SELECT job_offer_id, description FROM dbo.requirements;')
#     for row in cursor.fetchall():
#         offers[row[0]]['requirements'] = row[1]
#     cursor.execute(f'SELECT oi.job_offer_id, i.name FROM dbo.industries i '
#                    f'JOIN dbo.job_offer_industries oi ON oi.industry_id = i.id;')
#     for row in cursor.fetchall():
#         offers[row[0]]['branches'] = row[1]
#     cursor.execute(f'SELECT job_offer_id, level_id FROM dbo.job_offer_levels;')
#     for row in cursor.fetchall():
#         offers[row[0]]['levels'] = row[1]
#     cursor.execute(f'SELECT job_offer_id, contract_type_id FROM dbo.job_offer_contract_types;')
#     for row in cursor.fetchall():
#         offers[row[0]]['contract_types'] = row[1]
#     cursor.execute(f'SELECT job_offer_id, employment_form_id FROM dbo.job_offer_employment_forms;')
#     for row in cursor.fetchall():
#         offers[row[0]]['forms'] = row[1]
#     cursor.execute(f'SELECT job_offer_id, localization_id FROM dbo.job_offer_localizations;')
#     for row in cursor.fetchall():
#         offers[row[0]]['localizations'] = row[1]
#
#
# def get_offer_by_id(cursor: pyodbc.Cursor, offer_id):
#     cursor.execute(f'SELECT offer_name, salary_from, duties, description, duties_embeddings, '
#                    f'description_embeddings, skills_embeddings FROM dbo.job_offers WHERE id = {offer_id};')
#     row = cursor.fetchone()
#     if not row:
#         return None
#     offer = {'name': row[0], 'min_salary': row[1],
#              'duties': row[2] if row[2] is not None else '', 'description': row[3] if row[3] is not None else ''}
#     offer_embeddings = {'duties': np.frombuffer(row[4], dtype=np.float32),
#                         'description': np.frombuffer(row[5], dtype=np.float32),
#                         'requirements+extra_skills': np.frombuffer(row[6], dtype=np.float32)}
#     put_offer_list_values(cursor, offer, offer_id)
#     return offer, offer_embeddings
#
#
# def get_all_offers(cursor: pyodbc.Cursor):
#     cursor.execute(f'SELECT id, offer_name, salary_from, duties, description, duties_embeddings, '
#                    f'description_embeddings, skills_embeddings FROM dbo.job_offers;')
#     rows = cursor.fetchall()
#     offers = {}
#     offers_embeddings = {}
#     for row in rows:
#         offers[row[0]] = {'name': row[1], 'min_salary': row[2], 'duties': row[3] if row[3] is not None else '',
#                           'description': row[4] if row[4] is not None else ''}
#         embeddings = {}
#         if row[5]:
#             embeddings['duties'] = np.frombuffer(row[5], dtype=np.float32)
#         if row[6]:
#             embeddings['description'] = np.frombuffer(row[6], dtype=np.float32)
#         if row[7]:
#             embeddings['requirements+extra_skills'] = np.frombuffer(row[7], dtype=np.float32)
#         offers_embeddings[row[0]] = embeddings
#     put_all_offers_list_values(cursor, offers)
#     return offers, offers_embeddings
#
#
# def save_offer_embeddings(cursor, offer_id, embeddings):
#     query = f'UPDATE dbo.job_offers SET duties_embeddings = ?, description_embeddings = ?, skills_embeddings = ? ' \
#             f'WHERE id = {offer_id}; '
#     cursor.execute(query, (embeddings["duties"].tobytes() if "duties" in embeddings else None,
#                            embeddings["description"].tobytes() if "description" in embeddings else None,
#                            embeddings["requirements+extra_skills"].tobytes() if "requirements+extra_skills" in
#                                                                                 embeddings else None))
#
#
# def get_employee_by_id(cursor: pyodbc.Cursor, employee_id: int):
#     cursor.execute(f'SELECT about_me, interests FROM dbo.employees WHERE id = {employee_id};')
#     row = cursor.fetchone()
#     if not row:
#         return None
#     employee = {'about_me': row[0] if row[0] is not None else '', 'hobbies': row[1] if row[1] is not None else ''}
#     cursor.execute(f'SELECT description FROM dbo.education WHERE employee_id = {employee_id};')
#     employee['education'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT description FROM dbo.experience WHERE employee_id = {employee_id};')
#     employee['experience'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT description FROM dbo.projects WHERE employee_id = {employee_id};')
#     employee['projects'] = [data[0] for data in cursor.fetchall()]
#     cursor.execute(f'SELECT description FROM dbo.skills WHERE employee_id = {employee_id};')
#     employee['skills'] = [data[0] for data in cursor.fetchall()]
#     return employee
#
#
# def get_all_employees(cursor: pyodbc.Cursor):
#     cursor.execute(f'SELECT id, about_me, interests FROM dbo.employees;')
#     rows = cursor.fetchall()
#     employees = {row[0]: {'about_me': row[1] if row[1] is not None else '',
#                           'hobbies': row[2] if row[2] is not None else ''} for row in rows}
#     cursor.execute(f'SELECT employee_id, description FROM dbo.education;')
#     for row in cursor.fetchall():
#         employees[row[0]]['education'] = row[1]
#     cursor.execute(f'SELECT employee_id, description FROM dbo.experience;')
#     for row in cursor.fetchall():
#         employees[row[0]]['experience'] = row[1]
#     cursor.execute(f'SELECT employee_id, description FROM dbo.projects;')
#     for row in cursor.fetchall():
#         employees[row[0]]['projects'] = row[1]
#     cursor.execute(f'SELECT employee_id, description FROM dbo.skills;')
#     for row in cursor.fetchall():
#         employees[row[0]]['skills'] = row[1]
#     return employees
