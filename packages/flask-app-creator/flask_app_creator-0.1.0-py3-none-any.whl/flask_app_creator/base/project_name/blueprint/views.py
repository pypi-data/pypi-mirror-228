from flask import Blueprint

bp = Blueprint(
    'blueprint',
    __name__,
    url_prefix='/blueprint',
    template_folder='templates',
    static_folder='static',
)


@bp.get('/')
def index():
    return 'Hello World, now in blueprint'
