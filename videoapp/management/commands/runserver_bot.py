from django.core.management.base import BaseCommand
import os
import sys
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
load_dotenv(env_path)

# Add bot directory to Python path
bot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../bot'))
if bot_dir not in sys.path:
    sys.path.insert(0, bot_dir)

from telegram_bot import main, init_client

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        # Get Telegram credentials with better error handling
        try:
            api_id = os.environ.get('API_ID')
            if not api_id:
                raise ValueError("API_ID not found in environment variables")
            api_id = int(api_id)

            api_hash = os.environ.get('API_HASH')
            if not api_hash:
                raise ValueError("API_HASH not found in environment variables")

            bot_token = os.environ.get('BOT_TOKEN')
            if not bot_token:
                raise ValueError("BOT_TOKEN not found in environment variables")

        except ValueError as e:
            self.stderr.write(f'Environment variable error: {e}')
            return
        except Exception as e:
            self.stderr.write(f'Unexpected error with environment variables: {e}')
            return

        self.stdout.write('Starting Telegram bot...')
        
        # Initialize and run the bot
        try:
            client = init_client(
                api_id=api_id,
                api_hash=api_hash,
                bot_token=bot_token
            )

            with client:
                client.loop.run_until_complete(
                    main(
                        api_id=api_id,
                        api_hash=api_hash,
                        bot_token=bot_token
                    )
                )
        except KeyboardInterrupt:
            self.stdout.write('Bot stopped by user')
        except Exception as e:
            self.stderr.write(f'Error running bot: {str(e)}')
