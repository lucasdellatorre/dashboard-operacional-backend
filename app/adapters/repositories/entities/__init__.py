import os
import importlib
from app.infraestructure.database.db import db

models_dir = os.path.dirname(__file__)
for filename in os.listdir(models_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"app.adapters.repositories.entities.{filename[:-3]}"
        importlib.import_module(module_name)