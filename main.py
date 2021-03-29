from typing import List, Set, Dict, Optional

from enum import Enum

from fastapi import Body, Coookie, FastAPI, Path, Query, Form
from pydantic import BaseModel, HttpUrl, Field, EmailStr


app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Image(BaseModel):
    url: HttpUrl
    name: str


# 클래스 내부 값에도 Field를 사용해 조건을 추가할 수 있음
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


# 코드 재사용 : 클래스
# class Animal(BaseModel):
#     name: str = Field(..., min_length=1, max_length=10)
#     height: int = Field(..., gt=0, le=1000)
#
#
# class Rabbit(Animal):
#     speed: int = Field(..., ge=0)
#
#
# class Abalone(Animal):
#     pass


# Response Model 객체 형태로 반환
# In 클래스로 비밀번호를 포함해 받아 Out 클래스로 비밀번호를 제외해 반환
# response_model_exclude_unset 옵션으로 default 값으로 초기화 대신 실제 입력된 값만 받음
@app.post("/user/", response_model=UserOut, response_model_exclude_unset=True)
async def create_user(user: UserIn):
    return user


# @app.get("/items/")
# 쿠키 파라미터
# async def read_items(ads_id: Optional[str] = Cookie(None)):
# 헤더 파라미터
# _ to -, case-insensitive 옵션을 끄려면 Header(None, convert_underscores=False)
# async def read_items(user_agent: Optional[str] = Header(None)):
# 중복 헤더
# async def read_items(x_token: Optional[List[str]] = Header(None)):
#     return {"X-Token values": x_token}
# 중복 헤더 결과물
# X-Token: foo
# X-Token: bar


@app.post("/index-weights/")
async def create_index_weights(weights: Dect[int, float]):
    return weights


@app.post("/images/multiple/")
async def create_multiple_images(*, images: List[Image]):
    return images


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


# Body값으로 받는 클래스 파라미터를 해당 자료형 이름으로
# 랩핑해서 받으려면 Body의 embed 기능을 사용하면 된다
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


# 결과값
# embed=True -> "item": {}로 랩핑됨
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }


# 단일값을 그대로 선언하면 쿼리 파라미터로 받아들이지만,
# Body 클래스를 사용하면 FastAPI는 또 다른 내부 바디 키롤 받아들인다
# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: int, item: Item, user: User, importance: int = Body(..., gt=0)
# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     return results


# 결과값
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }


# 다수의 클래스 파라미터 입력
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, user: User):
#     results = {"item_id": item_id, "item": item, "user": user}
#     return results


# 자 조건문 greater than(gt), less than(lt), gt or equal(ge), lt or equal(le)
# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int = Path(..., title="The ID of item to get", ge=0, le=1000),
#     q: Optional[str] = None,
#     item: Optional[Item] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results


# 결과물 Response body
# {
#   "item_id": 1,
#   "q": "additional",
#   "item": {
#     "name": "The name",
#     "description": "string",
#     "price": 0,
#     "tax": 0
#   }
# }


# 첫번째 파라미터로 *를 받으면 순서 무관
# @app.get("/items/{item_id}")
# async def read_items(
#     *,
#     item_id: int = Path(..., title="The ID of the item to get"),
#     q: str,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items/")
# async def read_items(
#     q: Optional[str] = Query(
#         None,
#         alias="item-query",
#         title="Query string",  # 현재 title은 작동 안함
#         description="Query string for the items to search in the database that have a good match",
#         min_length=3,
#         max_length=50,
#         regex="^fixedquery$",
#         deprecated=True,
#     )
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# ...로 필수 파라미터 지정 가능
# @app.get("/items/")
# async def read_items(q: str = Query(..., min_length=3)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# 리스트 파라미터 입력 (List[str] 대신 list로 대체 가능)
# @app.get("/items/")
# async def read_items(q: List[str] = Query(["foo", "bar"])):
#     query_items = {"q": q}
#     return query_items


# Query 첫번째 파라미터는 디폴트값, 이 후 조건들
# @app.get("/items/")
# async def read_items(q: Optional[str] = Query("fixedquery", min_length=3, max_length=50, regex="^fixedquery$")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_item(user_id: int):
    return {"user_id": user_id}
