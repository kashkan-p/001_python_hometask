from bs4 import BeautifulSoup


# Здесь в конструктор передаем html код страницы и затем парсим всё что нам нужно. Наверное лучше тоже всё будет сделать
# методами класса

class RabotaByParser:
    def __init__(self, raw_html):
        self.raw_html = raw_html

    # def get_page_number(self):
    #     soup = BeautifulSoup(self.raw_html, "lxml")

    def parse_vacancy_hrefs(self):
        soup = BeautifulSoup(self.raw_html, "lxml")
        vacancies = soup.find_all("div", class_="vacancy-serp-item__row vacancy-serp-item__row_header")
        vacancy_list = []
        for item in vacancies:
            vacancy_list.append(item.find("a", class_="bloko-link").get("href"))
        return vacancy_list

    def parse_vacancy_desc(self):
        soup = BeautifulSoup(self.raw_html, "lxml")
        title = soup.find("div", class_="vacancy-title").find("h1").text
        vacancy_desc = soup.find("div", class_="vacancy-section").prettify()
        return title, vacancy_desc
