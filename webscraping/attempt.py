from urllib import request
import re

class Scrap():
      
    url = 'https://docs.python.org/3.8/index.html'
    root_pattern = '<p class="biglink">[\s\S]*?</p>'
    biglink_pattern = '<a class="biglink" href=[\s\S]*?</a>'
    linkdescr_pattern = '<span class="linkdescr">[\w\W]*?</span>'

    def __fetch_content(self):
        content = request.urlopen(Scrap.url).read()
        htmls = str(content, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        biglinks = []
        root_html = re.findall(Scrap.root_pattern, htmls)
        for html in root_html:
            biglink = re.findall(Scrap.biglink_pattern, html)
            linkdescr = re.findall(Scrap.linkdescr_pattern, html)
            des_dict = {'header': biglink, 'descr': linkdescr}
            biglinks.append(des_dict)
        print(biglinks[1])
        a = 1

    def go(self):
        htmls = self.__fetch_content()
        self.__analysis(htmls)

scrap = Scrap()
scrap.go()
