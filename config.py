import os

telegram_token = '6501432731:AAEpwpqGhEE_GR4vin8npDWJzNeLuYGD114'
token_metrics_api = 'tm-6d7cc4f6-86b6-4021-8745-a48faf3d5f0f'
openai_api_key = "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"
etherscan_api_key = "P4PHDAZI554S1P571PTE2E9ZZE6Z8DD82U"
# moralis_api_key = "thAV1Fskj6cjggoNDh33Awt1LMEOH0MN9sNi5LjTHldIaxWOuAXba6xYYA6ibGI7"
moralis_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImU4ODYzOTc3LTY3MjAtNGJlZC1iOWVhLWJlZTZmYWQ3YjU1NSIsIm9yZ0lkIjoiMzgwODU1IiwidXNlcklkIjoiMzkxMzQ0IiwidHlwZUlkIjoiYzY1YTY4NDAtZjBlNy00ZmI5LTlhNWItMGVmYTZjNzAxOWU1IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MDkzNjU4NDgsImV4cCI6NDg2NTEyNTg0OH0.BWMw_fbJnIIhr0wD-E7MplCp8TLvI1LaFJ9RxtRS3zc"
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