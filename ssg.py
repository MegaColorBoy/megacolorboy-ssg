"""
Author: Abdush Shakoor
megacolorboy-ssg: A simple static site generator written in Python 3
Updated on: 19-02-2021
"""

#!/usr/bin/env python3

import os, random, sys
from glob import glob
import json
from collections import namedtuple
from datetime import datetime, date
from dateutil.parser import parse
from jinja2 import Environment, PackageLoader
# from markdown2 import markdown
import markdown2
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
import htmlentities
from pprint import pprint

# Using Typer as the CLI tool
app = typer.Typer()

# Site configuration
site_config = {}

# Menu configuration
menu_config = []

# All posts
all_posts = []

# Jinja2 Environment
env = None

# Generate categories
def generate_categories():
    pass

# TODO: Use archive_posts method to fetch all posts in archive order
# Generate archive posts
#def generate_archive_posts():
#    pass

# Generate menu
def generate_menu():
    menu = []
    for section in cfg.sections:
        if 'display_in_menu' in section and section['display_in_menu'] == True:
            menu.append({'link': section['url'], 'title': section['title']})
    return menu

# TODO: Need to rewrite method for optimization
# Generate JSON dump
def generate_json(section):
    posts = section['posts']
    
    json_data = {
        'posts': []
    }
    
    for post in posts:
        json_data['posts'].append(post)
    
    json_directory = 'output/json/'
    create_directory(json_directory)
    
    with open(json_directory + section['content_directory'] + '.json', 'w') as file:
        json.dump(json_data, file)
    

# TODO: Need to rewrite method for optimization
# Generate RSS Feed in XML
def generate_rss(section):
    posts = section['posts']

    post_url = "posts"

    if not section['root']:
        post_url = '/'.join([section['content_directory'], "posts"])

    xml_directory = 'output/rss/'
    create_directory(xml_directory)

    xml_items = []

    for post in posts:
        title = post['title']
        link = '/'.join([site_config['url'], post_url, post['slug']])

        date_raw = convert_to_raw_date(post['date'])
        date = datetime.fromisoformat(date_raw).strftime("%a, %d %b %Y %X")
                
        summary = post['summary']

        xml_items.append("""
            <item>
                <title>{title}</title>
                <link>{link}</link>
                <guid isPermaLink="true">{link}</guid>
                <pubDate>{date} GMT</pubDate>
                <description>{summary}</description>
            </item>
        """.format(title=htmlentities.encode(title), link=link, date=date, summary=htmlentities.encode(summary))
        )
    
    rss_title = ' | '.join([section['seo']['title'], site_config['name']])
    rss_link = site_config['url'] if section['root'] else '/'.join([site_config['url'], section['content_directory']])
    rss_description = section['seo']['description']

    xml = """
      <?xml version="1.0" encoding="UTF-8"?>
      <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
        <channel>
            <title>{title}</title>
            <link>{link}</link>
            <description>{description}</description>
            <atom:link href="{link}" rel="self" type="application/rss+xml" />
            {items}
        </channel>
       </rss>
    """.format(title=htmlentities.encode(rss_title), link=rss_link, description=htmlentities.encode(rss_description), items=''.join(xml_items).strip())

    file_path = xml_directory + section['content_directory'] + '.xml'
    write_to_file(file_path, xml.strip().encode('utf-8'))

# Format date in YYYY-MM-DD
def convert_to_raw_date(date_time_str: str):
    return "{0.year}-{0:%m}-{0:%d}".format(parse(date_time_str))

# Get the index of the blog article
def get_file_index(path):
    return int(re.search("content\/\w+\/(\d+).*", path, re.IGNORECASE).group(1))

def json_decoder(json_dict):
    return namedtuple('X', json_dict.keys())(*json_dict.values())

# Convert JSON Data to an Object
def convert_json_to_python_object(json_dict):
    return json.loads(json.dumps(json_dict), object_hook=json_decoder)

# Load all articles/posts at once
def load_posts():
    content_directories = [section['content_directory'] for section in cfg.sections if 'content_directory' in section]
    posts = get_posts(content_directories)
    return posts

