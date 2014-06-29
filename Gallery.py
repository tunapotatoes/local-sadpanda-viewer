#!/usr/bin/python2
import os
import hashlib
import json
import io
import re
import Search

class LocalGallery(object):
    def __init__(self, parent, path, **kwargs):
        self.parent = parent
        self.C_QGallery = None
        self.WebGallery = None
        self.needed_metadata = True
        self.files = []
        self.path = os.path.expanduser(path)
        self.title = os.path.normpath(self.path).split(os.sep)[-1]
        self.metadata_file = os.path.join(self.path, ".metadata.json")
        self._find_files()
        #if not self.has_metadata():
        #    self._search()
        if self.has_metadata():
            self.needed_metadata = False
            self.local_metadata = self.load_metadata()
            self.WebGallery = WebGallery(gallery_id=self.local_metadata["gmetadata"]["gid"],
                                         gallery_token=self.local_metadata["gmetadata"]["token"])

    def has_metadata(self):
        return os.path.exists(self.metadata_file)

    def load_metadata(self):
        metadata_file = io.open(self.metadata_file, "r", encoding="utf-8")
        local_metadata = json.load(metadata_file)
        metadata_file.close()
        if type(local_metadata) is not dict:
            local_metadata = {}
        if type(local_metadata.get("gmetadata", None)) is not dict:
            local_metadata["gmetadata"] = {}
        return local_metadata

    def save_metadata(self, metadata):
        clean_metadata(metadata)
        local_metadata = {"gmetadata": {}}
        local_metadata["gmetadata"] = metadata
        metadata_file = open(self.metadata_file, "w")
        json_data = json.dumps(local_metadata,
                               ensure_ascii=False).encode("utf8")
        metadata_file.write(json_data)
        metadata_file.close()

        
    def _find_files(self):
        temp_files = []
        for path, dirs, files in os.walk(self.path):
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext in self.parent.config["exts"]:
                    temp_files.append(os.path.join(self.path, f))
            break
        self.files = sorted(temp_files, key=lambda f: f.lower())

    def search(self, **kwargs):
        self._search()
        if self.has_metadata():
            self.local_metadata = self.load_metadata()


    def _search(self):
        if len(self.files) == 0:
            return
        sha1 = hashlib.sha1()
        with open(self.files[0], "rb") as image:
            buff = image.read(self.parent.config["hash_size"])
            while len(buff) > 0:
                sha1.update(buff)
                buff = image.read(self.parent.config["hash_size"])
        sha_hash = sha1.hexdigest()
        hash_search = Search.WebSearch(self.parent, sha_hash=sha_hash,
                                       silent=True)
        print "Len hash: %s" % str(len(hash_search.result_urls))
        print hash_search.result_urls
        if len(hash_search.result_urls) == 1:
            self.WebGallery = WebGallery(url=hash_search.result_urls[0])
            return
        title = clean(self.title)
        title_search = Search.WebSearch(self.parent, title=title, silent=True)
        print "Title: %s\nLen: %s" % (title, str(len(title_search.result_urls)))
        if len(hash_search.result_urls) == 0:
            if len(title_search.result_urls) == 0:
                print("No galleries found.")
                return
            if len(title_search.result_urls) == 1:
                self.WebGallery = WebGallery(url=title_search.result_urls[0])
                return
        else:
            for hash_url in hash_search.result_urls:
                if hash_url in title_search.result_urls:
                    self.WebGallery = WebGallery(url=hash_url)
                    return
            print("For %s" % self.title)
            print("No definite gallery found, picking first.")
            self.WebGallery = WebGallery(url=hash_search.result_urls[0])


class WebGallery(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get("url", None)
        self.gallery_id = kwargs.get("gallery_id", "")
        self.gallery_token = kwargs.get("gallery_token", "")
        if self.url is not None:
            self._process_url()
        self.gid = [self.gallery_id, self.gallery_token]

    def _process_url(self, **kwargs):
        split_url = self.url.split("/")
        self.gallery_id = split_url[-3]
        self.gallery_token = split_url[-2]

    def validate_data(self, metadata):
        gid = metadata["gid"]
        token = metadata["token"]
        return (self.gallery_id, self.gallery_token) == (str(gid), str(token))
    

def clean(string):
    "Removes chars that cause problems with ex"
    banned_chars = ["=", "-", ":", "|", "~", "+", "]", "[", ".", ","]
    string = re.sub(r'\([^)]*\)', ' ', string)
    string = re.sub(r'\{[^}]*\}', ' ', string)
    #string = re.sub(r'\[[^]]*\]', ' ', string)
    for char in banned_chars:
        string = string.replace(char, " ")
    return string

def clean_metadata(metadata):
    for key in metadata.keys():
        if type(metadata[key]) == dict:
            self.clean(metadata[key])
        elif type(metadata[key]) == list:
            for i in range(len(metadata[key])):
                metadata[key][i] = re.sub("&#(\d+)(;|(?=\s))", "", metadata[key][i])
                metadata[key][i] = re.sub("(&amp;)", "&", metadata[key][i])
        elif type(metadata[key]) == unicode:
            metadata[key] = re.sub("&#(\d+)(;|(?=\s))", "", metadata[key])
            metadata[key] = re.sub("(&amp;)", "&", metadata[key])
