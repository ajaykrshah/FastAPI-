from pydantic import BaseModel
class ScriptInfo(BaseModel):
    name: str
    path: str
    url: str