# Get posts required to render
def get_posts(content_directories = []):
    
    # List of posts
    posts = []
    # Refer to https://github.com/trentm/python-markdown2/wiki/Extras for documentation
    extras = ['metadata', 'code-friendly', 'fenced-code-blocks']

    paths = []
    
    for directory in content_directories:
        paths.append("content/" + directory)
    
    # Look for Markdown file recursively in the specified directory
    with IncrementalBar('Processing...', suffix='%(percent)d%%') as bar:
        for path in paths:
            for root, directories, files in os.walk(path):
                for post in files:
                    file_path = os.path.join(root, post)
                    if post.endswith('.md'):
                        with open(file_path, 'r') as file:
                            post_content = markdown2.markdown(file.read(), extras=extras)

                            # Fetch metadata of each article
                            index = get_file_index(file_path)
                            title = post_content.metadata['title']
                            post_date = post_content.metadata['date']
                            date_raw = convert_to_raw_date(post_content.metadata['date'])
                            date_alt = "{0:%d}.{0:%m}.{0.year}".format(parse(post_content.metadata['date']))
                            post_year = datetime.fromisoformat(date_raw).strftime("%Y")
                            slug = post_content.metadata['slug']
                            category = post_content.metadata['category']
                            # summary = post_content.metadata['summary'] if 'summary' in post_content.metadata else 'Tips & Tricks &mdash; ' + category
                            # summary = post_content.metadata['summary'] if 'summary' in post_content.metadata else "".join(filter_text(extract_text(post_content)))
                            summary = post_content.metadata['summary'] if 'summary' in post_content.metadata else ""
                            reading_time = estimate_reading_time(post_content)
                            post_url = '/'.join([path.replace('content/', ''), 'posts', slug])

                            # if the status is not present in the file, it's assumed that the post is active.
                            status = post_content.metadata['status'] if 'status' in post_content.metadata else 'active'
                            
                            # Only active posts must be stored
                            if status == 'active':
                                posts.extend([
                                    {
                                        'section': root,
                                        'title': title,
                                        'link': post_url,
                                        'date': post_date,
                                        'date_alt': date_alt,
                                        'year': post_year,
                                        'date_raw': date_raw,
                                        'slug': slug,
                                        'category': category,
                                        'summary': summary,
                                        'reading_time': reading_time,
                                        'filename': file_path,
                                        'status': status,
                                        'content': post_content,
                                        'index': index
                                    }
                                ])
                            bar.next()

    # sort posts by index and date
    posts = sorted(posts, key=lambda x: (x['date_raw']), reverse=True)
    return posts

# Archive mode
def archive_posts(posts):
    return [list(group) for _, group in groupby(sorted(posts, key=lambda x: x['date_raw'], reverse=True), key=lambda y: datetime.fromisoformat(y['date_raw']).strftime("%Y"))]

# Generate index page with pagination links
def generate_index_with_paginator(section, posts_per_page):
    template = env.get_template('listing.html')

    # Check if section has specified any template config to override default configuration.
    if section['page_type'] == 'main':
        template = env.get_template('main.html') 
    elif 'template' in section:
        template = env.get_template(section['template']['listing'])

    # Total number of posts per section
    total_number_of_posts = len(section['posts'])
    
    # Number of pagination links to generate
    number_of_pages = int(total_number_of_posts / posts_per_page)

    # Create a directory to store the pagination links (By default, it's root)
    root_directory = 'output/'

    # If the current section is not root, then create it as a sub_directory instead.
    if section['page_type'] != 'main': 
        root_directory = 'output/' + section['content_directory'] + '/'
    
    create_directory(root_directory)    
    
    page_directory = "/" + section['content_directory'] + "/pages/" if section['page_type'] != 'main' else "/pages/" 

    """
    Split the posts in even chunks
    """
    it = iter(section['posts'])
    chunked_posts = list(iter(lambda: tuple(islice(it, posts_per_page)), ()))

    for page_number in range(0, number_of_pages+1):
        current_page_number = page_number + 1
        
        sub_directory = ''
        
        # Don't create a sub_directory for the first page        
        if current_page_number > 1:
            sub_directory = 'pages/{page}/'.format(page=current_page_number)
            delete_directory(root_directory + sub_directory)
            create_directory(root_directory + sub_directory)
        
        # Path of the index page for each pagination link
        page_index_file = ''.join([root_directory, sub_directory, 'index.html'])

        # Create links for previous and next pages
        previous_page = 0 if current_page_number == 1 else current_page_number-1
        next_page = 0 if current_page_number == number_of_pages+1 else current_page_number+1

        # Render the page
        rendered_html = template.render(
            body_class="",
            posts=chunked_posts[page_number],
            curr=current_page_number,
            prev=previous_page,
            next=next_page,
            total=number_of_pages+1,
            directory = page_directory,
            pagination_links = generate_pagination_links(page_directory, current_page_number, number_of_pages+1),
            page = {
                'title': section['seo']['title'], 
                'description': section['seo']['description']
            },
            pagination = True,
            site = site_config, 
            menu = menu_config
        )

        write_to_file(page_index_file, rendered_html.encode('utf-8'))

