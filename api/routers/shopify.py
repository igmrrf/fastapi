from typing import Dict
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import shopify
import os
from fastapi import APIRouter

load_dotenv()
router = APIRouter()

access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
api_version = os.getenv("SHOPIFY_API_VERSION")
shop_url = os.getenv("SHOPIFY_SHOP_URL")
shop_name = os.getenv("SHOPIFY_SHOP_NAME")


def activate_shopify_session():
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    shopify.Shop.current()
    return shopify


@router.get("/shopify")
def shopify_session():
    # activate shopify
    activate_shopify_session()

    # get products
    # count products
    # get orders
    # count orders
    # get saved current order index
    # send next 150 orders to MOD
    # mark orders and update current order index

    product = shopify.Product.find()
    print(product)
    return {"Hello": "World"}


@router.get("/shopify/count")
def count_shopify_products() -> Dict[str, int]:
    activate_shopify_session()

    count = shopify.Product.count()
    return {"count": count}


@router.get("/shopify/orders")
def shopify_orders(page: int, limit: int) -> JSONResponse:
    activate_shopify_session()
    orders = shopify.Order.find(limit=limit)
    # next_page = orders.has_next_page()
    # print(next_page)
    print(page)
    return JSONResponse({"orders": [order.to_dict() for order in orders]})


@router.get("/shopify/orders/new")
def shopify_new_orders(page: str, limit: str) -> Dict[str, int]:
    activate_shopify_session()
    orders = shopify.Order.find(status="open", limit=limit, page=page)
    # next_page: bool = orders.has_next_page()
    print(orders)
    return {"count": len(orders)}
