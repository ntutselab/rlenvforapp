from io import StringIO

from lxml import etree

from RLEnvForApp.logger.logger import Logger


class HtmlExtractor:
    def __init__(self):
        pass

    def get_label_name(self, dom: str, focusElementXpath: str):
        tree = etree.parse(StringIO(dom), etree.HTMLParser())
        focus_elements = tree.xpath(focusElementXpath.lower())
        focus_element = None
        if focus_elements:
            focus_element = focus_elements[0]
        label_name = ""

        if focus_element is not None:
            label_name = etree.tostring(
                focus_element,
                method="text",
                encoding="UTF-8").decode('utf-8').strip()

            if label_name == "":
                label_name = self._find_label_byid(tree, focus_element)
            if label_name == "":
                label_name = self._find_closest_label_name(element=focus_element)
            if label_name == "":
                label_name = self._get_html_tag_attribute(
                    element=focus_element, attribute="placeholder")

        if label_name == "":
            Logger().info(
                f"HTML Extractor Warning: Can't find Label name in xpath[{focusElementXpath}]")

        return ' '.join(label_name.split())

    def get_placeholder(self, dom: str, focusElementXpath: str):
        tree = etree.parse(StringIO(dom), etree.HTMLParser())
        focus_elements = tree.xpath(focusElementXpath.lower())
        focus_element = None
        if focus_elements:
            focus_element = focus_elements[0]

        placeholder = ""
        if focus_element is not None:
            placeholder = self._get_html_tag_attribute(
                element=focus_element, attribute="placeholder")

        return ' '.join(placeholder.split())

    def _find_label_byid(self, tree, element):
        label_name = ""
        if element is not None and 'id' in element.attrib:
            focusElementId = element.attrib['id']
            labels = tree.xpath("//label[@for='" + focusElementId + "']")
            if labels:
                labelElement = labels[0]
                label_name = labelElement.text

        return label_name

    def _find_closest_label_name(self, element):
        label_name = ""
        level_of_parents = 0
        try:
            inputElements = element.getparent().xpath(".//input".lower())
            if not inputElements and element not in inputElements:
                return label_name
            index = inputElements.index(element)

            while not label_name and level_of_parents <= 5:
                labelElements = element.xpath(".//label".lower())
                if not labelElements:
                    element = element.getparent()
                    level_of_parents += 1
                elif len(labelElements) > 1:
                    if self._get_html_tag_attribute(labelElements[index], "for"):
                        element = element.getparent()
                        level_of_parents += 1
                        continue
                    label_name = etree.tostring(labelElements[index], method="text", encoding="UTF-8").decode(
                        'utf-8').strip()
                else:
                    if self._get_html_tag_attribute(labelElements[0], "for"):
                        element = element.getparent()
                        level_of_parents += 1
                        continue
                    label_name = etree.tostring(labelElements[0], method="text", encoding="UTF-8").decode(
                        'utf-8').strip()
        except Exception as exception:
            Logger().info(
                f"HTML Extractor Warning: find closest Label name fail {exception}")

        return label_name

    def _get_html_tag_attribute(self, element, attribute):
        try:
            attribute_text = element.attrib[attribute]
        except Exception:
            attribute_text = ""
        return attribute_text
