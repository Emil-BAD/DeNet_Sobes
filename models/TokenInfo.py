from pydantic import BaseModel

class TokenInfo(BaseModel):
    name: str
    symbol: str
    decimals: int
    total_supply: int | None = None