import json
import random

import requests
from bs4 import BeautifulSoup


def find_name(soup: BeautifulSoup) -> str:
    return soup.find('h1', class_="offer-viewkHIhn3").get_text().encode('latin1').decode('utf-8')


def find_company_name(soup: BeautifulSoup) -> str:
    return soup.find('h2', class_="offer-viewwtdXJ4").find_all(string=True)[0].encode('latin1').decode('utf-8').strip()


def find_salary(soup: BeautifulSoup) -> str:
    salary = soup.find('strong', class_="offer-viewLdvtPw")
    if salary:
        return salary.get_text().encode('latin1').decode('utf-8')
    return ""


def find_localization(soup: BeautifulSoup) -> list[str]:
    localization = soup.find('p', class_="offer-viewAV75Zu")
    if localization:
        return [localization.get_text().encode('latin1').decode('utf-8')]
    else:
        return [soup.find('button', class_="offer-viewnqE8MW").get_text().encode('latin1').decode('utf-8')]


def find_specialization(soup: BeautifulSoup) -> str:
    return soup.find('span', class_="offer-viewPFKc0t").get_text().encode('latin1').decode('utf-8')


def find_technologies(soup: BeautifulSoup) -> tuple[list[str], list[str]]:
    technologies = soup.find_all('li', class_="offer-vieweKR6vg")
    obligatory = []
    optional = []
    for technology in technologies:
        if "offer-viewjJiyAa" in technology["class"]:
            obligatory.append(technology.get_text().encode('latin1').decode('utf-8'))
        else:
            optional.append(technology.get_text().encode('latin1').decode('utf-8'))
    return obligatory, optional


def find_offers_params(soup: BeautifulSoup) -> tuple[str, str, str, str]:
    contract_type = soup.find('div', class_="offer-viewXo2dpV")
    working_time = contract_type.find_next('div', class_="offer-viewXo2dpV")
    level = working_time.find_next('div', class_="offer-viewXo2dpV")
    form = level.find_next('div', class_="offer-viewXo2dpV")
    return contract_type.get_text().encode('latin1').decode('utf-8'), \
           working_time.get_text().encode('latin1').decode('utf-8'), \
           level.get_text().encode('latin1').decode('utf-8'), \
           form.get_text().encode('latin1').decode('utf-8')


def find_requirements(soup: BeautifulSoup) -> list[str]:
    requirements = soup.find(attrs={"data-scroll-id": "requirements-expected-1"})
    if requirements:
        requirements = requirements.find_all('li', class_="offer-viewFkOubE")
        return [requirement.get_text().encode('latin1').decode('utf-8') for requirement in requirements]
    return []


def find_extra_skills(soup: BeautifulSoup) -> list[str]:
    extra_skills = soup.find(attrs={"data-scroll-id": "requirements-optional-1"})
    if extra_skills:
        extra_skills = extra_skills.find_all('li', class_="offer-viewFkOubE")
        return [requirement.get_text().encode('latin1').decode('utf-8') for requirement in extra_skills]
    return []


def find_and_process_requirements(soup: BeautifulSoup) -> tuple[list[str], list[str]]:
    obligatory_technologies, optional_technologies = find_technologies(soup)
    requirements = find_requirements(soup)
    extra_skills = find_extra_skills(soup)
    for technology in obligatory_technologies:
        is_new = True
        for requirement in requirements:
            if technology in requirement:
                is_new = False
                break
        if is_new:
            requirements.append(technology)
    for technology in optional_technologies:
        is_new = True
        for extra_skill in extra_skills:
            if technology in extra_skill:
                is_new = False
                break
        if is_new:
            extra_skills.append(technology)
    return requirements, extra_skills


def find_duties(soup: BeautifulSoup, separate_duties: bool = True) -> str:
    duties = soup.find('ul', class_="offer-view6lWuAT")
    if duties:
        duties = duties.find_all('li', class_="offer-viewFkOubE")
        duties = [duty.get_text().encode('latin1').decode('utf-8') for duty in duties]
        for i in range(len(duties) - 1):
            if duties[i][-1] in [',', '.', ';']:
                duties[i] = duties[i][:-1]
            duties[i] += ('.' if duties[i + 1] == "" or duties[i + 1][0].isupper() else ',')
        return ' '.join(duties) if separate_duties else '\n'.join(duties)
    return ""


