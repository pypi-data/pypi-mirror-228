from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class CustomHeaderPlugin(BasePlugin):

    def on_page_content(self, html, page, config, files):
        header = f'<div class="custom-header">WELCOME TO MKDOCS ABHI</div>'
        return header + html
    
    def on_post_page(self, output, page, config):
        custom_css = '<style>.custom-header {background-color : #f2f2f2; padding: 10px } </style>'

        return custom_css + output