# Generate links for each "pages/" index directory
def generate_pagination_links(page_directory, current, max):
    current_page = current
    last = max
    delta = 2
    left = current_page - delta
    right = current_page + delta + 1
    page_range = []
    page_range_with_dots = []
    limit = None

    for i in range(1, last + 1):
        if i == 1 or i == last or (i >= left and i < right):
            page_range.append(i)

    for i in page_range:
        if limit:
            if i - limit == 2:
                page_range_with_dots.append({
                    'url': page_directory + str(limit + 1) if limit + 1 > 1 else page_directory.replace('/pages/', '/'),
                    'page': limit + 1,
                    'has_dots': False
                })
            elif i - limit != 1:
                page_range_with_dots.append({
                    'url': page_directory + str(i - limit) if i - limit > 1 else page_directory.replace('/pages/', '/'),
                    'page': i - limit,
                    'has_dots': True
                })

        page_range_with_dots.append({
            'url': page_directory + str(i) if i > 1 else page_directory.replace('/pages/', '/'),
            'page': i,
            'has_dots': False
        })

        limit = i

    return page_range_with_dots

# Generate index page without pagination links
def generate_index_without_paginator(section):
    template = env.get_template('listing.html')

    # Check if it's a custom page
    if section['page_type'] == 'custom':
        template = env.get_template(section['template']['custom'])
    # Check if it's an archive page
    elif section['page_type'] == 'archive':
        template = env.get_template('archive.html')
    # Check if section has specified any template config to override default configuration.
    elif 'template' in section:
        template = env.get_template(section['template']['listing'])        
    
    # Markdown Based Page
    if 'data_type' not in section or 'markdown' in section['data_type']:
        rendered_html = template.render(
            body_class= "details-page" if len(section['posts']) == 1 else "",
            posts = section['posts'], 
            post = section['posts'][0],
            page = {
                'title': section['seo']['title'], 
                'description': section['seo']['description']
            }, 
            pagination = False,
            site = site_config, 
            menu = menu_config
        )
    # JSON Based Page
    elif 'data_type' in section and 'json' in section['data_type']:
        rendered_html = template.render(
            data = convert_json_to_python_object(section['json_data']),
            page = {
                'title': section['seo']['title'], 
                'description': section['seo']['description']
            },
        )
    
    # if the current section is the root of the blog
    create_directory('output/' + section['content_directory'] + '/')
    file_path = os.path.join('output/' + section['content_directory'], 'index.html')
    write_to_file(file_path, rendered_html.encode('utf-8'))

# Generate index/listing page
def generate_index_page(section):
    if 'enable_pagination' not in section or section['enable_pagination'] == False:
        generate_index_without_paginator(section)        
    else:
        generate_index_with_paginator(section, 8)

