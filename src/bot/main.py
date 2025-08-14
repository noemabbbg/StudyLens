import asyncio
import httpx
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from ..config import get_settings

settings = get_settings()
bot = Bot(settings.tg_token or "")
dp = Dispatcher()
router = Router()
dp.include_router(router)


class NewPack(StatesGroup):
    title = State()
    id = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer("Привет! Используй /newpack чтобы создать набор.")


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    await message.answer("/start, /help, /quota, /newpack")


@router.message(Command("quota"))
async def cmd_quota(message: types.Message) -> None:
    await message.answer("Лимиты пока не считаем.")


@router.message(Command("newpack"))
async def wizard_new_pack(message: types.Message, state: FSMContext) -> None:
    await state.set_state(NewPack.title)
    await message.answer("Введите название набора:")


@router.message(NewPack.title)
async def set_title(message: types.Message, state: FSMContext) -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://api:8000/packs/", json={"title": message.text})
    data = resp.json()
    await state.update_data(pack_id=data["id"])
    await message.answer(f"Набор создан. ID: {data['id']}. Пришлите файлы.")
    await state.set_state(NewPack.id)


@router.message(NewPack.id, F.document | F.photo | F.audio)
async def upload_handler(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    pack_id = data.get("pack_id")
    await message.answer(f"Получен файл для набора {pack_id}.")


@router.message(Command("build"))
async def build_cmd(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    pack_id = data.get("pack_id")
    if not pack_id:
        await message.answer("Сначала создайте набор.")
        return
    async with httpx.AsyncClient() as client:
        await client.post(f"http://api:8000/packs/{pack_id}/build")
    await message.answer("Обработка запущена. Ожидайте уведомления.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
