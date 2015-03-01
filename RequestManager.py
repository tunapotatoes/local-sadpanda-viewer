#!/usr/bin/env python
import requests
import time
import json
from Logger import Logger
import Exceptions


class RequestClass(Logger):
    API_TIME_WAIT = 5
    API_RETRY_COUNT = 10
    API_TIME_REQ_DELAY = 5
    API_MAX_SEQUENTIAL_REQUESTS = 5
    API_TIME_TOO_FAST_WAIT = 100
    COOKIES = {"ipb_member_id": "", "ipb_pass_hash": ""}
    count = 0

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

    def _rest(self, method, url, **kwargs):
        retry_count = kwargs.pop("retry_count", self.API_RETRY_COUNT)
        payload = kwargs.pop("payload", None)
        if payload:
            payload = json.dumps(payload)
        while retry_count >= 0:
            time.sleep(self.API_TIME_REQ_DELAY)
            if self.count >= self.API_MAX_SEQUENTIAL_REQUESTS:
                time.sleep(self.API_TIME_WAIT)
                self.count = 0
            self.count += 1
            self.logger.info("Sending %s request to %s with payload %s" %
                             (method, url, payload))
            try:
                response = getattr(requests,
                                   method)(url, data=payload,
                                           cookies=self.COOKIES, **kwargs)
            except TypeError:
                response = getattr(requests,
                                   method)(url, cookies=self.COOKIES, **kwargs)
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

    def __getattr__(self, name):
        if name is "name":  # Oh god I need to fix this
            raise AttributeError

        def handler(*args, **kwargs):
            return self._rest(name, *args, **kwargs)
        return handler


RequestManager = RequestClass()
del RequestClass
