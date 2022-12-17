#!/bin/bash
#currentDate=date +%F
echo "Begin deployment..."

sleep 2

echo "Generating all pages..."
python ssg.py build --mode all

echo "Exporting RSS Feed..."
python ssg.py export-rss-feed

echo "Exporting JSON file..."
python ssg.py export-as-json

sleep 2

# mkdir -p ghpages

echo "Copying static files to staging directory..."
cp -r output/* ghpages/

cd ghpages

echo "Pushing changes to GitHub repo..."

git add .
git commit -m "deploying new changes"
git push -u origin master

cd ..

echo "Site is ready. Check it out!"