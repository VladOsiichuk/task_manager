import os
from datetime import timedelta

DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DEBUG = bool(os.getenv("DEBUG", False))


# JWT constants
# -----------------------------------------------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY", "ee47c846a633a29e500b1038316dbee99378d6eefd6ec5163384c401280ea857"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 10 * 24 * 60


JWT_SETTINGS = {
    "ALGORITHM": ALGORITHM,
    "ACCESS_EXPIRE_IN": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    "SECRET_KEY": SECRET_KEY,
    "REFRESH_EXPIRE_IN": timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
}
# -------------------------------------------------------------------------
