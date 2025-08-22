import os
import logging
from dotenv import load_dotenv
from telegram.ext import (Application, CommandHandler, MessageHandler, filters,
                          ConversationHandler, CallbackQueryHandler)
from telegram import (Update, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove)

from database.models import init_db, SessionLocal
from handlers.start import start, help_command, cancel
from handlers.order import (order_start, size_selection,
                            references_handler, confirm_order)
from handlers.tracking import track_order
from handlers.admin import admin_panel, confirm_order_admin, update_tracking


load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
SIZE, REFERENCES, CONFIRMATION = range(3)

def main():
    init_db()
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("track", track_order))
    application.add_handler(CommandHandler("admin", admin_panel))
    order_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('order', order_start)],
        states={
            SIZE: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, size_selection)],
            REFERENCES: [
                MessageHandler(filters.PHOTO, references_handler),
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, references_handler)
            ],
            CONFIRMATION: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, confirm_order)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(order_conv_handler)

    application.add_handler(CallbackQueryHandler(
        confirm_order_admin, pattern="^confirm_"))
    application.add_handler(CallbackQueryHandler(
        update_tracking, pattern="^track_"))
    application.run_polling()


if __name__ == '__main__':
    main()
