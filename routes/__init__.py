# from .auth import *
# from .admin import *
# from .teacher import *
# from .student import *

# from .auth import *
# from .admin import *
# from .teacher import *
# from .student import * 

from .auth import register_auth_routes
from .admin import register_admin_routes
from .teacher import register_teacher_routes
from .student import register_student_routes

def register_routes(app, db):
    register_auth_routes(app, db)
    register_admin_routes(app, db)
    register_teacher_routes(app, db)
    register_student_routes(app, db) 