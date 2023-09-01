# GHutter

`GHutter` is a tool to recreate the history graph of a GitHub repository in Graphviz's Dot Language

## Install

`Ghutter` is available on PyPI

```bash
pip install ghutter
```

## Usage

```text
usage: python -m ghutter [-h] [-t TOKEN] [--max-commits MAXCOMMITS] [-d DOTOUTPUT] [-o DRAWOUTPUT] repository

'GHutter' is a tool to recreate the history graph of a GitHub repository in Graphviz's Dot Language

positional arguments:
  repository            github repository in format "owner/repository" or url

options:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        github personal access token
  --max-commits MAXCOMMITS
                        max number of commits to fetch from the history. If it is omitted it tries to fetch the whole
                        history (parents will always be shown)
  -d DOTOUTPUT, --dot-output DOTOUTPUT
                        graph dot file output path (default 'history.dot')
  -o DRAWOUTPUT, --draw-output DRAWOUTPUT
                        graph render output path (there may be several). Check 'Graphviz' supported formats on your
                        system
```

### Example

```bash
python -m ghutter -t <token> --max-commits 1000 -d history_graph.dot -o history.svg -o history.png archlinux/linux
```

## License

This project is licensed under the terms of the GPL-3.0 license.
