#!/usr/bin/env python
import requests
import time
import json
import random
from Logger import Logger
import Exceptions
import threading


class RequestClass(Logger):
    API_TIME_WAIT = 3
    API_RETRY_COUNT = 5
    API_TIME_REQ_DELAY = 3
    API_MAX_SEQUENTIAL_REQUESTS = 3
    API_TIME_TOO_FAST_WAIT = 100
    SEQ_TIME_DIFF = 10
    COOKIES = {"ipb_member_id": "", "ipb_pass_hash": ""}
    HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0"}  # No idea if this actually helps
    count = 0
    prevtime = 0
    lock = threading.Lock()

    @property
    def id(self):
        return self.COOKIES["ipb_member_id"]

    @id.setter
    def id(self, val):
        self.COOKIES["ipb_member_id"] = val

    @property
    def pwhash(self):
        return self.COOKIES["ipb_pass_hash"]

    @pwhash.setter
    def pwhash(self, val):
        self.COOKIES["ipb_pass_hash"] = val

    def rest(self, method, url, kwargs):
        try:
            self.lock.acquire()
            return self._rest(method, url, **kwargs)
        finally:
            self.lock.release()

    def _rest(self, method, url, **kwargs):
        retry_count = kwargs.pop("retry_count", self.API_RETRY_COUNT)
        payload = kwargs.pop("payload", None)
        if payload:
            payload = json.dumps(payload)
        while retry_count >= 0:
            gen_time_sleep = self.API_TIME_REQ_DELAY * random.randint(100, 200)/100
            time_diff = time.time() - self.prevtime
            if time_diff <= gen_time_sleep:
                time.sleep(gen_time_sleep)
            sequential = time_diff <= self.SEQ_TIME_DIFF
            if sequential and self.count >= self.API_MAX_SEQUENTIAL_REQUESTS:
                time.sleep(self.API_TIME_WAIT * random.randint(100, 200)/100)
                self.count = 0
            if sequential:
                self.count += 1
            self.logger.info("Sending %s request to %s with payload %s" %
                             (method, url, payload))
            self.prevtime = time.time()
            response = getattr(requests,
                               method)(url, data=payload, headers=self.HEADERS,
                                       cookies=self.COOKIES, **kwargs)
            # except TypeError:
            #     response = getattr(requests,
            #                        method)(url, cookies=self.COOKIES, **kwargs)
            if self.validate_response(response):
                break
            else:
                retry_count -= 1
                self.logger.warning(
                    "Request failed, retry with %s tries left." % retry_count)
        if not retry_count >= 0:
            self.logger.warning("Request ran out of retry attempts.")
            return
        try:
            return response.json()
        except ValueError:
            pass
        if "text/html" in response.headers["content-type"]:
            return response.text
        else:
            return response

    def validate_response(self, response):
        content_type = response.headers["content-type"]
        assert response is not None
        self.logger.debug("Response: %s" % response)
        self.logger.debug("Response headers: %s" % response.headers)
        if response.status_code != 200:
            self.logger.warning("Error code: %s")
            return False
        if "image/gif" in content_type:
            raise(Exceptions.BadCredentialsError())
        if "text/html" in content_type and "You are opening" in response.text:
            self.logger.info("Detected that we are overloading SP. Waiting for %s seconds" %
                             self.API_TIME_TOO_FAST_WAIT)
            time.sleep(self.API_TIME_TOO_FAST_WAIT)
            return False
        if "text/html" in content_type and "Your IP address" in response.text:
            raise(Exceptions.UserBannedError())
        try:
            if response.json().get("error") is not None:
                self.logger.warning("Got error message %s" %
                                    response.json().get("error"))
                return False
        except ValueError:
            pass
        return True

    def get(self, *args, **kwargs):
        return self.rest("get", *args, **kwargs)


    def post(self, *args, **kwargs):
        return self.rest("post", *args, **kwargs)


RequestManager = RequestClass()
del RequestClass
