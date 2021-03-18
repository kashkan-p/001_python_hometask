from http_client import HttpClient
from rabotaby_parser import RabotaByParser

# Тут определяем базовый url и часть url отвечающий за поисковую выдачу, ключевое слово для поиска,
# часть url отвечающий за пагинацию и хедер

KEYWORD = 'Python'
URL = 'https://rabota.by/search/'
QUERY = f'vacancy?L_is_autosearch=false&area=1002&clusters=true&enable_snippets=true&text={KEYWORD}'
PAGE = '&page='
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}

if __name__ == '__main__':

    # В этом цикле получаем html код каждой страницы поисковой выдачи. Количество страниц пока хардкод, но его тоже нужно спарсить

    pages = []
    for url in range(0, 1):
        query = QUERY + PAGE + str(url)
        pages.append(HttpClient.get_html(URL, query=query, header=HEADERS))

    # В этом цикле с каждой страницы выдачи парсим ссылки на каждую вакансию. Получаем список равный количеству страниц
    # выдачи внутри которого каждый айтем является списком ссылок находящихся на странице

    vacancies_refs = []
    for page in pages:
        vacancies_refs.append(RabotaByParser(page).parse_vacancy_hrefs())

    # Преобразуем список из шага выше в один список ссылок на все вакансии из поисковой выдачи

    vacancies_refs_united = []
    for sublist in vacancies_refs:
        for ref in sublist:
            vacancies_refs_united.append(ref.split('?query')[0])

    # В этом цикле будем переходить по каждой ссылке из списка из предыдущего шага и парсить название и описание вакансии

    vacancy_description_dict = {}
    for url in vacancies_refs_united:
        response = HttpClient.get_html(url, header=HEADERS)
        parser = RabotaByParser(response)
        vacancy = parser.parse_vacancy_desc()
        vacancy_description_dict[vacancy[0]] = vacancy[1]

    # print(list(vacancy_description_dict.keys())[0])

    # Вот это всё сделано просто что бы глянуть как заработает, всё это нужно будет разделить на отдельные функции

    python_count = 0
    linux_count = 0
    flask_count = 0
    counted = {}
    for key in vacancy_description_dict:
        python = vacancy_description_dict[key].lower().count("python")
        linux = vacancy_description_dict[key].lower().count("linux")
        flask = vacancy_description_dict[key].lower().count("flask")
        counted[key] = {"python occurrences": python, "linux occurrences": linux, "flask occurrences": flask}
        python_count += python
        linux_count += linux
        flask_count += flask

    print(counted)
    print(python_count / len(vacancy_description_dict), flask_count / len(vacancy_description_dict),
          linux_count / len(vacancy_description_dict))
