# sniper

> kill targets across the globe.

Iterate over a CSV containing resource names, and delete them if they contain tags clearly indicating they want to be deleted.

Intended to consume CSVs as created by Tag Editor in global mode.

##  Overview

Using [Aws Resouce Groups and Tag Editor](https://aws.amazon.com/blogs/aws/resource-groups-and-tagging/), ops personel can find resources quickly and globally across all regions, by filtering on tags. Once a search result is returned, the user has the option of editing those tags.

For example, if I wanted to search all resources tagged with `project=devbox`, and then select all those matches where the `version=` tag was too old, I could do so. Then with the reslutant selection I could add a `deleteme=yes` tag. Now every obsolete AMI, snapshot, and instance across all regions is targetted for removal. I then export to CSV.

With CSV in hand, and the desire to delete the whole batch, I can use Sniper. Sniper double-checks that every resource it's targetting is indeed tagged with `deleteme=yes`. It will not delete unless that condition is met.

## Getting started

Install from pip:

```sh
$ pip install pz-sniper
```

Or install from source:

```sh
$ git clone git@github.com:parallelz-org/sniper.git
$ pip install .
```

(sudo may be required).

## Usage

To see help simply invoke with no arguments:

```sh
$ sniper
```

```text
usage: Sniper [-h] [-d] [-f FILE]

delete resources across regions in AWS

options:
  -h, --help            show this help message and exit
  -d, --delete          actually delete the resource (rather than dry-run)
  -f FILE, --file FILE  a CSV file with columns Identifier, Type, and Region

Sniper, by Parallelz
```

To point to a CSV, invoke sniper like so:

```sh
$ sniper --file /path/to/my/file.csv
```

That will do a dry run. When you're sure you want to actually delete, do this:

```sh
$ sniper --file /path/to/my/file.csv --delete
```

## Building

View `Makefile` to see what build options are available. To create a new release:

```sh
$ make clean    # deletes ./build and ./dist
$ make build    # runs python -m build
$ make publish  # if you have a valid token for pypi
```

## CSV format

The CSV file must have at least the following columns: Identifier, Type, Region. Example:

| Identifier              | Type      | Region       |
| ----------------------- | --------- | ------------ |
| snap-09072991f6df02736  | Snapshot  | sa-east-1    |
| ami-0bae32af2b8c59d4d   | Image     | ca-central-1 |
| i-0040ccd97ac3a6642     | Instance  | us-east-1    |
