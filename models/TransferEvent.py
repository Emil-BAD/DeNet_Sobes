from pydantic import BaseModel, field_validator
from datetime import datetime

class TransferEvent(BaseModel):
    from_address: str
    to_address: str
    value: float
    block_timestamp: datetime
    transaction_hash: str

    @field_validator('block_timestamp')
    def parse_block_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value

    @field_validator('value')
    def parse_value(cls, value):
        if isinstance(value, (str, int)):
            return float(value) / 10**18
        return value