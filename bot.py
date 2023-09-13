from FileShare import FileShareBot
from config import bot_token, api_hash, api_id

if __name__ == "__main__":
    FileShareBot(bot_token, api_id, api_hash).start()