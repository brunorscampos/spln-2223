# Modules for TP1
import sys
import pymongo
import requests
# Misc
import datetime
from PIL import Image
from io import BytesIO
# Init variables
config = {}
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Load config file
def load_config():
    f = open("config","r")
    c = f.read()
    for line in c.split("\n"):
        key,value = line.split(":")
        config[key] = value
    global db,collection,headers
    db = client["askGPT"]
    collection = db[config["mongocollection"]]
    headers = {"Authorization": f"Bearer {config['key']}"}
    f.close()

# Save config to file
def save_config():
    f = open("config","w")
    f.write(f"""key:{config["key"]}
mongocollection:{config["mongocollection"]}
context:{config["context"]}""")
    f.close()

# Get user input with tag (e.g. "askGPT-general> ")
def get_input(tag):
    sys.stdout.write(tag)
    sys.stdout.flush()
    line = sys.stdin.readline()
    return line.strip()

# Ask ChatGPT
def ask_chatgpt(question):
    prompt = f"Q: {question}\nA:"
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", 
        headers=headers, 
        json={"model": "gpt-3.5-turbo", 
              "messages": [
                {"role": "system", "content": config["context"]},
                {"role": "user", "content": question}
        ]})
    answer = response.content.decode("utf-8")
    start_index = answer.find('"content":"') + len('"content":"')
    end_index = answer.find('"}', start_index)
    answer = answer[start_index:end_index]
    if response.status_code == 200:
        collection.insert_one({"type":"chat",
                               "context": config["context"],
                               "prompt": question, 
                               "answer": answer,
                               "date": datetime.datetime.now().strftime("%Y-%m-%d")
                               })
    return answer

# Generate ChatGPT image
def generate_image(question,filename):
    global headers
    response = requests.post("https://api.openai.com/v1/images/generations", 
                             headers=headers, 
                             json={
                                 "model": "image-alpha-001", 
                                 "prompt": question
                                 })
    if response.status_code == 200:
        image_data = response.json()["data"][0]["url"]
        response = requests.get(image_data)
        image = Image.open(BytesIO(response.content))
        image.save("imgs/"+filename)
        print("Saved image at:","imgs/"+filename)
        collection.insert_one({"type":"image",
                               "prompt": question, 
                               "answer": image_data,
                               "date": datetime.datetime.now().strftime("%Y-%m-%d")
                               })
    else:
        print(response.content)

# Find MongoDB documents that include the terms in the question or answer.
def find_entries(terms):
    if not len(terms):
        results = collection.find({},{"_id": 0})
    else:
        query = {
            "$or": 
                [{"prompt": {"$regex": term, "$options": "i"}} for term in terms]
                +
                [{"answer": {"$regex": term, "$options": "i"}} for term in terms]
        }
        results = collection.find(query,{"_id": 0})
    num_matches = len(list(results.clone()))
    if num_matches > 0:
        print(f"\nSearch concluded with {num_matches} " + ("matches" if num_matches != 1 else "match") + " found!")
        print("=" * 40)
        for result in results:
            print(f"Type: {result['type']}")
            if result['type'] == "chat":
                print(f"Context: {result['context']}")
            print(f"Prompt: {result['prompt']}")
            print(f"Answer: {result['answer']}")
            print(f"Date: {result['date']}")
            print("-" * 40)
    else:
        print("\nNo matches found!\n")

# Delete MongoDB documents that include the term in the question or answer.
def delete_entries(term,mode):
    query = {"$or": [
        {"prompt": {"$regex": term, "$options": "i"}},
        {"answer": {"$regex": term, "$options": "i"}}
    ]}
    if mode == "one":
        result = collection.delete_one(query)
    else:
        result = collection.delete_many(query)
    print(f"Deleted {result.deleted_count} documents!")
        

def handle_exit(c):
    """
    Usage: exit
    Exit the program and close the MongoDB client.
    """
    if len(c):
        print("Usage: exit")
    else:
        client.close()
        return True

