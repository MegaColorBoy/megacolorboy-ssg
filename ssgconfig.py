# Custom configuration for the website


# General configuration for the blog
site = {
    "name": "megacolorboy",
    "url": "https://www.megacolorboy.com",
    "author": "Abdush Shakoor",
    "theme": "minimal/",
    "color": "dark", 
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
		'title': 'Projects',
		'link': '/projects',
	},
	{
		'title': 'Resume',
		'link': '/resume',
	}
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
        'root': True,
        'pagination': False   
    },
    {
        'title': 'Writings',
        'directory': 'writings',
        'seoTitle': "Writings",
        'seoDescription': "Sometimes, I write stuff about computers, math, technology & design.",
        'template': {
            'index': 'listing.html',
            # 'details': 'details.html',
        },
        # 'multiple': ['writings', 'til'],
        "archive": True,
        'root': False,
        'pagination': False
    },
    {
        'title': 'TIL Posts',
        'directory': 'til',
        'seoTitle': "Today I Learned",
        'seoDescription': "This project is a collection of short write-ups on the things that I learn on a day-to-day basis across a variety of fields such as Computer Science, Mathematics, Software Engineering and Digital Design.",
        'template': {
            'index': 'listing.html',
            'details': 'details.html',
        },
        "archive": False,
        'root': False,
        'pagination': False
    },
    {
        'title': 'About page',
        'directory': 'about',
        'template': {
            'index': 'about.html',
        },
        'archive': False,
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