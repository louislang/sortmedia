# Mediasort
Dedupe and sort images and video files based on their creation date. Includes facilities for handling `heic` files (common on iOS), excluding directories and skipping processing for directories.

## Installation
`pip install mediasort`

or

`python setup.py`

## Command Line Usage
### Sorting a directory of media files, *move* to destination directory.
Basic usage - processing a directory of media files `foo` and moving them to the destination directory `bar`.

`python sort.py foo bar`

### Sorting a directory of media files, *copy* to destination directory.
Instead of moving files (the default), copy the files leaving the source directory `foo` intact. 

`python sort.py -c foo bar`

or 

`python sort.py --copy foo bar`

### Exclude directory
You can list a set of directories that we should completely ignore. Assuming the following directory structure:

```
foo/
  ignoreMe/
  ignoreMeToo/
  img1.jpg
  img2.png
  ...
```

`python sort.py --exclude=foo/ignoreMe,foo/ignoreMeToo foo/ bar/`

### Skip processing for a specified directory - but still move/copy.
If you have directories that are already sorted, that you'd like to skip processing but still move or copy you can mark them as "no process" directories. Assuming the following directory structure:

```
foo/
  alreadySorted/
  img1.jpg
  img2.png
  ...
```

`python sort.py --noprocess=foo/alreadySorted/ foo/ bar/`

This will result in `alreadySorted/` being moved to `bar/` without analyzing the files under that directory.

## Programmatic Usage
## 
