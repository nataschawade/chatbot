"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import requests


@route('/', method='GET')
def index():
    return template("chatbot.html")
data = {
    'swear_words' :["shit", "merde","bitch","looser","fuck","asshole"],
    'swear_answers' :["You're a shit!", "I don't speak french","You're a bitch","it's not my fault i have no friends"],
    'whatsup' : ["hello","hey","good morning","good afternoon","hi"],
    "good_greetings" : ["good", "amazing", "fantastic", "super", "happy", "great"],
    'bad_greetings':["bad","not great","awful","sad","died"],
    'joke_selection':["Did you hear about the restaurant on the moon? Great food, no atmosphere.","What do you call a fake noodle? An Impasta.","How many apples grow on a tree? All of them.",
              "Want to hear a joke about paper? Nevermind it's tearable.","I just watched a program about beavers. It was the best dam program I've ever seen." ],
    'questions':["you?", "how you doing","whatsup", "what's up"],
    'answers':["Im a bit sad, my dog died", "I'm high","I'm doing great I just bought a new card","I'm excited, I'm going on holiday on tuesday"],
    'counter':0
}
#
# swear_words= ["shit", "merde","bitch","looser","fuck","asshole"]
# swear_answers =["You're a shit!", "I don't speak french","You're a bitch","it's not my fault i have no friends"]
# whatsup = ["hello","hey","good morning","good afternoon","hi"]
# good_greetings=["good","amazing","fantastic","super","happy","great"]
# bad_greetings=["bad","not great","awful","sad","died"]
# joke_selection=["Did you hear about the restaurant on the moon? Great food, no atmosphere.","What do you call a fake noodle? An Impasta.","How many apples grow on a tree? All of them.",
#           "Want to hear a joke about paper? Nevermind it's tearable.","I just watched a program about beavers. It was the best dam program I've ever seen." ]
# questions=["you?", "how you doing","whatsup", "what's up"]
# answers=["Im a bit sad, my dog died", "I'm high","I'm doing great I just bought a new card","I'm excited, I'm going on holiday on tuesday"]

def main_function(input, animation):
    message = input.lower()

    if "joke" in input:
        return jokes(), "giggling"

    for word in message.split():

        if word in data['whatsup']:
            return whatsup_answer(input), "excited"

        if any(word in message for word in data['bad_greetings']):
            return bad_greetings_answ(), "crying"

        if word in data['good_greetings']:
            return good_greetings_answ(),"excited"

        if word in data['swear_words']:
            return swear(input), "crying"

        if word in data['questions']:
            return about_me(), "dog"

    return hello(input), "ok"

def swear(input):
    new = input.split()
    for words in new :
        if words in data['swear_words']:
            index_input = data['swear_words'].index(words)
            output = data['swear_answers'][index_input]
            return output


def hello(name):
    data['counter'] +=1
    if data['counter'] == 1:
        return "hi {0}! So nice to meet you? How was your day?".format(name)
    else:
        return "Please ask me something else"

def whatsup_answer(whatsup):
    return "{0} you. How are you?".format(whatsup)

def good_greetings_answ():
    return "Great I'm happy to hear!"

def bad_greetings_answ():
    return "sorry to hear"

def jokes():
    return random.choice(data['joke_selection'])

def about_me():
    return random.choice(data['answers'])

def reset_counter():
    data['counter']=0
    return


# r = requests.get('https://api.github.com/events')
# print(r.text)
# print(r.status_code)
#
# r = requests.get('http://httpbin.org/get')
# print(r.headers['Access-Control-Allow-Credentials'])
# print(r.headers['Access-Control-Allow-Origin'])
# print(r.headers['CONNECTION'])
# print(r.headers['content-length'])
# print(r.headers['Content-Type'])
# print(r.headers['Date'])
# print(r.headers['server'])
# print(r.headers['via'])


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    animation = ""
    (user_message , animation) = main_function(user_message , animation)
    return json.dumps({"animation": animation, "msg":user_message})

@route("/test", method='POST')
def chat():
    reset_counter()
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
