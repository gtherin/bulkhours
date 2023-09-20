from .poly2r import Poly2dr
from .poly1r import Poly1dr
from .tools import md, html
from .math_table import MathTable
from . import td1
from . import td2
from .vector import Vector, VectorGrid

def display_warning():
    html("""🚧🚧🚧🚧<font color="red">Cette page est un brouillon de correction. 
Il y a donc beaucoup encore d'erreurs. Merci de reporter les erreurs à guillaume.therin@ipsa.fr
</font>🚧🚧🚧🚧<br/><br/>
⚠️⚠️⚠️⚠️<b>ATTENTION DE BIEN EXECUTER LA PREMIERE CELLULE POUR QUE LA PAGE S'EXECUTE</b>⚠️⚠️⚠️⚠️""")