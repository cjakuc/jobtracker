from app import app, db
from app.models import User, Resume, Listing

# This allows us to do 'flask shell' in the terminal and have
## access to the app, as well as whatever we pre-load or add to
### the context here
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Resume': Resume, 'Listing': Listing}
    # Check it out using:
    ## flask shell
    ## >>> db
    ## >>> User
    ## >>> Resume
    ## >>> Listing