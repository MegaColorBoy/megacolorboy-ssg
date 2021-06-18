#!/bin/bash
sass templates/minimal-theme/scss/main.scss templates/minimal-theme/css/main.css --style=compressed
rm -rf output/static/css output/static/fonts output/static/vendor
cp -r templates/minimal-theme/css output/static/css
cp -r templates/minimal-theme/fonts output/static/fonts
cp -r templates/minimal-theme/vendor output/static/vendor
cp templates/minimal-theme/logo.png output/static/logo.png