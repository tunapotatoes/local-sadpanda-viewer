#!/usr/bin/python2
import requests
import json
import time

class RequestObject():
    def __init__(self, parent=None):
        self.count = 0
        self.parent = parent
        
    def request(self, url, mode="get", data=None):
        time.sleep(self.parent.config["API_TIME_REQ_DELAY"])
        redo_count = 10
        if self.count >= self.parent.config["API_MAX_SEQUENTIAL_REQUESTS"]:
            time.sleep(self.parent.config["API_TIME_WAIT"])
            self.count = 0
        self.count += 1
        if mode == "get":
            while redo_count > 0:
                request = requests.get(url,
                                       headers=self.parent.config["HEADERS"],
                                       cookies=self.parent.config["COOKIES"])
                if self.validate_request(request):
                    break
                else:
                    redo_count -= 1
        if mode == "post":
            while redo_count > 0:
                request = requests.post(url, json.dumps(data),
                                        headers=self.parent.config["HEADERS"],
                                        cookies=self.parent.config["COOKIES"])
                if self.validate_request(request):
                    break
                else:
                    redo_count -= 1
        if not redo_count > 0:
            print("Redo count limit.")
            
        return request

    def validate_request(self, request):
        content_type = request.headers["content-type"]
        print content_type
        if request.status_code != 200:
            print("REQUESTS: Error code %s" % request.status_code)
            return False
        if content_type == "image/gif":
            print("Error, bad credentials. Sad panda detected.")
            return False
        if content_type == "text/html" and "You are opening" in request.text:
            self.overload(request.text)
            return False
        if content_type == "text/html" and "Your IP address" in request.text:
            raise(self.Banned(request.text))
        try:
            if request.json().get("error", None) is not None:
                print("Obtained error: %s" % request.json()["error"])
                return False
        except:
            pass
        return True

    def overload(self, text):
        print(text)
        time.sleep(self.parent.config["API_TIME_TOO_FAST_WAIT"])
        
    class Banned(Exception):
        def __init__(self, msg):
            self.msg = "We have detected that you are banned.\n%s" % msg
