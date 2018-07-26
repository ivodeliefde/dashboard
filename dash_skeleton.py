from dash import Dash

STYLESHEETS = ['normalize.css', 'bootstrap.min.css', 'dashboard.css']

class prettyDash(Dash):
    """Custom Dash class overriding index() method for local CSS support"""
    def _generate_css_custom_html(self):
        link_str = '<link rel="stylesheet" href="{}/{}">'
        static_url_path = '/static'
        return '\n'.join(link_str.format(static_url_path, path) for path in STYLESHEETS)

    def index(self, *args, **kwargs):
        scripts = self._generate_scripts_html()
        css = self._generate_css_dist_html()
        custom_css = self._generate_css_custom_html()
        config = self._generate_config_html()
        title = getattr(self, 'title', 'Dashboard')
        return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
                {css}
                {custom_css}
            </head>
            <body>
                <div id="react-entry-point">
                    <div class="_dash-loading">
                        Loading...
                    </div>
                </div>
                <footer>
                    {config}
                    {scripts}
                </footer>
            </body>
        </html>
        '''