import os

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://lakehouse:{os.environ['META_DB_PASSWORD']}@meta-db:5432/superset"
WTF_CSRF_ENABLED = True
SUPERSET_WEBSERVER_TIMEOUT = 120
FEATURE_FLAGS = {"DASHBOARD_RBAC": False}
