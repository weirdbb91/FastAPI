from typing import List, Optional

from enum import Enum

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field


app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


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
