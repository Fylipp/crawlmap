# crawlmap

A simple web crawler. Data is persisted into [neo4j](https://neo4j.com).

## Output format

### `Page` node

Unique pages.

| Key  | Type    | Description                                             |
| ---- | ------- | ------------------------------------------------------- |
| root | Boolean | Whether this page was used as a crawling starting point |
| url  | Text    | Absolute page URL                                       |
| used | Boolean | Whether the page has already been requested             |
| code | Numeric | The status code or `0` if aborted or timeout            |

### `REFERENCES` relationship

Individual links between pages.

## Usage

### Install dependencies

```
pip install -r requirements.txt
```

### Configure behaviour

Edit `crawlmap.ini` to configure the neo4j connection, web access settings and crawl limits.

### Run

Usage is as follows:

```
./crawlmap-cli.py [<ROOT_URL> ...]
```

For example:

```
./crawlmap-cli.py https://github.com https://news.ycombinator.com/
```

