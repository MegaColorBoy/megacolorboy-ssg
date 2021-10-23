# Custom configuration for the website

# General configuration for the blog
site = {
    "name": "megacolorboy",
    "url": "https://www.megacolorboy.com",
    "author": "Abdush Shakoor",
    "theme": "minimal-theme/",
    #"color": "dark", 
}

menu = [
	{
		'title': 'About',
		'link': '/about',
	},
	{
		'title': 'Writings',
		'link': '/writings',
	},
	{
		'title': 'Today I Learned',
		'link': '/til',
	},
	{
		'title': 'Resume',
		'link': '/resume',
	}
    #{
	# 	'title': 'Projects',
	# 	'link': '/projects',
	#},
]

# Sections of the blog
sections = [
    {
        'title': 'Home',
        'directory': 'home',
        'seoTitle': "Abdush Shakoor's Blog",
        'seoDescription': "A not-so-typical software developer & designer with a passion for computer science, mathematics, software engineering, digital design & technology.",
        'template': {
            'index': 'index.html',
        },
        'sectionsToShow': ['writings', 'til'],
        'root': False,
        'homepage': True,
        'pagination': False   
    },
    {
        'title': 'Writings',
        'directory': 'writings',
        'seoTitle': "Writings",
        'seoDescription': "Sometimes, I write stuff about computers, math, technology & design.",
        'template': {
            'index': 'listing.html',
            'details': 'details.html',
        },
        # 'multiple': ['writings', 'til'],
        "archive": True,
        'root': False,
        'homepage': False,
        'pagination': False
    },
    {
        'title': 'TIL Posts',
        'directory': 'til',
        'seoTitle': "Today I Learned",
        'seoDescription': "A collection of short write-ups on the things that I learn on a day-to-day basis.",
        'template': {
            'index': 'listing.html',
            'details': 'details.html',
        },
        "archive": True,
        'root': False,
        'homepage': False,
        'pagination': False
    },
    {
        'title': 'About page',
        'directory': 'about',
        'seoTitle': "A little bit about myself",
        'seoDescription': "Here's a not-so-formal kind of introduction about myself.",
        'template': {
            'index': 'details.html',
        },
        'archive': False,
        'root': False,
        'homepage': False,
        'pagination': False
    },
    {
        'title': 'Resume',
        'directory': 'resume',
        'seoTitle': "Resume",
        'seoDescription': "A simple looking resume for the recruiters.",
        'template': {
            'index': 'resume.html',
        },
        'dataType': "json",
        'jsonData': "data/resume.json",
        'archive': False,
        'root': False,
        'homepage': False,
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