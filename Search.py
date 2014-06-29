#!/usr/bin/python2
import time
import json
import BeautifulSoup


class WebSearch(object):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.result_urls = []
        self._search(**kwargs)

    def _search(self, **kwargs):
        silent = kwargs.get("silent", False)
        page_num = kwargs.get("page_num", 0)
        num_pages = kwargs.get("num_pages", None)
        sha_hash = kwargs.get("sha_hash", "")
        title = kwargs.get("title", "")
        url = (self.parent.config["base_url"] %
               (title, sha_hash, page_num))
        request = self.parent.request_object.request(url, "get")
        html_results = BeautifulSoup.BeautifulSoup(request.text)
        results = html_results.findAll("div", {"class" : "it5"})
        for result in results:
            self.result_urls.append(result.a.attrs[0][1])
        if num_pages is None:
            pages = html_results.find("table", "ptt")
            if pages is None:
                return
            try:
                num_pages = int(pages.findAll("a")[-2].contents[0]) - 1
            except IndexError:
                num_pages = 0
            if num_pages > 0:
                if silent:
                    return
                # Probably should just delete this shit since I'm not going to
                # support a console mode
                answer = raw_input("%s pages of results found.\n"
                                   "In order to prevent you from getting "
                                   "banned,\nthere is a %s second delay "
                                   "between each page request. \n"
                                   "Do you want to continue? " %
                                   ((num_pages + 1),
                                    self.parent.config["API_TIME_WATI"]))
                if answer.lower() != "y" and answer.lower() != "yes":
                    return
            kwargs["num_pages"] = num_pages
        if page_num >= num_pages:
            return
        if page_num == 0:
            kwargs["page_num"] = 1
        else:
            kwargs["page_num"] += 1
        self.search(**kwargs)

