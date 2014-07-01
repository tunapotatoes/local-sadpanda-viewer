local-sandpanda-viewer
=====================

Overview
---------------------
This provides a simple application for indexing and searching local copies of
EX/EH galleries. It works by searching the directories you provide for folders,
and then searching Sadpanda to find the matching gallery (if it can).
When it is done finding all of the galleries, it submits additional requests
using the actual API to download the metadata provided for each found gallery.
This metadata is then stored in the gallery folder under the name
".metadata.json" and is then used to let you search your galleries.


How to use
---------------------
The lefthand column is the control panel for this program.
To start with, enter your member ID and password hash in their respective
fields. If you do not have these, download a cookie manager for the browser
of your choice and look for the values "ipb_member_id" and "ipb_pass_hash"
under the EX domain. After that, enter the path or paths to where you keep your
manga/doujinshi and hit submit.

Because this is the first time you are running the program, you will have to
get the metadata for all of the galleries. To do this, click the box marked
"Get metadata for new galleries." and press the respective submit button This
can take a long time, and is entirely the fauly of EX/EH - they are swift to ban
for too many requests sent in a short period of time. Because of this, I have
limited the number of requests to a very, very conservative amount - you will
not get banned running this program. Well, probably not.

Depending on the size of your gallery it could take a very long time to
complete, so I would suggest leaving the program running in the background and
do something else in the meantime.

When the program is finished, you will see all of the galleries that the program
was able to detect and find displayed. You can then search for tags or titles,
just like in EX/EH. You can use quotes or underscores for multi-word tags, and
"-" preceding a tag to filter out galleries with that tag. The one missing
feature that probably will not be added is the ability to search tags by
gender/type (E.G female:tag, male:tag).


FAQ
---------------------
### Will this get me banned?

It shouldn't. The request limiter is very careful and should never result in a
ban. The only time you could possibly get banned using this is if you ran
multiple copies of this on the same network, or were agressively browsing EX/EH
while the program is running.


### Why is it so slow?

So you don't banned, see above.


### What are the different gallery options for?

"Search directories for galleries" will search your specified directories for
all galleries in it. Ones that have metadata will be displayed. Use this if you
ever move galleries into a specified directory.

"Get metadata for new galleries" will try to get the metadata for galleries
which don't have any. This should be your primary function.

"Reobtain all gallery information" will try to get the metadata for all
galleries, regardless of whether they have metadata already or not. Use with
caution, this will take a long time for large collections.


### The program is displaying the wrong tags/title for a gallery!

Please send me information regarding that gallery (a link). Note that I don't
consider getting a different language gallery as a mistake (E.G if your gallery
is in English and I get the tags for the Chinese version that isn't an
error/mistake).


### The program is showing the wrong image for a gallery!

The image displayed is the first image in the gallery, ignoring case.
Remove/rename the offending file. And complain to whoever did the naming for
that gallery.


### The program failed to display a gallery!

This means it failed to find it on EX/EH. There are a few reasons for this, but
to determine if it is a bug I need details.


The software should be considered alpha. Please be a good guinea pig and send me
lots and lots of sample data/problems. It can be hard to test for all possible
weirdness. All bug/issues should be logged on Github.


TODO
---------------------
Finish this README

Improve progress bar.

Allow user to pick from choices if no definite gallery is found.

Allow custom tagging/editing of galleries.

Add proper logging/debug options.

Present errors in the GUI.

Provide EH alternative.

Code cleanup. (Yeah right.)

