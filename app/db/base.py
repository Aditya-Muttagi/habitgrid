from sqlalchemy.orm import declarative_base
from fastapi.templating import Jinja2Templates


Base = declarative_base()

templates = Jinja2Templates(directory='app/template')


