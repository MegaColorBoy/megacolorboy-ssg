"""
Author: Abdush Shakoor
megacolorboy-ssg: A simple static site generator written in Python 3
Updated on: 19-02-2021
"""

#!/usr/bin/env python3

import os, random, sys
from glob import glob
import json
from datetime import datetime, date
from dateutil.parser import parse
from jinja2 import Environment, PackageLoader
from markdown2 import markdown
import typer
from time import sleep
from progress.bar import IncrementalBar
from itertools import islice, groupby
import shutil
import re
import bs4
from bs4 import BeautifulSoup
import subprocess
import ssgconfig as cfg

# Using Typer as the CLI tool
app = typer.Typer()

# Jinja2 Environment
env = Environment(loader=PackageLoader('ssg','templates/' + cfg.site['theme']))

# Generate JSON dump
def generateJSON(section):
    posts = section['posts']
    
    jsonData = {
        'posts': []
    }
    
    for post in posts:
        jsonData['posts'].append(post)
    
    jsonDirectory = 'output/json/'
    createDirectory(jsonDirectory)
    
    with open(jsonDirectory + section['directory'] + '.json', 'w') as file:
        json.dump(jsonData, file)
    

# Generate RSS Feed in XML
def generateRSS(section):
    posts = section['posts']

    postUrl = "posts"

    if not section['root']:
        postUrl = '/'.join([section['directory'], "posts"])

    xmlDirectory = 'output/rss/'
    createDirectory(xmlDirectory)

    xmlItems = []

    for post in posts:
        title = post['title']
        link = '/'.join([cfg.site['url'], postUrl, post['slug']])
        date = post['dateRaw']
        summary = post['summary']

        xmlItems.append("""
            <item>
                <title>{title}</title>
                <link>{link}</link>
                <guid isPermaLink="true">{link}</guid>
                <pubDate>{date}</pubDate>
                <description>{summary}</description>
            </item>
        """.format(title=title, link=link, date=date, summary=summary)
        )
    
    rssTitle = ' | '.join([section['seoTitle'], cfg.site['name']])
    rssLink = cfg.site['url'] if section['root'] else '/'.join([cfg.site['url'], section['directory']])
    rssDescription = section['seoDescription']

    xml = """
      <?xml version="1.0" encoding="UTF-8"?>
      <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
        <channel>
            <title>{title}</title>
            <link>{link}</link>
            <description>{description}</description>
            <atom:link href="{link}" rel="self" type="application/rss+xml" />'
            {items}
        </channel>
       </rss>
    """.format(title=rssTitle, link=rssLink, description=rssDescription, items=''.join(xmlItems).strip())

    filepath = xmlDirectory + section['directory'] + '.xml'
    writeToFile(filepath, xml.strip().encode('utf-8'))

# Format date in YYYY-MM-DD
def convertToRawDate(dateTimeStr: str):
    return "{0.year}-{0:%m}-{0:%d}".format(parse(dateTimeStr))

