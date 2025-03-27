# LLM tools

A simple Python package to encapsulate some useful functions for the LLM project.

## Installation

You can install it using pip:

```bash
pip install git+https://github.com/rainfishs/llmtools.git
```
## Usage

### Simple ChatBot
```python
from llmtools import ChatBot, UserMessage
# Create a ChatBot instance. If API key is provided in environment variable(OPENAI_API_KEY).
bot = ChatBot()

# Set ChatBot model.
model = "gpt-3.5-turbo"

# Get response from the ChatBot.
response = bot.ask([UserMessage("Hello, how are you?")], model=model)

# Print the response.
print(response)
```

### Continue the conversation
```python
from llmtools import ChatBot, UserMessage, AssistantMessage
# Create a ChatBot instance. If API key is provided in environment variable(OPENAI_API_KEY).
bot = ChatBot()

# Set ChatBot model.
model = "gpt-3.5-turbo"

# Create a UserMessage instance.
user_message = UserMessage("Hello, how are you?")

# Get response from the ChatBot.
response = bot.ask([user_message], model=model)

# Print the response.
print(response)

# Continue the conversation.
new_user_message = UserMessage("What is your name?")
conversation = [user_message, AssistantMessage(response), new_user_message]

new_response = bot.ask(conversation, model=model)

print(new_response)
```

### ChatBot with more options
```python
from llmtools import ChatBot, UserMessage, AssistantMessage

bot = ChatBot(base_url="SOME_CUSTOM_LLM_API_URL", api_key="YOUR_API_KEY")
model = "SOME_CUSTOM_MODEL"

try:
    conversation = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        conversation.append(UserMessage(user_input))
        response = ""
        print("Bot: ", end="")
        for text in bot.ask(conversation,
                            model=model,
                            temperature=0.5,
                            stream=True):
            if text == "":
                continue
            response += text
            print(text, end="")
        print()
        conversation.append(AssistantMessage(response))

except KeyboardInterrupt:
    print("Bye!")

```

### ChatBot with conversation manager
```python
from llmtools import ChatBot, ConversationManager

bot = ChatBot()
model = "gpt-3.5-turbo"

chat = ConversationManager(bot, model=model)

try:
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Bot: ", end="")
        for text in chat(user_input, stream=True):
            print(text, end="")
        print()

except KeyboardInterrupt:
    print("\nBye!")

```