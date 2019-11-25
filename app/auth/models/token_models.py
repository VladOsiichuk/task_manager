import datetime
from typing import Dict, Union

from pydantic import BaseModel


class TokenRefreshResponseModel(BaseModel):
    token: str
    expire_in: datetime.timedelta
