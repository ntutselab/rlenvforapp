from bs4 import BeautifulSoup


class HtmlParser:
    def __init__(self):
        self.element_set = []

    def parse(self, html: str, tag_name: str = "body"):
        return self.extract_element_to_string(html, tag_name)

    def extract_element_to_string(self, dom: str, tag_name: str):
        contents = self._extract_element_content(dom, tag_name)
        content_string = ""
        for tag in contents:
            stringTagName = tag[0]
            if stringTagName == "a":
                stringTagName = "hyperlink"
            stringContent = tag[1]
            content_string += "tag " + stringTagName + ", content " + stringContent + ". "
        return content_string

    def _extract_element_content(self, dom: str, tag_name: str):
        contents = []

        soup = BeautifulSoup(dom, 'html.parser')
        element = soup.find(tag_name)
        for string in element.stripped_strings:
            stringTagName = element.find(string=string)
            if stringTagName is None:
                continue
            else:
                stringTagName = stringTagName.parent.name
            stringContent = repr(string)[1:len(repr(string)) - 1]
            contents.append((stringTagName, stringContent))

        return contents
