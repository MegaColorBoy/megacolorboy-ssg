"""
Author: Abdush Shakoor
megacolorboy-ssg: A simple static site generator written in Python 3
"""

#!/usr/bin/env python3

import os, random, sys
from glob import glob
import json
import datetime
from dateutil.parser import parse
from jinja2 import Environment, PackageLoader
from markdown2 import markdown
import typer
from time import sleep
from progress.bar import IncrementalBar
from itertools import islice
import shutil

# General configuration for the blog
config = {
    'name': 'megacolorboy',
    'author': 'Abdush Shakoor',
    'description': "I like problem solving and building stuff for fun.",
}

# Sections of the blog
sections = [
    {
        'title': 'Main blog',
        'directory': 'articles',
        'template': {
            'index': 'index-alt-v4.html',
            'paginationIndex': 'index-alt-v5.html',
            'details': 'post-detail-v3.html',
        },
        'root': True,
        'pagination': False
    },
    {
        'title': 'TIL Posts',
        'directory': 'til',
        'template': {
            'index': 'til_index.html',
            'paginationIndex': 'index-alt-v5.html',
            'details': 'til-detail.html',
        },
        'root': False,
        'pagination': False
    },
    {
        'title': 'About page',
        'directory': 'about',
        'template': {
            'index': 'about-alt-2.html',
        },
        'root': False,
        'pagination': False
    }
]

# The template for storing meta information of the blog post
METATEMPLATE = """
title: {title}
date: {date}
slug: {slug}
category: {category}
summary: Write your summary here.
status: inactive

Start writing your content here.
"""

# Using Typer as the CLI tool
app = typer.Typer()

# Jinja2 Environment
env = Environment(loader=PackageLoader('ssg','templates'))

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
def generateRSS(section: str):
    return False

# Format date in YYYY-MM-DD
def convertToRawDate(dateTimeStr: str):
    return "{0.year}-{0:%m}-{0:%d}".format(parse(dateTimeStr))

# Get posts required to render
def getPosts(section=""):
    
    # List of posts
    posts = []
    
    # Refer to https://github.com/trentm/python-markdown2/wiki/Extras for documentation
    extras = ['metadata', 'fenced-code-blocks']
    
    # Directory where all the content is stored
    contentDirectory = "content/" + section
    
    # Look for Markdown file recursively in the specified directory
    with IncrementalBar('Processing...', suffix='%(percent)d%%') as bar:
        for root, directories, files in os.walk(contentDirectory):
            for post in files:
                filepath = os.path.join(root, post)
                if post.endswith('.md'):
                    with open(filepath, 'r') as file:
                        postContent = markdown(file.read(), extras=extras)
                        
                        # Fetch metadata of each article
                        title = postContent.metadata['title']
                        date = postContent.metadata['date']
                        dateRaw = convertToRawDate(postContent.metadata['date'])
                        slug = postContent.metadata['slug']
                        category = postContent.metadata['category']
                        summary = postContent.metadata['summary'] if 'summary' in postContent.metadata else 'n/a'

                        # if the status is not present in the file, it's assumed that the post is active.
                        status = postContent.metadata['status'] if 'status' in postContent.metadata else 'active'
                        
                        # Only active posts must be stored
                        if status == 'active':
                            posts.extend([
                                {
                                    'section': root,
                                    'title': title,
                                    'date': date,
                                    'dateRaw': dateRaw,
                                    'slug': slug,
                                    'category': category,
                                    'summary': summary,
                                    'filename': filepath,
                                    'status': status,
                                    'content': postContent,
                                }
                            ])
                        bar.next()
                    
    # sort posts by filename and date
    posts = sorted(posts, key=lambda x: (x['filename'], x['dateRaw']), reverse=True)
    return posts

# Generate archive based on section
def archive(section: str):
    return False

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
            posts=chunkedPosts[pageNumber],
            curr=currentPageNumber,
            prev=prevPage,
            next=nextPage,
            total=numberOfPages+1
        )

        writeToFile(pageFile, renderedHtml.encode('utf-8'))

# Generate index page without pagination links
def generateIndexWithoutPaginator(section):
    template = env.get_template(section['template']['index'])
    renderedHtml = template.render(posts=section['posts'])
    
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
    
    # Create a directory to store all the posts based on the section
    createDirectory(postsDirectory)

    if not section['root']:
        postsDirectory = 'output/' + section['directory'] + '/posts/'

    for post in posts:
        renderedHtml = template.render(post=post)
        filepath = postsDirectory + '{slug}/index.html'.format(slug=post['slug'])

        # Create directory for the post
        createDirectory(filepath)
        writeToFile(filepath, renderedHtml.encode('utf-8'))
            

#Build entire or section(s) of the blog
@app.command()
def build():
    sectionList = '\n'.join([str(idx+1) + ". " + item['title'] for idx, item in enumerate(sections)])
    typer.echo("""Which section do you want to render? Hit '0' for all sections.\n""" + sectionList)
    option = int(typer.prompt("Enter number"))
    
    # If it's a specific section
    if option != 0:

        section = sections[option-1]
        section['posts'] = getPosts(section['directory'])

        # Delete subdirectory before generating new posts
        deleteDirectory('output/' + section['directory'] + '/')
        generateIndexPage(section)

        if 'details' in section['template']:
            generateContent(section)
            generateJSON(section)

    # Else, generate all sections of the blog
    else:
        # Delete directory before generating a new set of files
        deleteDirectory('output/')
        
        for section in sections:
            section['posts'] = getPosts(section['directory'])
            generateIndexPage(section)
            if 'details' in section['template']:
                generateContent(section)
                generateJSON(section)

    typer.echo('Your posts are succesfully generated.')

"""
Create a blog post
"""
@app.command()
def create():
    
    # Prompt the user to enter the title, section and category of the blog post
    title = typer.prompt("What's the title of the blog post?")
    section = typer.prompt("Which section does it belong to?")
    category = typer.prompt("What category does it fall under?")
    
    # The directory of the post
    directory = "content/" + section + "/"

    # Create a new section if it doesn't exist
    createDirectory(directory)

    # Post to be created on the current date
    today = datetime.date.today()
    slug = generateSlug(title)
    
    blogFilePath = generateFilePath(today, directory, slug)

    postDate = formatDate(today, '%B {S}, %Y')
    meta = METATEMPLATE.strip().format(title=title, category=category, date=postDate, slug=slug)

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

"""
Execute app
"""
if __name__ == "__main__":
    app()
