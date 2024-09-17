from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()



engine = create_engine('sqlite:///my_database.db')
Base = declarative_base()