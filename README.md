# Fanserials parser for IPTV

## Overview
Parser to store seasons, episodes in mysql db. 

## Requirements
- Python 3.6.2
- mysql
- docker

## Usage

```bash
# docker build -t ottplayer .
# docker run --rm ottplayer python manage.py parse --seasons
# docker run --rm ottplayer python manage.py parse --episodes
# docker run --rm ottplayer python manage.py save
```
