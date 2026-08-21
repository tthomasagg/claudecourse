import os
from dotenv import load_dotenv
from anthropic import Anthropic
import argparse

load_dotenv()

DEFAULT_TEMPERATURE = 0.5
DEFAULT_MAX_TOKENS = 1000

parser = argparse.ArgumentParser(description="Simple Claude API-based AI chatbot")
parser.add_argument("--model", type=str, required=False, help="Claude model to use")
parser.add_argument("--response-mode", type=str, required=False, help="Claude response mode. [stream | sync]. Default = stream", default="stream")
args = parser.parse_args()


client = Anthropic()
model = args.model if args.model else os.getenv("DEFAULT_CLAUDE_MODEL")

def add_user_message(messages, text):
	user_message = {"role": "user", "content": text}
	messages.append(user_message)

def add_assistant_message(messages, text):
	assistant_message = {"role": "assistant", "content": text}
	messages.append(assistant_message)

def build_chat_params(msg_history, system=None, chat_model=model, max_tokens=DEFAULT_MAX_TOKENS, temperature=DEFAULT_TEMPERATURE):
	params = {
		"messages": msg_history,
		"model": chat_model,
		"max_tokens": max_tokens,
		"temperature": temperature
	}

	if system:
		params["system"] = system

	return params

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
def chat(msg_history, system=None, temperature=DEFAULT_TEMPERATURE, response_mode=args.response_mode):

	params = build_chat_params(msg_history, system, model, DEFAULT_MAX_TOKENS, temperature)

	if args.response_mode == "sync":
		response = client.messages.create(**params)
		print(response.content[0].text)
	else:
		with client.messages.stream(
				**params
		) as stream:
			for text in stream.text_stream:
				print(text, end="")
		response = stream.get_final_message()

	print("\n")

	return response.content[0].text

messages = []

while True:
	user_input = input("> ")
	add_user_message(messages, user_input)
	# system prompt exercise
	#answer = chat(messages, "Act as a code generator. When writing code: don't comment on every line; Don't provide alternatives; don't provide usage examples; Just output code as if you were writing directly to the interpreter")
	answer = chat(messages)
	add_assistant_message(messages, answer)