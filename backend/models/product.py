from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    titre: str = Field(..., description="Titre du produit")
    description: str = Field(..., description="Description du produit")
    prix: str = Field(..., description="Prix")
    image_url: str = Field(..., description="URL de l’image")
