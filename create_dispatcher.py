from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import (
    menu_router, 
    test_mode_router, 
    problem_mode_router
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(
    menu_router, 
    test_mode_router, 
    problem_mode_router
)