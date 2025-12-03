from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserListResponse(BaseModel):
    users: dict[str, str]


class UserConfigResponse(BaseModel):
    uri: str
