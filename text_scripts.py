text_dict = {
    'main_menu': 'Hello',
    'project_question': 'Write a question in the chat that interests you about the project.',
    'any_question': 'Write a question that interests you in the chat.',
    'img_generate': 'Write in the chat below a description for the photo you would like to generate',
    'img_analyze': 'Send a picture to the chat for analysis.',
    'wallet_analyze': 'Write in the chat below the address of the wallet you want to analyze.',
    'wallet_analyze_template': "📝 **Wallet Info** 📝\n\n"
                               "💎 **Wallet:** [{}](https://etherscan.io/address/{})\n"
                               "💰 **Current Balance: {} **\n"
                               "📈 **Profits in 30D: {} ETH**\n"
                               "🔒 **Tokens Hold:**\n"
                               " - {}\n\n"
                               "📊 **Last 10 trades** 📊\n\n"
                               "🟢 **Bought** ⤵️ Sort: Latest 🔼\n"
                               " - {}\n\n"
                               "🔴 **Sold:** ⤵️ Sort: Latest 🔼\n"
                               " - {}",
    'token_analyze': 'Write in the chat below the contract address of the token you want to analyze.',
    'coming_soon': 'This section is under development. Coming soon...'
}


openai_prompt = {
    'project_question_prompt': 'You need to answer users questions using the following information about the company:\n'
                               'Use the information below:\n'
                               'We are a company "Synthetic Ai Bot" specializing in telegram-based software development. \n'
                               'We want to create an excellent product for interacting with users using artificial intelligence technologies to generate pictures,\n'
                               'describe pictures, create an analysis of cryptocurrency tokens, analyze a wallet and much more.\n\n'
                               'Use only the information I give you, don’t take anything else from anywhere, so as not to misinform the user. You can also use emoticons to design text',
    'any_question_prompt': '',

}