def handle_ask(c):
    """
    Usage: ask
    Prompts ChatGPT, and prints the answer.
    Also creates a document in current MongoDB collection with type, prompt, answer and date fields.
    """
    if len(c):
        print("Usage: ask")
    else:
        input = get_input("Question> ")
        answer = ask_chatgpt(input)
        print(answer)

def handle_context(c):
    """
    Usage: context
    Set the context for ChatGPT to use in generating answers.
    """
    if len(c):
        print("Usage: context")
    else:
        config["context"] = get_input("Context> ")
        save_config()

def handle_find(c):
    """
    Usage: find
    Search for documents in the current MongoDB collection that match the given terms.
    If no terms are given, returns all documents in current MongoDB collection.
    """
    if len(c):
        print("Usage: find")
    else:
        terms = get_input("What terms should I search for?\nTerms> ").split()
        find_entries(terms)

def handle_image(commands):
    """
    Usage: image <output_filename>
    Generate an image based on the given prompt and save it to the given output file.
    Also creates a document in current MongoDB collection with type, prompt, answer and date fields.
    """
    if len(commands) != 1:
        print("Usage: image <output_filename>")
    else:
        input = get_input("Prompt> ")
        generate_image(input,commands[0])

def handle_delete(commands):
    """
    Usage: delete <one|many|all>
    Delete one or many documents from the MongoDB collection that match the given term.
    If "all" is provided as the argument, delete all documents in the collection.
    """
    if len(commands) != 1:
        print("Usage: delete <one|many|all>")
    else:
        if commands[0] in ["one","many"]:
            term = get_input("What term should I search for?\nTerm> ").split()
            delete_entries(term,commands[0])
        elif commands[0] == "all":
            choice = get_input("Are you sure?[y/N]> ").split()
            if choice == "y":
                result = collection.delete_many({})
                print(f"Deleted {result.deleted_count} documents!")
            else:
                print("Operation cancelled!")
        else:
            print("Invalid command. Usage: delete <one|many|all>")

def handle_use(commands):
    """
    Usage: use <collection_name>
    Set the current MongoDB collection to the given name.
    """
    if len(commands) != 1:
        print("Usage: use <collection_name>")
    else:
        global db, collection
        config["mongocollection"] = commands[0]
        collection = db[config["mongocollection"]]
        save_config()
    
def handle_help(commands):
    """
    Usage: help <command>
    Display information about the given command.
    """
    if len(commands) == 1:
        if commands[0] in command_handlers:
            print(f"{command_handlers[commands[0]].__doc__}")
        else:
            print(f"Invalid command: {commands[0]}")
    elif not len(commands):
        print("Available commands:")
        print("  exit    - Quit program")
        print("  ask     - Ask question to ChatGPT")
        print("  context - Set context for ChatGPT")
        print("  find    - Find entries in current MongoDB collection")
        print("  image   - Generate image based on a prompt")
        print("  delete  - Delete one, many or all entries from current MongoDB collection")
        print("  use     - Change current MongoDB collection")
        print("  help    - Show this help message\n")
        print("Type 'help <command>' for more information on a specific command.")
    else:
        print("Usage: help <command>")

# ... more functions ...

command_handlers = {
    "exit": handle_exit,
    "ask": handle_ask,
    "context": handle_context,
    "find": handle_find,
    "image": handle_image,
    "delete": handle_delete,
    "use": handle_use,
    "help": handle_help,
    # ... more commands ...
}

def askGPT(commands):
    if commands[0] in command_handlers:
        return command_handlers[commands[0]](commands[1:])
    print("ERROR: Invalid command!")
        
def main():
    exit = False
    load_config()
    if config["key"] == "OPENAI_API_KEY":
        print("ERROR: OpenAI API key necessary!\nPlace it in the 'key' field inside the config file!")
        return None
    while not exit:
        input = get_input(f"askGPT-{config['mongocollection']}> ")
        exit = askGPT(input.split())
    save_config()
    client.close()

if __name__ == "__main__":
    main()