from bs4 import BeautifulSoup


class HtmlParser:
    def __init__(self):
        self.elementSet = []

    def parse(self, html: str, tagName: str="body"):
        return self.extractElementToString(html, tagName)

    def extractElementToString(self, dom: str, tagName: str):
        contents = self._extractElementContent(dom, tagName)
        contentString = ""
        for tag in contents:
            stringTagName = tag[0]
            if stringTagName == "a":
                stringTagName = "hyperlink"
            stringContent = tag[1]
            contentString += "tag " + stringTagName + ", content " + stringContent + ". "
        return contentString

    def _extractElementContent(self, dom: str, tagName: str):
        contents = []

        soup = BeautifulSoup(dom, 'html.parser')
        element = soup.find(tagName)
        for string in element.stripped_strings:
            stringTagName = element.find(string=string)
            if stringTagName is None:
                continue
            else:
                stringTagName = stringTagName.parent.name
            stringContent = repr(string)[1:len(repr(string)) - 1]
            contents.append((stringTagName, stringContent))

        return contents
