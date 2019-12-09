# sortmedia
![Actions Status](https://github.com/LouisLang/sortmedia/workflows/Python%20application/badge.svg)
![MIT License Badge](https://img.shields.io/github/license/LouisLang/sortmedia) 
[![Coverage Status](https://coveralls.io/repos/github/LouisLang/sortmedia/badge.svg?branch=master)](https://coveralls.io/github/LouisLang/sortmedia?branch=master)
[![GitHub issues](https://img.shields.io/github/issues/LouisLang/sortmedia)](https://github.com/LouisLang/sortmedia/issues)

Dedupe and sort images and video files based on their creation date. 

![Image of Sorted Files](https://github.com/LouisLang/sortmedia/blob/master/resources/demo.png)

* Handles images and video files.
* Support for `heic` files (common iOS format).
* Supports excluding directories.
* Removes duplicates based on file hash.
* Organizes files into `year/month/day/files.ext`.

## Installation
`pip install sortmedia`

## Command Line Usage
### Sorting a directory of media files, *move* to destination directory.
Basic usage - processing a directory of media files `foo` and moving them to the destination directory `bar`.

`sortmedia foo bar`

### Sorting a directory of media files, *copy* to destination directory.
Instead of moving files (the default), copy the files leaving the source directory `foo` intact. 

`sortmedia -c foo bar`

or 

`sortmedia --copy foo bar`

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

`sortmedia --exclude=foo/ignoreMe,foo/ignoreMeToo foo/ bar/`

### Skip processing for a specified directory - but still move/copy.
If you have directories that are already sorted, that you'd like to skip processing but still move or copy you can mark them as "no process" directories. Assuming the following directory structure:

```
foo/
  alreadySorted/
  img1.jpg
  img2.png
  ...
```

`sortmedia --noprocess=foo/alreadySorted/ foo/ bar/`

This will result in `alreadySorted/` being moved to `bar/` without analyzing the files under that directory.

## Programmatic Usage
The primary interface into `sortmedia` is the `SortMedia` class. This class can be instantiated and used as follows:

```
from sortmedia.sort import SortMedia
sort = SortMedia()
sort.process('src/', 'dst/')
```

This will process media in `src/` and move the files to `dst/`.

### Copying instead of moving
You can set the sorter to `copy` rather than `move` (which is the default):

```
from sortmedia.sort import SortMedia
sort = SortMedia(copy=True)
```

### Specifying directories to ignore
Lets say you have a directory of photos, `photos/`, with two directories you want to completely ignore: `ignoreMe` and `ignoreMeToo`.

```
from sortmedia.sort import SortMedia
sort = SortMedia(excludes=['photos/ignoreMe', 'photos/ignoreMeToo'])
```

### Move/copy but do not process directory
In some instances you might have a directory of media (e.g. `photos/birthday-photos/`) that you want to move or copy to the destination directory without processing the files in the directory. You can achieve this by passing a list of directories in the `noprocess` parameter.

```
from sortmedia.sort import SortMedia
sort = SortMedia(noprocess=['photos/birthday-photos/`])
```
