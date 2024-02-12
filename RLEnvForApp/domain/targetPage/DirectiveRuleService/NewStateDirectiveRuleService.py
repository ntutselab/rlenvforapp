import difflib
import re
from io import StringIO

from lxml import etree
from RLEnvForApp.domain.targetPage.DirectiveRuleService.FormSubmitCriteriaSingleton import \
    FormSubmitCriteriaSingleton
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import \
    IDirectiveRuleService
from RLEnvForApp.logger.logger import Logger


class NewStateDirectiveRuleService(IDirectiveRuleService):
    def __init__(self):
        super().__init__()

    def isLegal(self, targetPageId: str, beforeActionDom: str,
                afterActionDom="") -> bool:
        if afterActionDom == "":
            Logger().info("afterActionDom is empty string")
            return False

        form_submit_criteria = FormSubmitCriteriaSingleton.getInstance().getFormSubmitCriteria()

        dom_similarity = self.getDomSimilarity(beforeActionDom, afterActionDom)

        if dom_similarity == 100:
            return False

        if not form_submit_criteria or form_submit_criteria["verify"] == "page_compare":
            return not (dom_similarity == -1 or dom_similarity >= 95)
        elif form_submit_criteria["verify"] == "keyword":
            return not self._isDomContainKeyword(
                afterActionDom, form_submit_criteria["keyword"])
        else:
            raise Exception(
                f"Error in isLegal function, formSubmitCriteria: {form_submit_criteria}")

        #
        # taskID = targetPageId
        # mk_time = int(time.mktime(time.gmtime()))
        # fileManager = FileManager()
        # fileManager.createFolder("output/task_last_dom", f"{taskID}")
        # fileManager.createFile(path=os.path.join("output", "task_last_dom", f"{taskID}"), fileName=f"{mk_time}.html", context=afterActionDom)
        # fileManager.createFolder(os.path.join("output", "task_first_time_dom"), f"{taskID}")
        #
        # path = os.path.join("output", "task_first_time_dom", f"{taskID}")
        # files = [f for f in listdir(path) if isfile(join(path, f))]
        # try:
        #     max_ratio = -1
        #     if files:
        #         for f in files:
        #             with open(os.path.join(path, f)) as json_file:
        #                 elements = json.load(json_file)
        #             diff = difflib.SequenceMatcher()
        #             diff.set_seq1(afterActionElements)
        #             diff.set_seq2(elements)
        #             ratio = diff.ratio() * 100
        #             if ratio > max_ratio:
        #                 max_ratio = ratio
        #         if max_ratio < 95:
        #             fileManager.createFile(path=os.path.join("output", "task_first_time_dom", f"{taskID}"),
        #                                    fileName=f"{mk_time}.json", context=json.dumps(afterActionElements))
        #             if not self._isDomContainKeyword(afterActionDom):
        #                 return True
        #     else:
        #         if not self._isDomContainKeyword(afterActionDom):
        #             return True
        #
        # except Exception as ex:
        #     template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
        #     message = template.format(type(ex).__name__, ex.args)
        #     Logger().info(message)
        #     Logger().info("ERROR!!!")
        # return False

    def _getElements(self, dom):
        parser = etree.HTMLParser()
        doc = etree.parse(StringIO(dom), parser)

        elements = list()
        for el in doc.getroot().iter():
            tag = el.tag
            classes = el.get('class')
            text = re.sub('\\s', '', str(el.text))
            elements.append(f'{tag} {classes} {text}')

        return elements

    def _isDomContainKeyword(self, dom: str, keywords: list):
        # keywords = ['error', 'invalid', 'cannot', 'failed', 'not', 'taken', 'required', 'should', 'Must', 'at least']

        domTree = etree.parse(StringIO(dom), etree.HTMLParser())

        for word in keywords:
            elements = domTree.xpath(
                f"//*[contains(text(),'{word}') and not(self::script or self::style)]")
            if elements:
                Logger().info(f'Current state contain keyword: {word}')
                return True

        return False

    def getDomSimilarity(self, beforeActionDom: str, afterActionDom: str):
        beforeActionElements = self._getElements(beforeActionDom)
        afterActionElements = self._getElements(afterActionDom)

        domSimilarity = -1
        try:
            similarity = difflib.SequenceMatcher()
            similarity.set_seq1(beforeActionElements)
            similarity.set_seq2(afterActionElements)
            domSimilarity = similarity.ratio() * 100
        except Exception as ex:
            template = 'Error, An exception of type {0} occurred. Arguments:\n{1!r}'
            message = template.format(type(ex).__name__, ex.args)
            Logger().info(message)

        Logger().info(f"domSimilarity is: {domSimilarity}")
        return domSimilarity
