import requests
import xml.etree.ElementTree as ET


class SynonymAPIError(Exception):
    pass


class API:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_szinonima(self, word: str, order: str = None, max: int = None):

        url = f"https://api.poet.hu/szinonima.php?f={self.username}&j={self.password}&s={word.lower()}"
        response = requests.get(url)

        if response.status_code == 200:
            content = response.content.decode("utf-8")
            root = ET.fromstring(content)

            match root.tag:
                case "hiba":
                    error = f"Error: {root.text}"
                    raise SynonymAPIError(error)

                case "szinonimak":
                    synonyms = []

                    for element in root.iter("szinonima"):
                        synonyms.append(element.text)
                        if max and len(synonyms) == max:
                            break

                    match order:
                        case "asc":
                            synonyms.sort()
                        case "desc":
                            synonyms.sort(reverse=True)

                    if len(synonyms) == 1:
                        return synonyms[0]

                    return synonyms

        else:
            error = f"Error: {response.status_code}"
            raise SynonymAPIError(error)

    def get_versek(self, category: str = None, author: str = None, text: str = None, max: int = None,
                   order_by: str = None, order: str = None, continue_from: int = None):

        url = f"https://api.poet.hu/vers.php?f={self.username}&j={self.password}"
        poems = []

        if category is not None:
            url += f"&kat={category}"
        if author is not None:
            url += f"&szerzo={author}"
        if text is not None:
            url += f"&szoveg={text}"
        if max is not None:
            url += f"&db={max}"
        if order_by is not None:
            url += f"&rendez={order_by}"
        if order is not None:
            if order == "asc":
                ordering = 0
            elif order == "desc":
                ordering = 1
            url += f"&rendez_ir={ordering}"
        if continue_from is not None:
            url += f"&honnan={continue_from}"

        if max is not None:
            if max > 5:
                max = 5

        response = requests.get(url)

        if response.status_code == 200:
            content = response.content.decode("utf-8")
            root = ET.fromstring(content)

            match root.tag:
                case "hiba":
                    error = f"Error: {root.text}"
                    raise SynonymAPIError(error)

                case "versek":
                    for vers in root.findall(".//vers"):
                        title = vers.find("cim").text
                        poem_text = vers.find("versszoveg").text
                        poem_author = vers.find("szerzo").text
                        cat = vers.find("kategoria").text

                        if vers.find("megjegyzes") is not None:
                            comment = vers.find("megjegyzes").text
                        else:
                            comment = ""

                        favs = vers.find("kedvenc").text
                        id = vers.find("id").text
                        url = vers.find("url").text
                        poems.append({
                            'title': title,
                            'text': poem_text,
                            'author': poem_author,
                            'category': cat,
                            'comment': comment,
                            'favs': favs,
                            'id': id,
                            'url': url
                        })

                    return poems

    def get_title(self, vers):
        title_list = []
        for title in vers:
            title_list.append(title.get('title'))
        if len(title_list) == 1:
            return title_list[0]
        return title_list

    def get_text(self, vers):
        text_list = []
        for text in vers:
            text_list.append(text.get('text'))
        if len(text_list) == 1:
            return text_list[0]
        return text_list

    def get_author(self, vers):
        author_list = []
        for author in vers:
            author_list.append(author.get('author'))
        if len(author_list) == 1:
            return author_list[0]
        return author_list

    def get_category(self, vers):
        category_list = []
        for category in vers:
            category_list.append(category.get('category'))
        if len(category_list) == 1:
            return category_list[0]
        return category_list

    def get_comment(self, vers):
        comment_list = []
        for comment in vers:
            comment_list.append(comment.get('comment'))
        if len(comment_list) == 1:
            return comment_list[0]
        return comment_list

    def get_favs(self, vers):
        fav_list = []
        for favs in vers:
            fav_list.append(favs.get('favs'))
        if len(fav_list) == 1:
            return fav_list[0]
        return fav_list

    def get_id(self, vers):
        id_list = []
        for id in vers:
            id_list.append(id.get('id'))
        if len(id_list) == 1:
            return id_list[0]
        return id_list

    def get_url(self, vers):
        url_list = []
        for url in vers:
            url_list.append(url.get('url'))
        if len(url_list) == 1:
            return url_list[0]
        return url_list
