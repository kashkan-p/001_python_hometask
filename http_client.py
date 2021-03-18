import requests


# Здесь просто делаем обёртку метода get чтобы он принимал нужные нам аргументы и возращал нужные данные

class HttpClient:

    @classmethod
    def get_html(cls, base_url, query=None, header=None):
        url = base_url
        if query:
            url = base_url + query
        response = requests.get(url, headers=header)
        return response.text
