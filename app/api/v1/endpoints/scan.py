from fastapi import APIRouter

import publisher
from schemas.scan import ScanRequest

router = APIRouter(
    prefix="/scan",
    tags=["scan"],
)


@router.post("/start")
async def start_scan(schema: ScanRequest):
    data = {
        'type': 'start_scan',
        'network': schema.network,
    }
    await publisher.send_to_queue('network-scanner', data)
    return schema
