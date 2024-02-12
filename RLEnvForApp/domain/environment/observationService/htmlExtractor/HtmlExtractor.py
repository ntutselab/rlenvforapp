from io import StringIO

from lxml import etree

from RLEnvForApp.logger.logger import Logger


class HtmlExtractor:
    def __init__(self):
        pass

    def get_label_name(self, dom: str, focusElementXpath: str):
        tree = etree.parse(StringIO(dom), etree.HTMLParser())
        focusElements = tree.xpath(focusElementXpath.lower())
        focusElement = None
        if focusElements:
            focusElement = focusElements[0]
        labelName = ""

        if focusElement is not None:
            labelName = etree.tostring(
                focusElement,
                method="text",
                encoding="UTF-8").decode('utf-8').strip()

            if labelName == "":
                labelName = self._find_label_byid(tree, focusElement)
            if labelName == "":
                labelName = self._find_closest_label_name(element=focusElement)
            if labelName == "":
                labelName = self._get_html_tag_attribute(
                    element=focusElement, attribute="placeholder")

        if labelName == "":
            Logger().info(
                f"HTML Extractor Warning: Can't find Label name in xpath[{focusElementXpath}]")

        return ' '.join(labelName.split())

    def get_placeholder(self, dom: str, focusElementXpath: str):
        tree = etree.parse(StringIO(dom), etree.HTMLParser())
        focusElements = tree.xpath(focusElementXpath.lower())
        focusElement = None
        if focusElements:
            focusElement = focusElements[0]

        placeholder = ""
        if focusElement is not None:
            placeholder = self._get_html_tag_attribute(
                element=focusElement, attribute="placeholder")

        return ' '.join(placeholder.split())

    def _find_label_byid(self, tree, element):
        labelName = ""
        if element is not None and 'id' in element.attrib:
            focusElementId = element.attrib['id']
            labels = tree.xpath("//label[@for='" + focusElementId + "']")
            if labels:
                labelElement = labels[0]
                labelName = labelElement.text

        return labelName

    def _find_closest_label_name(self, element):
        labelName = ""
        levelOfParents = 0
        try:
            inputElements = element.getparent().xpath(".//input".lower())
            if not inputElements and element not in inputElements:
                return labelName
            index = inputElements.index(element)

            while not labelName and levelOfParents <= 5:
                labelElements = element.xpath(".//label".lower())
                if not labelElements:
                    element = element.getparent()
                    levelOfParents += 1
                elif len(labelElements) > 1:
                    if self._get_html_tag_attribute(labelElements[index], "for"):
                        element = element.getparent()
                        levelOfParents += 1
                        continue
                    labelName = etree.tostring(labelElements[index], method="text", encoding="UTF-8").decode(
                        'utf-8').strip()
                else:
                    if self._get_html_tag_attribute(labelElements[0], "for"):
                        element = element.getparent()
                        levelOfParents += 1
                        continue
                    labelName = etree.tostring(labelElements[0], method="text", encoding="UTF-8").decode(
                        'utf-8').strip()
        except Exception as e:
            Logger().info(
                f"HTML Extractor Warning: find closest Label name fail {e}")

        return labelName

    def _get_html_tag_attribute(self, element, attribute):
        try:
            attributeText = element.attrib[attribute]
        except Exception as e:
            attributeText = ""
        return attributeText
