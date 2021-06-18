#!/bin/bash
#currentDate=date +%F
echo "Begin deployment..."

sleep 2

echo "Generating all pages..."
python ssg.py build --mode all

sleep 2

# mkdir -p ghpages

cp -r output/* ghpages/

cd ghpages

git add .
git commit -m "deploying new changes"
git push -u origin master

cd ..

echo "Site is ready. Check it out!"
