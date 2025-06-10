from pydantic import BaseModel, field_validator
from datetime import datetime

class ResponseTransfer(BaseModel):
    """Модель для данных о трансферах токенов из Moralis API."""
    token_name: str
    block_timestamp: datetime
    transaction_hash: str
    from_address: str
    to_address: str
    value: int
    possible_spam: bool
    
    @field_validator('block_timestamp', mode='before')
    def parse_block_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value
    
    @field_validator('value', mode='before')
    def parse_value(cls, value):
        if isinstance(value, str):
            return int(value)
        return value
    