# Generate pages with content
def generate_content(section):
    posts = section['posts']
    template = env.get_template('single.html')

    # Check if section has specified any template config to override default configuration.
    if 'template' in section:
        template = env.get_template(section['template']['single'])        
    
    if section['page_type'] == 'multiple':
        posts_directory = 'output/' + section['content_directory'] + '/posts/'
    else:
        posts_directory = 'output/' + section['content_directory'] + '/'

    # Create a directory to store all the posts based on the section
    create_directory(posts_directory)

    if section['page_type'] == 'multiple':
        for post in posts:
            rendered_html = render_post(template, {
                'post': post,
                'content_directory': section['content_directory']    
            })
            file_path = posts_directory + '{slug}/index.html'.format(slug=post['slug'])
            # Create directory for the post
            create_directory(file_path)
            write_to_file(file_path, rendered_html.encode('utf-8'))
    else:
        rendered_html = render_post(template, {
            'post': posts[0],
            'content_directory': section['content_directory']    
        })
        file_path = posts_directory + 'index.html'
        write_to_file(file_path, rendered_html.encode('utf-8'))

# Method to render a single article
def render_post(template, options):
   return template.render(
        post=options['post'],  
        directory=options['content_directory'],
        page = {
            'title': options['post']['title'], 
            'description': options['post']['summary']
        }, 
        site = site_config, 
        menu = menu_config
    )

# Get posts based on content directory/section
def get_posts_by_content_directory(content_directories = []):
    return [post for post in all_posts if post['section'].replace('content/', '') in content_directories]

# Get recent articles
def get_recent_articles():
    content_directories = []
    for section in cfg.sections:
        if 'show_in_recent_articles' in section and section['show_in_recent_articles'] == True:
            content_directories.append(section['content_directory'])
    return get_posts_by_content_directory(content_directories)

# Generate the main page section of the blog
def generate_main_page(section):
    template = env.get_template('main.html')

    # Check if section has specified any template config to override default configuration.
    if 'template' in section:
        template = env.get_template(section['template']['main'])        
    
    section['posts'] = get_recent_articles()
    generate_index_with_paginator(section, 8)

# Generate the archive section of the blog
def generate_archive_page(section):
    template = env.get_template('archive.html')

    # Check if section has specified any template config to override default configuration.
    if 'template' in section:
        template = env.get_template(section['template']['archive'])

    section['posts'] = archive_posts(all_posts)
    generate_index_without_paginator(section)

# Generate all pages i.e. index, details and RSS required for the section
def generate_pages(section):    
    page_type = section['page_type']

    # Deletes section related files only
    directory_to_delete = "output/{directory}/".format(directory=section['content_directory']) + "/"
    delete_directory(directory_to_delete)

    if section['page_type'] == 'multiple':
        generate_index_page(section)

    generate_content(section)
        
# Generate JSON based pages -- mainly created for the Resume section
def generate_json_section(section):
    message = "Error: Make sure that the JSON data for the {section} section exists".format(section=section['title'])

    # Check if this JSON data exists for this section
    if 'data_type' in section and section['data_type'] == 'json':
        file = section['content_directory'] + "/data.json"
        if os.path.exists(file):
            # Fetch data
            with open(section['content_directory']) as json_file:
                section['json_data'] = json.load(json_file)

            # Delete section
            directory_to_delete = "output/{directory}/".format(directory=section['content_directory'])

            # Generate Page
            generate_index_page(section)

            message = "{section} Created".format(section=section['title'])
        
    typer.echo(message)

# Build all sections
def build_all_sections():
    for section in cfg.sections:
        build_section(section)

# Build a specific section
def build_section(section):
    # If the content is JSON data based
    if 'data_type' in section and section['data_type'] == "json":
        generate_json_section(section)

    # If the content is Markdown based, by default it is Markdown.
    else:
        if section['page_type'] == 'main':
            generate_main_page(section)
        elif section['page_type'] == 'archive':
            generate_archive_page(section)
        else:
            section['posts'] = get_posts_by_content_directory([section['content_directory']])
            generate_pages(section)

def is_archive_mode_enabled(section):
    return True if 'archive' in section and section['archive'] else False

