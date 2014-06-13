#!/usr/bin/python2
import os
import hashlib
import json
import search
import io


class LocalGallery(object):
    def __init__(self, path):
        config_file = open("config.json")
        config = json.load(config_file)
        config_file.close()
        self.WebGallery = None
        self.exts = config["exts"]
        self.hash_size = config["hash_size"]
        self.path = os.path.expanduser(path)
        self.title = os.path.normpath(self.path).split(os.sep)[-1]
        self.metadata_file = os.path.join(self.path, ".metadata.json")
        self._find_files()
        if not self.has_metadata():
            self._search()
        else:
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
        local_metadata = {"gmetadata": {}}
        local_metadata["gmetadata"] = metadata
        metadata_file = open(self.metadata_file, "w")
        json_data = json.dumps(local_metadata, ensure_ascii=False).encode("utf8")
        metadata_file.write(json_data)

    def _find_files(self):
        self.files = []
        for path, dirs, files in os.walk(self.path):
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext in self.exts:
                    self.files.append(os.path.join(self.path, f))
            return
        if len(self.files) == 0:
            print("No images found.")

    def _search(self):
        if len(self.files) == 0:
            return
        sha1 = hashlib.sha1()
        with open(self.files[0], "rb") as image:
            buff = image.read(self.hash_size)
            while len(buff) > 0:
                sha1.update(buff)
                buff = image.read(self.hash_size)
        sha_hash = sha1.hexdigest()
        hash_search = search.WebSearch(sha_hash=sha_hash, silent=True)
        if len(hash_search.result_urls) == 1:
            self.WebGallery = WebGallery(url=hash_search.result_urls[0])
            return
        title_search = search.WebSearch(title=self.title, silent=True)
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
            print("No definite gallery found, picking first.")
            self.WebGallery = WebGallery(url=hash_search.result_urls[0])


class WebGallery(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get("url", None)
        self.gallery_id = kwargs.get("gallery_id", "")
        self.gallery_token = kwargs.get("gallery_token", "")
        if self.url is not None:
            self.__process_url()
        self.gid = [self.gallery_id, self.gallery_token]

    def __process_url(self, **kwargs):
        split_url = self.url.split("/")
        self.gallery_id = split_url[-3]
        self.gallery_token = split_url[-2]


if __name__ == "__main__":
    #LocalGallery("(774) together with my sisters (girls for m vol. 5) [eng]")
    #x = LocalGallery("~/Pictures/djs/", "(774) Together With My Sisters (Girls For M Vol. 5) [ENG]")
    pass
