from uuid import uuid4
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/packs", tags=["packs"])


class PackCreate(BaseModel):
    title: str


class Pack(BaseModel):
    id: str
    title: str
    status: str = "pending"


_packs: dict[str, Pack] = {}


@router.post("/", response_model=Pack)
async def create_pack(data: PackCreate) -> Pack:
    pack_id = str(uuid4())
    pack = Pack(id=pack_id, title=data.title)
    _packs[pack_id] = pack
    return pack


@router.post("/{pack_id}/build")
async def build_pack(pack_id: str) -> dict[str, str]:
    pack = _packs.get(pack_id)
    if not pack:
        raise HTTPException(status_code=404, detail="pack not found")
    pack.status = "ready"
    return {"status": "building"}
