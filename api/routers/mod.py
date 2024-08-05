from pydantic import BaseModel


class ItemInfo(BaseModel):
    itemId: str
    size: str
    colour: str


class Order(BaseModel):
    username: str
    sellerUsername: str
    itemInfoList: list[ItemInfo]
    shippingMethod: str
    shippingTotal: float
    handlingTotal: float
    taxTotal: float
    customerEmail: str
    customerFName: str
    customerLName: str
    customerCompany: str
    customerAddress1: str
    customerCity: str
    customerState: str
    customerPostalCode: str
    customerCountry: str
    customerPhone: str


class Item(BaseModel):
    ownerUsername: str
    itemName: str
    quantityAvailable: int
    s3ImageLink: str
    s3ImageLinkSecondary: str
    price: float
    description: str


items: list[Item] = [
    Item(
        ownerUsername="npc",
        itemName="mog",
        quantityAvailable=200,
        s3ImageLink="https://picsum.photos/400",
        s3ImageLinkSecondary="https://picsum.photos/500",
        price=10.5,
        description="A beautiful MOG",
    )
]
