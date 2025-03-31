#!/bin/bash

xdg-open http://localhost:9999/index.html &
python -m http.server 9999
