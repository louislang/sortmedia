# sortmedia
![Actions Status](https://github.com/LouisLang/sortmedia/workflows/Python%20application/badge.svg)
![MIT License Badge](https://img.shields.io/github/license/LouisLang/sortmedia) 
![Coverage](https://github.com/LouisLang/sortmedia/blob/master/resources/coverage.svg)

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
## 