# Build entire or section(s) of the blog
@app.command()
def build(mode=""):
    message = "The posts for all sections are generated successfully!"
    
    # if no mode has been specified, prompt the user
    if len(mode) == 0:
        sections = '\n'.join([str(idx+1) + ". " + item['title'] for idx, item in enumerate(cfg.sections)])
        typer.echo("""Which section do you want to render? Hit '0' for all sections.\n""" + sections)
        option = int(typer.prompt("Enter the appropriate number"))
    
        # If it's a specific section
        if option != 0:
            section = cfg.sections[option-1]
            message = "The articles for {section} section is generated successfully!".format(section=section['title'])
            build_section(section)            
        # Else, generate all sections of the blog
        else:
            build_all_sections()

    # If it's all, then build all sections
    elif mode == "all":
        build_all_sections()

    # Else, that option is not available
    else:
        message = "Invalid build mode specified. Type --help to know more."

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
    create_directory(directory)

    # Post to be created on the current date
    today = date.today()
    slug = generate_slug(title)
    
    post_file_path = generate_file_path(today, directory, slug)

    post_date = format_date(today, '%B {S}, %Y')
    meta = cfg.METATEMPLATE.strip().format(title=title, category=category, date=post_date, slug=slug)

    with open(post_file_path, 'w') as file:
        file.write(meta)
    
    typer.echo("Your file has been created: " + post_file_path)

# Generate file path
def generate_file_path(date, directory, slug):
    file_number = generate_file_number(directory)
    file_name = "_".join(['{:0>2}', '{}', '{:0>2}', '{:0>2}', '{}.md'])
    return directory + file_name.format(file_number, date.year, date.month, date.day, slug)

"""
Format blog post date
You can write in any format, the current format
used is: Month Day, year

The current stub is replacing the number with a prefix
"""
def format_date(date: str, format: str):
    return date.strftime(format).replace('{S}', date_suffix(date.day))

# Create ordinal date suffix
def date_suffix(day: int):
    return str(day) + ("th" if 4 <= day%100 <= 20 else {1:'st', 2:'nd', 3:'rd'}.get(day%10, "th"))

# Generate unique file number
def generate_file_number(path):
    
    # Get existing files
    existing_files = glob(path + "*.md");
    max_prefix = 0

    """
    If there are no posts under this section,
    then this is the first file        
    """ 
    if not existing_files:
        return 1
    
    """
    Find the largest index in the directory
    and auto-increment it for the new post!
    """
    indexes = [get_file_index(filename) for filename in existing_files]
    return max(indexes, key=lambda n: int(n)) + 1
    
# Generate slug based on the title
def generate_slug(title: str):
    title = "".join(x for x in title if x.isalnum() or x == ' ')
    return title.lower().strip("").replace(' ', '-')

# Count the words in the text
def count_words_in_text(text_list, word_length):
    total_words = 0
    for text in text_list:
        total_words += len(text) / word_length
    return total_words 

# Estimate reading time of the article
def estimate_reading_time(content):
    str = ""
    wpm = 200
    word_length = 5
    texts = extract_text(content)
    filtered_text = filter_text(texts)
    minutes = round(count_words_in_text(filtered_text, word_length) / wpm)
    if minutes > 1:
        str = "{minutes} minutes read".format(minutes=minutes)
    else:
        str = "1 minute read"
    return str

# Extract text from HTML
def extract_text(content):
    soup = BeautifulSoup(content, features='html.parser')
    texts = soup.findAll(text=True)
    return texts

# Strip out CSS, JS, Scripts or any HTML Tags
def strip_html_elements(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'pre', 'code']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    elif element.string == '\n':
        return False
    return True

# Filter text only
def filter_text(content):
    return filter(strip_html_elements, content)

# Get the first line of the content
def get_first_line(content):
    soup = BeautifulSoup(content.splitlines()[0], features="html.parser")
    for x in soup.find_all():
        if len(x.get_text(strip=True)) == 0:
            x.extract()
    return ' '.join(['<p>', soup.get_text(strip=True), '</p>'])

# Return index in an array of dicts
def find_index(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

# Check if the section/directory exists
def section_exists(section: str):
    return os.path.exists(section)

# Write to file
def write_to_file(path, content):
    with open(path, 'wb') as file:
        file.write(content)
        file.close()

# Create a new directory
def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(os.path.dirname(directory))

# Delete existing directory
def delete_directory(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)

# Delete File
def delete_file(file: str):
    if os.path.exists(file):
        os.remove(file)

"""
Execute app
"""
if __name__ == "__main__":
    all_posts = load_posts()
    site_config = cfg.site
    menu_config = generate_menu()
    env = Environment(loader=PackageLoader('ssg','templates/' + site_config['theme']))
    app()