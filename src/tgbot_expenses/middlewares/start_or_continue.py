from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.helpers.keyboards.start_over_or_continue import \
    get_keyboard_start_over_or_continue
from src.tgbot_expenses.states.chat_states import StateChat


class StartOrContinueMiddleware(BaseMiddleware):
    """Start or continue middleware"""
    async def on_pre_process_message(self, message: types.Message,
                                     data: dict) -> None:
        """
        On pre process messages
        """
        current_state = await Bot.get_current_state()

        if current_state is None:
            return None

        if message.content_type == "text" and "/start" == message.text.strip():
            await message.delete()

            await Bot.answer(
                message=message,
                text=QuestionText.start,
                reply_markup=str(get_keyboard_start_over_or_continue())
            )

            raise CancelHandler()

    async def on_pre_process_callback_query(self, query: types.CallbackQuery,
                                            data: dict) -> None:
        """
        On pre process callback query
        """
        current_state = Bot.dispatch.current_state()

        if query.data in ["start_over", "continue"]:
            await Bot.delete_message(chat_id=query.message.chat.id,
                                     message_id=query.message.message_id)
            if query.data == "start_over":
                await Bot.delete_message(chat_id=query.message.chat.id,
                                         message_id=query.message.message_id-2)

                await current_state.reset_data()

                await StateChat.MainMenu.set()

                await Bot.answer(
                    message=query.message,
                    text=QuestionText.main_menu,
                    reply_markup=str(get_keyboard_main_menu())
                )

            raise CancelHandler()


__all__ = ["StartOrContinueMiddleware"]
