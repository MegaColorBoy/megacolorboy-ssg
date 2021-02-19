#!/bin/bash
#currentDate=date +%F
echo "Begin deployment..."

sleep 2

echo "Generating all pages..."
python3.7 ssg.py build --mode all

sleep 2

mkdir -p ghpages

cp -r output/* ghpages/

git add .
git commit -m "deploying new changes"
git push -u origin master

echo "Site is ready. Check it out!"