def find_about_project(soup: BeautifulSoup) -> str:
    about = soup.find('div', class_="offer-viewlvWH1V")
    return about.get_text().encode('latin1').decode('utf-8') if about else ""


def find_what_we_offer(soup: BeautifulSoup, separate_lines: bool = True) -> str:
    extras = soup.find('div', class_="offer-viewaYTjNT")
    if extras:
        extras = extras.find_all('li', class_="offer-view0fL3IZ")
        extras = [duty.get_text().encode('latin1').decode('utf-8') for duty in extras]
        for i in range(len(extras) - 1):
            if extras[i][-1] in [',', '.', ';']:
                extras[i] = extras[i][:-1]
            extras[i] += ('.' if extras[i + 1] == "" or extras[i + 1][0].isupper() else ',')
        return ' '.join(extras) if separate_lines else '\n'.join(extras)
    return ""


def find_about_us(soup: BeautifulSoup) -> str:
    about_us = soup.find('div', class_="offer-viewr0S3zJ")
    if about_us:
        about_us = about_us.find_all('p', class_="offer-viewfkAkeG")
        return '\n'.join([p.get_text().encode('latin1').decode('utf-8') for p in about_us])
    return ''


def fix_spaces(offer: dict[str, str | list[str]]):
    for key, val in offer.items():
        if isinstance(val, list):
            for i in range(len(val)):
                val[i] = val[i].replace('\u202f', ' ').replace('\xa0', '')
        else:
            val = val.replace('\u202f', ' ').replace('\xa0', '')
        offer[key] = val
    return offer


def get_offer(url: str, duties_separate, extras_separate):
    response = requests.get(url, headers={'Accept-Encoding': 'utf-8'})
    if response.status_code == 200:
        print(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        offer = {'name': find_name(soup), 'localization': find_localization(soup), 'company': find_company_name(soup),
                 'salary': find_salary(soup), 'contract_type': (find_offers_params(soup))[0],
                 'working_time': (find_offers_params(soup))[1], 'level': (find_offers_params(soup))[2],
                 'form': (find_offers_params(soup))[3], 'requirements': (find_and_process_requirements(soup))[0],
                 'extra_skills': (find_and_process_requirements(soup))[1], 'duties': find_duties(soup, duties_separate),
                 'about_project': find_about_project(soup), 'what_we_offer': find_what_we_offer(soup, extras_separate),
                 'about_us': find_about_us(soup)}
        offer = fix_spaces(offer)
        return offer


def get_all_offers(url: str):
    response = requests.get(url, headers={'Accept-Encoding': 'utf-8'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True, class_="listing_n194fgoq")]
        is_first = True
        with open('offers_sprzedaż.jsonl', 'r', encoding='utf-8') as file:
            offers = [json.loads(offer) for offer in file]
        offers_dict = {}
        for offer in offers:
            offers_dict[(offer['name'], offer['company'], offer['level'])] = offer
        for link in links:
            if "pracodawcy" not in link:
                if is_first:
                    duties_separate = random.randint(0, 3) > 0
                    extras_separate = random.randint(0, 3) > 0
                    try:
                        offer = get_offer(link, duties_separate, extras_separate)
                        unique_data = (offer['name'], offer['company'], offer['level'])
                        if unique_data in offers_dict:
                            if offer['localization'] not in offers_dict[unique_data]['localization']:
                                offers_dict[unique_data]['localization'].append(offer['localization'])
                        else:
                            offers_dict[unique_data] = offer
                    except Exception as e:
                        print(f'Exception in {link}')
                is_first = not is_first
        with open('offers_sprzedaż.jsonl', 'w', encoding='utf-8') as file:
            for element in list(offers_dict.values()):
                json.dump(element, file, ensure_ascii=False)
                file.write('\n')


# get_offer('https://www.pracuj.pl/praca/release-tester-katowice-bracka-28a,oferta,1002890062?s=8a082c87&searchId=MTY5NjkyMjgyMjAwNC42MDc0', True, True)
get_all_offers("https://www.pracuj.pl/praca/sprzeda%C5%BC;cc,5028?pn=5&content=869178782752856141%2C-8712487292646447305&campaignid=20330707368&adgroupid=153698629569&twdr=10872205446335339352&twdnt=g&gclid=Cj0KCQjw7JOpBhCfARIsAL3bobdxnvvAXGAevvja1tosZXsX7zN6A35d9xctJ49PgkYrKcUAVcXszvEaAhPiEALw_wcB")

