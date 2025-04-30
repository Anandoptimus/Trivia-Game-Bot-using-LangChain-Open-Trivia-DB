import requests
import json
import random
import html
from langchain.agents import tool
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents import AgentExecutor

# === Tool Definition ===
@tool
def get_trivia_questions() -> str:
    """
    Fetches a single multiple-choice trivia question from the Open Trivia Database (OpenTDB) API, 
    randomizes the answer options, and returns the formatted question along with the correct answer 
    and labeled options.

    Returns:
    formatted (str): The trivia question with labeled answer choices (a, b, c, d).
    correct (str): The correct answer to the question.
    """

    Base_url = "https://opentdb.com/api.php?amount=3&category=17&difficulty=medium&type=multiple"
    response = requests.get(Base_url)
    if response.status_code != 200:
        raise Exception (f"invalid urll {response.status_code}")
    q = response.json()["results"][1]
    question = html.unescape(q["question"])
    correct_answer = q["correct_answer"]
    incorrect_answer = q["incorrect_answers"] 
    incorrect_answer.append(correct_answer)
    random.shuffle(incorrect_answer)
    labelled_options = { chr(97+label): option for label, option in enumerate(incorrect_answer)}
    formatted_ques = question + "\n"
    for label, opt in labelled_options.items():
        formatted_ques += f"{label}) {opt} \n"
    return f"{formatted_ques}\nCorrect Answer: {correct_answer}"


# === Tools and Function Bindings ===
functions = [format_tool_to_openai_function(get_trivia_questions)]
model = ChatOpenAI(model = "gpt-3.5-turbo").bind(functions = functions)
tool = [get_trivia_questions]

# === Prompt Template ===
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a friendly trivia game bot. Ask fun multiple-choice questions, wait for the user's answer, "
     "and then tell them if they are correct or not. If they ask to play again, fetch a new question. strictly check the answer should be like this pattern 'option) answer' got it"
     "Use simple and engaging language."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name= "agent_scratchpad")
    
])

# === Agent Chain Setup ===
observation = get_trivia_questions({})
chain = prompt | model | OpenAIFunctionsAgentOutputParser()
result1 = chain.invoke({
    "input": "let's play",
    "agent_scratchpad": format_to_openai_functions([(result, observation)])
})
# print(result1.return_values['output'])
agent_chain = RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
) | chain


# === Agent Executor ===
agent = AgentExecutor(agent = agent_chain, tools = tool, verbose = True) # still not add memory remind it 
agent.invoke({"input": "let's play"})
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a friendly trivia game bot. Ask fun multiple-choice questions, wait for the user's answer, "
     "and then tell them if they are correct or not. If they ask to play again, fetch a new question. strictly check the answer should be like this pattern 'option) answer' got it"
     "Use simple and engaging language."),
    MessagesPlaceholder(variable_name = "chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name= "agent_scratchpad")
    
])
agent_chain = RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
) | prompt | model | OpenAIFunctionsAgentOutputParser()


# === Memory ===
memory = ConversationBufferMemory(return_messages = True, memory_key = "chat_history")

agent = AgentExecutor(agent = agent_chain, tools = tool, verbose=False, memory=memory) #added memory

agent.invoke({"input": "let's play"})

agent.invoke({"input": "c) paris"})

agent.invoke({"input": "yes let's play"})

agent.invoke({"input": "b) Drag"})

agent.invoke({"input": "yes let's play"})

agent.invoke({"input": "i dont know"})



# === Output with memory ===
{'input': 'i dont know',
 'chat_history': [HumanMessage(content="let's play"),
  AIMessage(content='What is radiation measured in?\na) Watt\nb) Decibel\nc) Kelvin\nd) Gray  '),
  HumanMessage(content='d) Gray'),
  AIMessage(content='Correct! Gray is the unit of measurement for radiation. Would you like to play again?'),
  HumanMessage(content="let's play"),
  AIMessage(content='What is the capital of France?\na) London\nb) Berlin\nc) Paris\nd) Rome  '),
  HumanMessage(content='c) paris'),
  AIMessage(content='Correct! Paris is the capital of France. Would you like to play again?'),
  HumanMessage(content="yes let's play"),
  AIMessage(content='In aeronautics, flaps and slats are used to control what on an aircraft?\na) Weight\nb) Drag\nc) Thrust\nd) Lift  '),
  HumanMessage(content='b) Drag'),
  AIMessage(content='Incorrect. Flaps and slats are used to control lift on an aircraft. Would you like to try another question?'),
  HumanMessage(content="yes let's play"),
  AIMessage(content='What is the largest planet in our solar system?\na) Earth\nb) Mars\nc) Jupiter\nd) Venus  '),
  HumanMessage(content='i dont know'),
  AIMessage(content='No problem! The correct answer is c) Jupiter, which is the largest planet in our solar system. Would you like to play again?')],
 'output': 'No problem! The correct answer is c) Jupiter, which is the largest planet in our solar system. Would you like to play again?'}







