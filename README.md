# Intro
Gitlab offers a convenient feature called `snippet` to store code fractions, but users only have a web interface to manage them. This little tool utilizes gitlab API to simplify that process. With it, you can do the following things with one click:
* check the snippets you have
* upload new snippets (and get a link to share with others)
* download any accessible snippets to a specified location

This tool is written in python2, but you can easily make it compatible with python3.

# Tutorial
## Set-up
1. Fill your git lab domain in `snippet.py` (`BASE_URL`). For UM's gitlab, for instance, it's https://gitlab.eecs.umich.edu

1. Generate your Access Token at {your gitlab domain}/profile/personal_access_tokens, and fill it in `snippet.py` (`TOKEN`)

1. Snippet visibility level is pre-set as `private`. You could change it to `internal` or `public` in `snippet.py` (`VISIBLE_LEVEL`).
**Notice: You have to change the visibility level for others to view or download your snippet, but pay attention to privacy issues!**

## Getting Started
1. upload
```
python snippet.py push a.cpp
# http://gitlab.eecs.umich.edu/snippets/2233
```
1. check
```
python snippet.py status
# http://gitlab.eecs.umich.edu/snippets/2233     a.cpp
```
*You will only see your snippets here*
1. download
```
python snippet.py pull 2233                     # download a.cpp to this dir
python snippet.py pull 2233 -f ~                # download a.cpp to ~
python snippet.py pull 2233 -f ~/b.cpp          # download a.cpp to ~ and rename as b.cpp
```
*You can download a snippet as long as you know the id and authorized to see it*
1. remove
```
python snippet.py rm 2233
```
1. update
```
python snippet.py update 2233 a.cpp
```

## Reference
1. Check existing snippets and get their ids
```
python snippet.py status
```

1. Upload a new snippet
```
python snippet.py push [local_file_path] -t [title] -m [description]
```
Title and description are optional. If not specified, title is the same as the file name. `local_file_path` could be relative or absolute.

1. Download an existing snippet
```
python snippet.py pull [snippet_id|snippet_url] -f [destination]
```
Destination is optional. It could be a directory or a file name (if you want a different name for the downloaded file). If not specified, a new file will be created in the current working directory.

1. Modify an existing snippet
```
python snippet.py update [snippet_id|snippet_url] [local_file_path] -t [title] -m [description]
```
Title and description are optional. `local_file_path` could be relative or absolute.

1. Delete an existing snippet
```
python snippet.py rm [snippet_id|snippet_url]
```