# Get posts required to render
# archiveMode is a flag to check if posts can be created in archive mode
def getPosts(section=""):
    
    # List of posts
    posts = []
    
    # Refer to https://github.com/trentm/python-markdown2/wiki/Extras for documentation
    extras = ['metadata', 'fenced-code-blocks']
    
    # Index of the section
    index = findIndex(cfg.sections, "directory", section)

    # Directory where all the content is stored

    if 'multiple' in cfg.sections[index]:
        paths = []
        for directory in cfg.sections[index]['multiple']:
            paths.append("content/" + directory)
    else:
        paths = ["content/" + section]
    
    # Look for Markdown file recursively in the specified directory
    with IncrementalBar('Processing...', suffix='%(percent)d%%') as bar:
        for path in paths:
            for root, directories, files in os.walk(path):
                for post in files:
                    filepath = os.path.join(root, post)
                    if post.endswith('.md'):
                        with open(filepath, 'r') as file:
                            postContent = markdown(file.read(), extras=extras)
                            
                            # Fetch metadata of each article
                            title = postContent.metadata['title']
                            postDate = postContent.metadata['date']
                            dateRaw = convertToRawDate(postContent.metadata['date'])
                            dateAlt = "{0:%d}.{0:%m}.{0.year}".format(parse(postContent.metadata['date']))
                            postYear = datetime.fromisoformat(dateRaw).strftime("%Y")
                            slug = postContent.metadata['slug']
                            category = postContent.metadata['category']
                            # summary = postContent.metadata['summary'] if 'summary' in postContent.metadata else 'Tips & Tricks &mdash; ' + category
                            summary = postContent.metadata['summary'] if 'summary' in postContent.metadata else "".join(filterText(extractText(postContent)))
                            readingTime = estimateReadingTime(postContent)
                            postUrl = '/'.join([section, 'posts', slug])

                            # if the status is not present in the file, it's assumed that the post is active.
                            status = postContent.metadata['status'] if 'status' in postContent.metadata else 'active'
                            
                            # Only active posts must be stored
                            if status == 'active':
                                posts.extend([
                                    {
                                        'section': root,
                                        'title': title,
                                        'link': postUrl,
                                        'date': postDate,
                                        'dateAlt': dateAlt,
                                        'year': postYear,
                                        'dateRaw': dateRaw,
                                        'slug': slug,
                                        'category': category,
                                        'summary': summary,
                                        'readingTime': readingTime,
                                        'filename': filepath,
                                        'status': status,
                                        'content': postContent,
                                    }
                                ])
                            bar.next()

    # sort posts by filename and date
    posts = sorted(posts, key=lambda x: (x['filename'], x['dateRaw']), reverse=True)
    return posts

# Archive mode
def archivePosts(posts):
    return [list(group) for _, group in groupby(sorted(posts, key=lambda x: x['dateRaw'], reverse=True), key=lambda y: datetime.fromisoformat(y['dateRaw']).strftime("%Y"))]

# Generate index page with pagination links
def generateIndexWithPaginator(section, postsPerPage):
    
    # Template required for pagination
    template = env.get_template(section['template']['paginationIndex'])

    # Total number of posts per section
    totalPosts = len(section['posts'])
    
    # Number of pagination links to generate
    numberOfPages = int(totalPosts/postsPerPage)

    # Create a directory to store the pagination links (By default, it's root)
    rootDirectory = 'output/'

    # If the current section is not root, then create it as a subdirectory instead.
    if not section['root']: 
        rootDirectory = 'output/' + section['directory'] + '/'

    createDirectory(rootDirectory)    

    """
    Split the posts in even chunks
    """
    it = iter(section['posts'])
    chunkedPosts = list(iter(lambda: tuple(islice(it, postsPerPage)), ()))

    for pageNumber in range(0, numberOfPages + 1):
        currentPageNumber = pageNumber + 1
        
        subDirectory = ''
        
        # Don't create a subdirectory for the first page        
        if currentPageNumber > 1:
            subDirectory = 'pages/{page}/'.format(page=currentPageNumber)
            createDirectory(rootDirectory + subDirectory)
        
        # Path of the index page for each pagination link
        pageFile = ''.join([rootDirectory, subDirectory, 'index.html'])

        # Create links for previous and next pages
        prevPage = 0 if currentPageNumber == 1 else currentPageNumber-1
        nextPage = 0 if currentPageNumber == numberOfPages+1 else currentPageNumber+1

        # Render the page
        renderedHtml = template.render(
            bodyClass="",
            posts=chunkedPosts[pageNumber],
            curr=currentPageNumber,
            prev=prevPage,
            next=nextPage,
            total=numberOfPages+1,
            page = {
                'title': section['seoTitle'], 
                'description': section['seoDescription']
            }, 
            site = cfg.site, 
            menu = cfg.menu
        )

        writeToFile(pageFile, renderedHtml.encode('utf-8'))

# Generate index page without pagination links
def generateIndexWithoutPaginator(section):
    template = env.get_template(section['template']['index'])
    renderedHtml = template.render(
        bodyClass= "details-page" if len(section['posts']) == 1 else "",
        posts = section['posts'] if not isArchiveModeEnabled(section) else section['archivePosts'], 
        post = section['posts'][0],
        page = {
            'title': section['seoTitle'], 
            'description': section['seoDescription']
        }, 
        site = cfg.site, 
        menu = cfg.menu
    )
    
    # if the current section is the root of the blog
    if section['root']:
        createDirectory('output/')
        filepath = os.path.join('output', 'index.html')
    else:
        createDirectory('output/' + section['directory'] + '/')
        filepath = os.path.join('output/' + section['directory'], 'index.html')
    
    writeToFile(filepath, renderedHtml.encode('utf-8'))

