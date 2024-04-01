import sys
import openai
import signal
import os
import traceback
import time
import traceback
import tiktoken
import re

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError()

class ChatGPTCall(object):
    def __init__(self, api_key_file="api_key.txt", model_name="gpt-3.5-turbo"):
    # def __init__(self, api_key_file="api_key.txt", model_name="gpt-4"):
        self.api_key = self.load_api(api_key_file)
        self.model_name = model_name

    @staticmethod
    def load_api(api_key_file):
        if not os.path.exists(api_key_file):
            raise ValueError(
                f"API key not found: {api_key_file}.")
        with open(api_key_file, "r") as file:
            api_key = file.read().split("\n")[0]
        return api_key

    def ask_gpt(self, query):
        openai.api_key = self.api_key
        try:
            res = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant."},
                    # {"role": "user", "content": "Previous Prompts"},
                    # {"role": "user", "content": "Previous Queries"},
                    {"role": "system", "content": "You are a helpful assistant that understands programming languages."},
                    {"role": "user", "content": f"{query}"},
                ],
                # temperature=0
            )
            res = res.choices[0].message.content
        except TimeoutError:
            signal.alarm(0)  # reset alarm
            return "TIMEOUT, No response from GPT for 5 minutes"
        except Exception:
            print(traceback.format_exc())
            print("Error during querying, sleep for one minute")
            time.sleep(60)  # sleep for 1 minute
            res = self.ask_gpt(query)
        return res

    def query(self, query, timeout=60*5):
        """
        :param query: the query to ask GPT
        :param timeout: the timeout for the user's query
        :return: the response from GPT
        """
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)  # set timeout to 5 minutes
        try:
            response = self.ask_gpt(query)
        except TimeoutError:
            print("TIMEOUT ERROR!!!")
            return "TIMEOUT, No Response From GPT For 5 minutes"
        finally:
            signal.alarm(0)  # reset alarm
        return response


def test_timeout():
    chatGPTCall = ChatGPTCall()
    res = chatGPTCall.query("noop", timeout=1)
    assert res is None
    print("Test Timeout Pass!")

def get_answer(q):
    chatGPTCall = ChatGPTCall()
    res = chatGPTCall.query(q)
    # assert res is None
    return res


def test_api_key():
    try:
        chatGPTCall = ChatGPTCall("fake_path")
    except:
        print("Test Invalid API Key Pass")
    else:
        raise ValueError("Test Fail For Invalid API Key!")

def load_query(path):
        if not os.path.exists(path):
            raise ValueError(
                f"The File Is Not Found: {path}.")
        with open(path, "r") as file:
            query = file.read()
        return query
                    

def write_to_file(file_path, text):
    try:
        with open(file_path, "w+") as file:
            file.write(text)
        print("Saved to file.")
    except IOError:
        print("An error occurred while writing to the file.")


# def truncate_to_token_limit(text, token_limit):
#     # enc = tiktoken.get_encoding("p50k_base")
#     enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
#     # enc = tiktoken.encoding_for_model("gpt-4")
#     tokens = enc.encode(text)

#     if len(tokens) <= token_limit:
#         return text
    
#     truncated_tokens = tokens[:token_limit]
#     print(len(truncated_tokens))
#     truncated_text = enc.decode(truncated_tokens)
#     print("@@@ Truncated to token limit.")
#     return truncated_text

def tests_from_model(dir):
    prompt = 'Generate 10 different tests (written in P language code) for the below P DSL models and P specifications. The tests should check critical properties of the models.\n'
    model = load_models(dir)
    # code = truncate_to_token_limit(code, 3000)
    print('Generating tests ...')
    arch_desc = get_answer(prompt + model)
    return arch_desc

def load_models(directory_path):
    prompt = ""

    subdirectories = [entry for entry in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, entry))]

    # Iterating through the immediate subdirectories
    for subdirectory in subdirectories:
        if subdirectory == "PSrc":
            subdirectory_path = os.path.join(directory_path, subdirectory)
            prompt += "\n\nP models:\n---------\n" + get_code(subdirectory_path)
        if subdirectory == "PSpec":
            subdirectory_path = os.path.join(directory_path, subdirectory)
            prompt += "\n\nP specifications:\n---------\n" + get_code(subdirectory_path)
    return prompt

def get_code(subdirectory_path):
    code = ""
    files_in_subdirectory = [file for file in os.listdir(subdirectory_path) if os.path.isfile(os.path.join(subdirectory_path, file))]

    for file_name in files_in_subdirectory:
            if(file_name.endswith(".p")):
                full_path = os.path.join(subdirectory_path, file_name)
                if not os.path.exists(full_path):
                    raise ValueError(
                        f"The File Is Not Found: {full_path}.")
                with open(full_path, "r") as file:
                    query = file.read()
                    code += "\n\n" + file_name + "\n\n:" + query
    return code


def extract_code(text):
    pattern = r'```(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        code = match.group(1)
        return code.strip()
    else:
        return None


def extract_functions_from_cpp(file_path):
    # Parse the C++ code
    decls = parse([file_path], config=utils.xml_generator_configuration_t())

    # Extract functions from the AST
    functions = [decl for decl in declarations.get_global_declarations(decls) if isinstance(decl, declarations.calldef_t)]
    return functions


######################################################

if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) > 1:
        directory_path = arguments[1]
    else:
        print("No argument provided.")
    
    # Generate digraph in one-shot
    # response = dot_from_src(os.path.join(subdirectory_path, file_name))
    response = tests_from_model(directory_path)

    write_to_file(directory_path + "/" + "_tests.txt", response)
    print("====================================")
