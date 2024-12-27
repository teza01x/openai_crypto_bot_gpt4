import os

telegram_token = ''
token_metrics_api = ''
openai_api_key = ""
etherscan_api_key = ""
moralis_api_key = ""
data_base = os.path.join(os.path.dirname(__file__), 'database.db')

START_MENU_STATUS = 0
ASK_PROJECT_STATUS = 1
ASK_ANY_STATUS = 2
GENERATE_IMAGE = 3
ANALYZE_IMAGE = 4
ANALYZE_TOKEN = 5
ANALYZE_WALLET = 6
CRYPTO_NEWS = 7

project_signature = "\n\n ⚡️ [SyntheticAiBot](https://t.me/SyntheticAiBot) ⚡️"
image_dir_path = 'openai_images/'
