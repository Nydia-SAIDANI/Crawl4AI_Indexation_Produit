from pydantic import BaseModel

class ProductInfo(BaseModel):
    titre: str
    description: str
    prix: str
    image: str
