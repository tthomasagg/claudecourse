import os
from dotenv import load_dotenv
from anthropic import Anthropic
import argparse

load_dotenv()

parser = argparse.ArgumentParser(description="Simple Claude API-based AI chatbot")
parser.add_argument("--model", type=str, required=False, help="Claude model to use")
args = parser.parse_args()


client = Anthropic()
model = args.model if args.model else os.getenv("DEFAULT_CLAUDE_MODEL")

def add_user_message(messages, text):
	user_message = {"role": "user", "content": text}
	messages.append(user_message)

def add_assistant_message(messages, text):
	assistant_message = {"role": "assistant", "content": text}
	messages.append(assistant_message)

# temperature lesson
# 0.8 - 1.0 high temperature
# - brainstorming
# - creative writing
# - marketing content
# - jokes
# 0.4 - 0.7 - med. temp.
# - summarization
# - ed. content
# - problem-solving
# - creative writing with constraints
# 0.0 - 0.3 low temperature
# - factual responses
# - coding assistance
# - data extraction
# - content moderation
def chat(messages, system=None, temperature=0.5):

	params = {
		"model": model,
		"max_tokens": 1000,
		"messages": messages,
		"temperature": temperature
	}

	if system:
		params["system"] = system

	message = client.messages.create(**params)

	return message.content[0].text

messages = []

while True:
	user_input = input("> ")
	add_user_message(messages, user_input)
	# system prompt exercise
	#answer = chat(messages, "Act as a code generator. When writing code: don't comment on every line; Don't provide alternatives; don't provide usage examples; Just output code as if you were writing directly to the interpreter")
	answer = chat(messages)
	add_assistant_message(messages, answer)
	print(answer + "\n")