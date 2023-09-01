{
    "name": "Migration wordpress",
    "version": "14.0.1.0.0",
    "depends": ["website"],
    "author": "Coopdevs Treball SCCL",
    "category": "Tools",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Wordpress migration, Sythil Tech module migrated to Odoo14.
    """,
    "description": "Copy data (pages, media) from wordpress CMS into Odoo",
    "data": [
        "data/res_groups.xml",
        "security/ir.model.access.csv",
        "views/migration_import_wordpress_views.xml",
        "views/menus.xml"
    ],
    "images":[
        "static/description/1.jpg"
    ],
    "installable": True,
}
