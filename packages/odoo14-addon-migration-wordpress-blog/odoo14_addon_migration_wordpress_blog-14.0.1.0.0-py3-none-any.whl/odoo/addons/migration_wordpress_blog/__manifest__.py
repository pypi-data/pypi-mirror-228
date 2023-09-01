# -*- coding: utf-8 -*-
{
    'name': "Wordpress Migration - Blog Posts",
    'version': "14.0.1.0.0",
    'author': "Coopdevs",
    'category': "Tools",
    'summary': "Migration Wordpress Blog, Sythil Tech module migrated to Odoo14",
    'description': "Copies Wordpress blog posts and comments into Odoo",
    'license':'AGPL-3',
    'data': [
        'views/migration_import_wordpress_views.xml',
    ],
    'demo': [],
    'depends': ['migration_wordpress', 'website_blog'],
    'images':[
        'static/description/1.jpg',
    ],
    'installable': True,
}