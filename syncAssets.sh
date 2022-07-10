#!/bin/bash
sass templates/minimalist-v2/scss/main.scss templates/minimalist-v2/css/main.css --style=compressed
#sass templates/minimalist-v2/scss/resume.scss templates/minimalist-v2/css/resume.css --style=compressed
rm -rf output/static/css output/static/fonts output/static/vendor
cp -r templates/minimalist-v2/css output/static/css
cp -r templates/minimalist-v2/fonts output/static/fonts
cp -r templates/minimalist-v2/vendor output/static/vendor
cp templates/minimalist-v2/logo.png output/static/logo.png
