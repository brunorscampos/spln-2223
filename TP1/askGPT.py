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
    return answer

# Generate ChatGPT image
def generate_image(question,filename):
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json={"model": "image-alpha-001", "prompt": question})
    image_data = response.json()["data"][0]["url"]
    response = requests.get(image_data)
    image = Image.open(BytesIO(response.content))
    image.save("imgs/"+filename)
    print("Saved image at:","imgs/"+filename)

# find MongoDB documents that include the terms in the question or answer.
def find_entries(terms):
    query = {
        "$or": 
            [{"question": {"$regex": term, "$options": "i"}} for term in terms]
            +
            [{"answer": {"$regex": term, "$options": "i"}} for term in terms]
    }
    results = collection.find(query,{"_id": 0})
    num_matches = len(list(results.clone()))
    if num_matches > 0:
        print(f"\nSearch concluded with {num_matches} " + ("matches" if num_matches != 1 else "match") + " found!")
        for result in results:
            print("\nQuestion:",result['question'])
            print("Answer:",result['answer'])
            print("Date:",result['date'],"\n")
    else:
        print("\nNo matches found!\n")

# Functionalities of program
def askGPT(commands):
    global db,collection
    if len(commands) == 1:
        if commands[0] == "exit":
            client.close()
            return False
        elif commands[0] == "ask":
            input = get_input("Question> ")
            answer = ask_chatgpt(input)
            collection.insert_one({"question": input, "answer": answer,"date": datetime.datetime.now().strftime("%Y-%m-%d")})
            print(answer)
        elif commands[0] == "context":
            config["context"] = get_input("Context> ")
        elif commands[0] == "find":
            terms = get_input("What terms should I search for?\nTerms> ").split()
            find_entries(terms)
        else:
            print("ERROR: Invalid command!")
    elif len(commands) == 2:
        if commands[0] == "image":
            input = get_input("Prompt> ")
            generate_image(input,commands[1])
        elif commands[0] == "delete":
            if commands[1] in ["all","one","many"]:
                pass
        elif commands[0] == "use":
            config["mongocollection"] = commands[1]
            collection = db[config["mongocollection"]]
            save_config()
        else:
            print("ERROR: Invalid command!")
    else:
        print("ERROR: Invalid command!")
    return True
        
def main():
    flag = True
    load_config()
    while flag:
        input = get_input(f"askGPT-{config['mongocollection']}> ")
        flag = askGPT(input.split())
    save_config()

if __name__ == "__main__":
    main()