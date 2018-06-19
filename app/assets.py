from flask_assets import Bundle, Environment, Filter

class ConcatFilter(Filter):
    """
    Filter that merges files, placing a semicolon between them.

    Fixes issues caused by missing semicolons at end of JS assets, for example
    with last statement of jquery.pjax.js.
    """
    def concat(self, out, hunks, **kw):
        out.write(';'.join([h.data() for h, info in hunks]))

js = Bundle(
    'node_modules/jquery/dist/jquery.js',
    'node_modules/jquery-pjax/jquery.pjax.js',
    'node_modules/bootbox/bootbox.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/bootstrap-datepicker/dist/js/bootstrap-datepicker.js',
    'node_modules/bootstrap-select/dist/js/bootstrap-select.js',
    'node_modules/blockui/jquery.blockUI.min.js',
    'node_modules/datatables.net/js/jquery.dataTables.min.js',
    'node_modules/datatables.net-bs/js/dataTables.bootstrap.min.js',
    'js/application.js',
    filters=(ConcatFilter, 'jsmin'),
    output='gen/packed.js'
)

css = Bundle(
    'node_modules/bootstrap/dist/css/bootstrap.css',
    'node_modules/font-awesome/css/font-awesome.css',
    'node_modules/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css',
    'node_modules/bootstrap-select/dist/css/bootstrap-select.css',
    'node_modules/datatables.net-bs/css/dataTables.bootstrap.min.css',
    'css/style.css',
    filters=('cssmin','cssrewrite'),
    output='gen/packed.css'
)

assets = Environment()
assets.register('js_all', js)
assets.register('css_all', css)
