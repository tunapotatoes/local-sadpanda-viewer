local-ex-viewer
=====================

Overview
---------------------
This provides a simple application for indexing and searching local copies of EX/EH galleries.
It works by searching the directories you provide for folders,
and then searching Sadpanda to find the matching gallery (if it can).
When it is done finding all of the galleries, it submits additional requests
using the actual API to download the metadata provided for each found gallery.
This metadata is then stored in the gallery folder under the name ".metadata.json"
and is then used to let you search your galleries.


How to use
---------------------
TODO

FAQ
---------------------
TODO


TODO
---------------------
Finish this README
Allow user to pick from multiple choices if no definite gallery is found.
Allow custom tagging/editing of galleries.
Add proper logging/debug options.
Present errors in the GUI.
Provide EH alternative.
Code cleanup.