# Generate index/listing page
def generateIndexPage(section):
    # Check if this section has an index page
    if 'index' in section['template']:
        # If pagination is not active
        if not section['pagination']:
            generateIndexWithoutPaginator(section)
        # If pagination is active
        else:
            generateIndexWithPaginator(section, 8)

# Generate pages with content
def generateContent(section):
    posts = section['posts']
    postsDirectory = 'output/posts/'
    template = env.get_template(section['template']['details'])
    
    if not section['root']:
        postsDirectory = 'output/' + section['directory'] + '/posts/'

    # Create a directory to store all the posts based on the section
    createDirectory(postsDirectory)

    for post in posts:
        renderedHtml = template.render(
            post=post, 
            bodyClass="details-page" + " " + section['directory'], 
            directory=section['directory'],
            page = {
                'title': post['title'], 
                'description': post['summary']
            }, 
            site = cfg.site, 
            menu = cfg.menu
        )
        filepath = postsDirectory + '{slug}/index.html'.format(slug=post['slug'])

        # Create directory for the post
        createDirectory(filepath)
        writeToFile(filepath, renderedHtml.encode('utf-8'))

# Generate the homepage section of the blog
def generateHomepage(section):
    limit = 9
    template = env.get_template(section['template']['index'])
    sectionsToShow = {}

    for selectedSection in section['sectionsToShow']:
        sectionsToShow[selectedSection] = getPosts(selectedSection)[0:limit]

    renderedHtml = template.render(
        bodyClass="",
        sections = sectionsToShow, 
        page = {
            'title': section['seoTitle'], 
            'description': section['seoDescription']
        }, 
        site = cfg.site, 
        menu = cfg.menu
    )

    createDirectory('output/')
    filepath = os.path.join('output', 'index.html')

    writeToFile(filepath, renderedHtml.encode('utf-8'))

# Generate all pages i.e. index, details and RSS required for the section
def generatePages(section):
    
    # Check if it's a home page
    if section['homepage']:
        generateHomepage(section)

    # Otherwise, generate other pages    
    else:
        # Deletes section related files only
        directoryToDelete = "output/posts/"

        if not section['root']:
            directoryToDelete = "output/{directory}/".format(directory=section['directory'])

        # Delete the RSS and JSON files related to the section
        filesToDelete = [
            'output/rss/' + section['directory'] + '.xml',
            'output/json/' + section['directory'] + '.json',
        ];

        for file in filesToDelete:
            deleteFile(file)

        # Generate the main page
        generateIndexPage(section)

        # Generate details page, if it has one
        if 'details' in section['template']:
            generateContent(section)
            # generateJSON(section)
            # generateRSS(section)

# Build all sections
def buildAllSections():
    for section in cfg.sections:
        buildSection(section)

# Build a specific section
def buildSection(section):
    section['posts'] = getPosts(section['directory'])

    # Create archive listing if archive mode is enabled
    if isArchiveModeEnabled(section):
        section['archivePosts'] = archivePosts(section['posts'])

    generatePages(section)

def isArchiveModeEnabled(section):
    return True if 'archive' in section and section['archive'] else False

# Build entire or section(s) of the blog
@app.command()
def build(mode=""):
    message = "The posts for all sections are generated successfully!"
    
    # if no mode has been specified, prompt the user
    if len(mode) == 0:
        sectionList = '\n'.join([str(idx+1) + ". " + item['title'] for idx, item in enumerate(cfg.sections)])
        typer.echo("""Which section do you want to render? Hit '0' for all sections.\n""" + sectionList)
        option = int(typer.prompt("Enter number"))
    
        # If it's a specific section
        if option != 0:
            section = cfg.sections[option-1]
            message = "The posts for {section} section is generated successfully!".format(section=section['title'])
            buildSection(section)            
        # Else, generate all sections of the blog
        else:
            buildAllSections()

    # If it's all, then build all sections
    elif mode == "all":
        buildAllSections()

    # Else, that option is not available
    else:
        message = "Invalid build mode specified."

    typer.echo(message)

