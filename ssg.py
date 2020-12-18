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

"""
    View all written blog posts
    @section: By default, it'll be for everything, else you can specify
    the section that you want to view
"""
def view_all_posts(section: str):
    return False


# Generate JSON dump of blog
def generate_json(section: str):
    return False


# Generate RSS Feed in XML
def generate_rss(section: str):
    return False

# Format date
def formattedDate(dateTimeStr: str):
    dateTimeObj = parse(dateTimeStr)
    return "{0.year}-{0:%m}-{0:%d}".format(dateTimeObj)

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
                        date = formattedDate(postContent.metadata['date'])
                        slug = postContent.metadata['slug']
                        category = postContent.metadata['category']
                        summary = postContent.metadata['summary'] if 'summary' in postContent.metadata else 'n/a'
                        status = postContent.metadata['status'] if 'status' in postContent.metadata else 'inactive'

                        posts.extend([
                            {
                                'title': title,
                                'date': date,
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
    posts = sorted(posts, key=lambda x: (x['filename'], x['date']), reverse=True)
    return posts
                

#Build entire or section(s) of the blog
@app.command()
def build():
    sections = [
        {
            'title': 'Main blog',
            'directory': 'articles'
        },
        {
            'title': 'TIL Posts',
            'directory': 'til-posts'
        },
        {
            'title': 'About page',
            'directory': 'about'
        }
    ]

    sectionStr = '\n'.join([str(idx+1) + ". " + item['title'] for idx, item in enumerate(sections)])
    typer.echo("""Which section do you want to render? Hit '0' for all sections.\n""" + sectionStr)
    option = typer.prompt("Enter number")
    sectionToRender = sections[int(option)-1]['directory'] if int(option) > 0 else ''
    getPosts(sectionToRender)
    typer.echo('Files are processed.')

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
    with open(path, 'w') as file:
        file.write(content)
        file.close()

# Create a new directory
def createDirectory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(os.path.dirname(directory))
    
"""
Execute app
"""
if __name__ == "__main__":
    app()
