from fastapi import APIRouter, status

import publisher
from core.dependencies import UOW, CurrentUserOrError
from schemas.exceptions import ExceptionErrorResponse
from schemas.scan import ScanRequest, ScanResultListResponse, ScanResultResponse
from services.scan import ScanService

router = APIRouter(
    prefix="/scans",
    tags=["scans"],
)


@router.post("/start",
             responses={
                 status.HTTP_200_OK: {
                     "model": ScanRequest
                 },
                 status.HTTP_401_UNAUTHORIZED: {
                     "model": ExceptionErrorResponse,
                     "description": "Invalid token",
                 },
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {
                     "description": "Backender lox sorry (",
                 }
             })
async def start_scan(uow: UOW, schema: ScanRequest, current_user: CurrentUserOrError):
    network = list(sorted(schema.network))
    network = ','.join(network)
    scan_result = await ScanService().create(uow, network)
    data = {
        'type': 'start_scan',
        'scan_result_id': scan_result.id,
        'network': network,
    }
    await publisher.send_to_queue('network-scanner', data)
    return {'id': scan_result.id}


@router.get("", response_model=ScanResultListResponse,
            responses={
                status.HTTP_200_OK: {
                    "model": ScanResultListResponse
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "model": ExceptionErrorResponse,
                    "description": "Invalid token",
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "description": "Backender lox sorry (",
                }
            })
async def get_scans_list(uow: UOW, current_user: CurrentUserOrError):
    response = await ScanService().get_list(uow, reverse=True, order_by='id')
    return response


@router.get("/{scan_id}", response_model=ScanResultResponse,
            responses={
                status.HTTP_200_OK: {
                    "model": ScanResultResponse
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "model": ExceptionErrorResponse,
                    "description": "Invalid token",
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "description": "Backender lox sorry (",
                }
            })
async def get_scans_list(uow: UOW, scan_id: int, current_user: CurrentUserOrError):
    response = await ScanService().get(uow, id=scan_id)
    return response