# Create a blog post
@app.command()
def create():
    
    # Prompt the user to enter the title, section and category of the blog post
    title = typer.prompt("What's the title of the blog post?")
    section = typer.prompt("Which section does it belong to?")
    category = typer.prompt("What category does it fall under?")
    
    # The directory of the post
    directory = "content/" + section.lower() + "/"

    # Create a new section if it doesn't exist
    createDirectory(directory)

    # Post to be created on the current date
    today = date.today()
    slug = generateSlug(title)
    
    blogFilePath = generateFilePath(today, directory, slug)

    postDate = formatDate(today, '%B {S}, %Y')
    meta = cfg.METATEMPLATE.strip().format(title=title, category=category, date=postDate, slug=slug)

    with open(blogFilePath, 'w') as file:
        file.write(meta)
    
    typer.echo("Your file has been created: " + blogFilePath)

# Generate file path
def generateFilePath(date, directory, slug):
    fileNumber = generateFileNumber(directory)
    fileName = "_".join(['{:0>2}', '{}', '{:0>2}', '{:0>2}', '{}.md'])
    return directory + fileName.format(fileNumber, date.year, date.month, date.day, slug)

"""
Format blog post date
You can write in any format, the current format
used is: Month Day, year

The current stub is replacing the number with a prefix
"""
def formatDate(date: str, format: str):
    return date.strftime(format).replace('{S}', dateSuffix(date.day))

# Create ordinal date suffix
def dateSuffix(day: int):
    return str(day) + ("th" if 4 <= day%100 <= 20 else {1:'st', 2:'nd', 3:'rd'}.get(day%10, "th"))

# Generate unique file number
def generateFileNumber(path):
    
    # Get existing files
    existingFiles = glob(path + "*.md");

    """
    If there are no posts under this section,
    then this is the first file        
    """ 
    if not existingFiles:
        return 1
    
    """
    Find the largest number in the directory
    and increment it for the new post!
    """
    prefixes = [filename.replace(path, '')[:2] for filename in existingFiles]
    biggest_prefix = max(prefixes, key=lambda n: int(n))
    return int(biggest_prefix) + 1
    
# Generate slug based on the title
def generateSlug(title: str):
    title = "".join(x for x in title if x.isalnum() or x == ' ')
    return title.lower().strip("").replace(' ', '-')

# Count the words in the text
def countWordsInText(textList, wordLength):
    totalWords = 0
    for text in textList:
        totalWords += len(text)/wordLength
    return totalWords 

# Estimate reading time of the article
def estimateReadingTime(content):
    str = ""
    WPM = 200
    wordLength = 5
    texts = extractText(content)
    filteredText = filterText(texts)
    minutes = round(countWordsInText(filteredText, wordLength) / WPM)
    if minutes > 1:
        str = "{minutes} minutes read".format(minutes=minutes)
    else:
        str = "1 minute read"
    return str

# Extract text from HTML
def extractText(content):
    soup = BeautifulSoup(content, features='html.parser')
    texts = soup.findAll(text=True)
    return texts

# Strip out CSS, JS, Scripts or any HTML Tags
def stripHtmlElements(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'pre', 'code']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    elif element.string == '\n':
        return False
    return True

# Filter text only
def filterText(content):
    return filter(stripHtmlElements, content)

# Get the first line of the content
def getFirstLine(content):
    soup = BeautifulSoup(content.splitlines()[0], features="html.parser")
    for x in soup.find_all():
        if len(x.get_text(strip=True)) == 0:
            x.extract()
    return ' '.join(['<p>', soup.get_text(strip=True), '</p>'])

# Return index in an array of dicts
def findIndex(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

# Check if the section/directory exists
def sectionExists(section: str):
    return os.path.exists(section)

# Write to file
def writeToFile(path, content):
    with open(path, 'wb') as file:
        file.write(content)
        file.close()

# Create a new directory
def createDirectory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(os.path.dirname(directory))

# Delete existing directory
def deleteDirectory(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)

# Delete File
def deleteFile(file: str):
    if os.path.exists(file):
        os.remove(file)

"""
Execute app
"""
if __name__ == "__main__":
    app()