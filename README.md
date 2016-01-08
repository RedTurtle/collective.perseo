.. contents::

WARNING
=======

Version 0.7a is not compatible with previous releases. Use at your own risk.


Introduction
============

Search Engine Optimization Package

Features
--------

With collective.perseo you can manage several kind of SEO features.

Globally
~~~~~~~~
Configurations applied to each page of the site, through 'PerSEO' tool under Add-on Configuration:
	- Webmaster Tools
	- tag title, description and keywords meta tags, separately for:
		- Home page
		- Single pages
		- Search page
		- Not Found page
		- Author page
		- Site Map page
		- Contact page
		- Event
		- File
		- Folder
		- Image
		- Link
		- News Item
		- Topic
	- Disable the indexing of resources using noindex and nofollow, separately for:
		- Search page
		- Login and Registration pages
		- Administration pages
		- Single pages
		- Event
		- File
		- Folder
		- Image
		- Link
		- News Item
		- Topic
		- (also handle noodp, noydir, noarchive, nosnippet)
	- Content types included in the sitemap.xml.gz
	- Ping sites (Google, Bing, Ask) automatically when the Site Map is updated
	- Indexing RSS feeds
	- Add itemscope and itemtype attributes to body tag (if you install the extension collective.perseoschema per Schema org)

One by one
~~~~~~~~~~
Through 'SEO' tab on each content of the site (allows you to change SEO settings for that specific content):
	- tag title and description and Keywords meta tags
	- Meta Robots Follow Tag (follow/nofollow)
	- Meta Robots Index Tag (index/noindex)
	- Meta Robots Advanced Tag (noodp, noydir, noarchive, nosnippet)
	- Canonical URL
	- Content included in the sitemap.xml.gz (yes/no).
	- Priority of content in sitemap.xml.gz
	- itemtype attribute (if you install the extension collective.perseoschema per Schema org)

SCHEMA.ORG
----------

For Schema.org attributes add the collective.perseoschema package.

Warning! Installing collective.perseoschema package, the main_template and plone.path_bar, 
plone.global_sections, plone.header viewlets will be customized, to insert Schema.org attributes.
The customizations of these resources in other Themes and Skins could be disabled.

If you don't want to install the collective.perseoschema package, but you still want Schema.org
attributes, the following are the customizations you can do in your theme.


Customizations of plone.path_bar viewlet at these points:

- Line 2 of path_bar.pt, added itemprop attribute, itemprop="breadcrumb"::
	
	<div id="portal-breadcrumbs"
		 itemprop="breadcrumb"
	...

Customizations of plone.global_sections viewlet at these points:

- Line 1 of section.pt,
  added itemscope and itemtype attributes in tag nav, itemtype="http://schema.org/SiteNavigationElement"::
	
	<nav itemscope="itemscope"
		 itemtype="http://schema.org/SiteNavigationElement">
		 ...
	</nav>

Customizations of plone.header viewlet at these points:

- Line 2 of portal_header.pt,
  added itemscope and itemtype attributes, itemtype="http://schema.org/WPHeader"::
	
	<div id="portal-header"
		 itemscope="itemscope"
	     itemtype="http://schema.org/WPHeader">
	     ...
     
Customizations of sunburst_templates / main_template at these points:

- Line 18, Taken value of "Add itemscope and itemtype attributes to body tag" field,
  from Plone SEO Configuration, and value of "itemtype attribute" field from SEO tab::
  	
	...
	<html xmlns="http://www.w3.org/1999/xhtml" 
	    tal:define="
	        ...
	        perseo_context nocall: context/@@perseo-context;
			itemscope_itemtype python:perseo_context.perseo_itemscope_itemtype();
			itemtype python:perseo_context.perseo_itemtype()"
	...

- Line 61, Added itemscope and itemtype attributes (according to previous values)::
	
	...
	<body ...
	    tal:attributes="...
	                    itemscope python:itemscope_itemtype and 'itemscope' or None;
	                    itemtype python:itemscope_itemtype and itemtype or None">
	...

- Line 94, Added itemprop attribute, itemprop="mainContentOfPage"::
	
	...
	<div id="content" itemprop="mainContentOfPage">
	...

- Line 149, Added itemscope and itemtype attributes, itemtype="http://schema.org/WPSideBar"::
	
	...
	<div id="portal-column-one"
		itemscope="itemscope"
		itemtype="http://schema.org/WPSideBar"
	...

- Line 161, Added itemscope and itemtype attributes, itemtype="http://schema.org/WPSideBar"::
	
	...
	<div id="portal-column-two"
		itemscope="itemscope"
		itemtype="http://schema.org/WPSideBar"
	...

- Line 176, Added itemscope and itemtype attributes, itemtype="http://schema.org/WPFooter"::
	
	...
	<div itemscope="itemscope" itemtype="http://schema.org/WPFooter">
		<div tal:replace="structure provider:plone.portalfooter" />
	</div>


Credits
=======

Developed with the support of `Andrea Pernici`__.

__ http://www.andreapernici.com/

collective.perseo is loosely based on quintagroup.seoptimizer.

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
