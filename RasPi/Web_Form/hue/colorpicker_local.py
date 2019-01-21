from flask import Markup


class colorpicker(object):
    def __init__(self, app=None):
        self.app = app
        if self.app is not None:
            self.init_app(app)
        else:
            raise(AttributeError("must pass app to colorpicker(app=)"))
                
        self.injectThem()  # injecting module into the template


    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def injectThem(self):
        """ to inject the module into the template as colorpicker """
        @self.app.context_processor
        def inject_vars():
            return dict(colorpicker=self)

    def loader(self):
        html = ""
        for i, n in enumerate(['js', 'css']):

            # IMPORTANT
            # Update the links for your settings

            links = ['http://127.0.0.1:5000/get_media/spectrum.css',
                     'http://127.0.0.1:5000/get_media/spectrum.js'] 
            tags = [
            '<script src="%s"></script>\n',
            '<link href="%s" rel="stylesheet">\n'
            ] 
            html += tags[i] % [
                l for l in links if l.split(
                    '.')[len(l.split('.')) - 1] == n][0]

        return Markup(html)


    def picker(self, ids=[".colorpicker"],
               default_color='rgb(0,0,255)',
               color_format='rgb',
               showAlpha='true',
               showInput='false',
               showButtons='false',
               allowEmpty='true'):
       
        """
        to get html ready colorpicker initiation with the given options

        @param: ids list of identifiers of the html element to assign the color picker to (Default: '.colorpicker')
        @param: default_color for the colorpicker to start with (Default: 'rgb(0,0,255)')
        @param: color_format color format to use (Default: 'rgb')
        @param: showAlpha to enable alpha (Default: 'true')
        @param: showInput to show or hide the color format (Default: 'false')
        @param: showButtons to show or hide buttons (Default: 'false')
        @param: allowEmpty to allow or disallow empty input (Default: 'true')

        """

        for h, a in {'showAlpha': showAlpha,
                     'showInput': showInput,
                     'showButtons': showButtons,
                     'allowEmpty': allowEmpty}.items():
            if not isinstance(a, str):
                raise(TypeError("colorpicker.picker(%s) takes string" % h))
            if h != 'id' and a != 'true' and a != 'false':
                raise(TypeError(
                    "colorpicker.picker(%s) only true or false string" % h))
            if not isinstance(ids, list):
                raise(TypeError("colorpicker.picker(ids) requires a list of strings"))
        html = ""
        for id in ids:
            html += " ".join([
                '<script> $(document).ready(function () {'
                '$("%s").spectrum({' % id,
                'showAlpha: %s,' % showAlpha,
                'showInput: %s,' % showInput,
                'showButtons: %s,' % showButtons,
                'allowEmpty: %s,' % allowEmpty,
                'color: $("%s").val() || "%s",' % (id, default_color),
                'preferredFormat: "%s",' % color_format,
                'move: function(color) {',
                '$(this).val(color.toRgbString())',
                '},', '})',
                '}) </script>'])
                
        return Markup(html) # html ready colorpicker