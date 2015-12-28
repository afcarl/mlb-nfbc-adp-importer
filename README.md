# mlb-nfbc-adp-importer

Collects NFBC ADP data from STATS's website for personal use.

## Installation

Clone this repository into (ideally) a fresh virtualenv
and install its requirements via `pip`:

```shell
$ git clone https://github.com/mattdennewitz/mlb-nfbc-adp-importer.git
$ cd mlb-nfbc-adp-importer
$ pip install -r requirements.txt
```

This will install Scrapy, a scraping backend.

## Usage

### Running the spider

To run the spider and generate a CSV formatted ranking list,
hop into the `nfbc` directory and run the spider using `scrapy crawl`:

```shell
$ cd nfbc
$ scrapy crawl nfbcadp -t csv -o nfbc-adp-2015.csv -a page_count=22
```

Note: If you'd like the standard JSON output, omit `-t` and change
      the extension of the filename given to `-o` to `.json`.
      Check the output of `scrapy crawl nfbcadp --help` for more information
      on available output formats.
      
Here, we tell the spider to crawl pages 1-22. STATS's pagination stops
on page 15 and resumes on page 16. We work around this by generating
a series of page numbers to define the collection of pages to crawl.

If you run without the `-a page_count` option, the spider will crawl
each position page, but miss some data. See below for more information.

#### Bonus

`csvkit` is a great way to peek at a CSV-formatted export from this spider.

```shell
$ cat nfbc-adp-2015.csv | csvcut -c 3-6 | csvsort -c 4 | csvlook | less
```

In this example, we're:

1. displaying the player name, team name, player position, and ADP
    (csv fields 3, 4, 5, and 6)
2. then, sorting by ADP
3. then, formatting the data as a table
4. then, paging the table with `less`

Read more about `csvkit` [here](https://csvkit.readthedocs.org/).

## Incomplete Data

STATS's ADP listings appear to have a gap between #724 and #749.
Read about this missing data [here](./nfbc/nfbc/spiders/nfbcadp.py#L22-L38).

## Closing thoughts

Don't hammer their site, be a jerk, or use their data in a way they would
not approve. This inevitably makes life harder for everyone else.
