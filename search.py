#!/usr/bin/python2
import json
import time
import requests
import BeautifulSoup


class WebSearch(object):
    def __init__(self, **kwargs):
        config_file = open("config.json")
        config = json.load(config_file)
        config_file.close()
        self.cookies = config["cookies"]
        self.base_url = config["base_url"]
        self.time_delay = config["API_TIME_WAIT"]
        self.result_urls = []
        self._search(**kwargs)

    def _search(self, **kwargs):
        silent = kwargs.get("silent", False)
        page_num = kwargs.get("page_num", 0)
        num_pages = kwargs.get("num_pages", None)
        sha_hash = kwargs.get("sha_hash", "")
        title = kwargs.get("title", "")
        filtered_title = clean(title)
        url = self.base_url % (filtered_title, sha_hash, page_num)
        request = requests.get(url, cookies=self.cookies)
        if not validate_request(request):
            print("Search failed.")
            return None
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
                answer = raw_input("%s pages of results found.\n"
                                   "In order to prevent you from getting "
                                   "banned,\nthere is a %s second delay "
                                   "between each page request. \n"
                                   "Do you want to continue? " %
                                   ((num_pages + 1), self.time_delay))
                if answer.lower() != "y" and answer.lower() != "yes":
                    return
            kwargs["num_pages"] = num_pages
        if page_num >= num_pages:
            return
        if page_num == 0:
            kwargs["page_num"] = 1
        else:
            kwargs["page_num"] += 1
        time.sleep(self.time_delay)
        self.search(**kwargs)


def validate_request(request):
    if request.status_code != 200:
        print("REQUESTS: Error code %s" % request.status_code)
        return False
    if request.headers["content-type"] == "image/gif":
        print("Error, bad credentials. Sad panda detected.")
        return False
    if (request.headers["content-type"] == "application/json" and
       request.json().get("error", False)):
        print("Obtained error: %s" % request.json()["error"])
        return False
    return True


def clean(string):
    "Removes chars that cause problems with ex"
    banned_chars = ["=", "-", ":"]
    for char in banned_chars:
        string = string.replace(char, "")
    return string


if __name__ == "__main__":
    s = WebSearch("(774) together with my sisters (girls for m vol. 5) [eng]")
