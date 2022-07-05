# Custom configuration for the website

# General configuration for the blog
site = {
    "name": "megacolorboy",
    "url": "https://www.megacolorboy.com",
    "author": "Abdush Shakoor",
    "theme": "minimalist-v2",
    "logo": "logo.gif",
    "enable_archive": True,
    "enable_tags": False,
    "export_rss_feed": False,
    "export_json": False
}

# Sections configuration
sections = [
	{
        'title': 'Home',
        'url': '/',
        'seo': {
            'title': "Abdush Shakoor's Weblog",
            'description': "Writings, experiments & ideas"
        },
        'page_type': 'main',
        'display_in_menu': True,
        'enable_listing': True,
        'enable_pagination': True
    },
    {
		'title': 'About',
		'url': '/about',
        'content_directory': "about",
        'seo': {
            'title': "A little bit about myself",
            'description': "Here's a not-so-formal kind of introduction about myself."
        },
        'page_type': 'single',
        'display_in_menu': True
	},
	{
		'title': 'Writings',
		'url': '/writings',
        'content_directory': "writings",
        'seo': {
            'title': "Writings",
            'description': "Sometimes, I write stuff about computers, math, technology & design."
        },
        'page_type': 'multiple',
        'display_in_menu': True,
        'enable_listing': True,
        'enable_pagination': True,
        'show_in_recent_articles': True
	},
	{
		'title': 'Today I Learned',
		'url': '/til',
        'content_directory': "til",
        'seo': {
            'title': "Today I Learned",
            'description': "A collection of short write-ups on the things that I learn on a day-to-day basis."
        },
        'page_type': 'multiple',
        'display_in_menu': True,
        'enable_listing': True,
        'enable_pagination': True,
        'show_in_recent_articles': True
	}
	# {
	# 	'title': 'Resume',
	# 	'url': '/resume',
 #        'content_directory': "resume",
 #        'data_type': 'json',
 #        'seo': {
 #            'title': "Resume",
 #            'description': "My resume"
 #        },
 #        'page_type': 'custom',
 #        'display_in_menu': False,
 #        'template': {
 #            'custom': "resume.html"
 #        }
	# }
]


# The template for storing meta information of the blog post
METATEMPLATE = """
title: {title}
date: {date}
slug: {slug}
category: {category}
tags: your, tags, here
summary: Write your summary here.
status: inactive

Start writing your content here.
"""