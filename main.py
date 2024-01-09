from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI, OpenAI
from flask import Flask, request, jsonify
from langchain.agents import load_tools
from langchain.tools import HumanInputRun
from dotenv import load_dotenv
from pathlib import Path
from dify import dify
import requests, logging, json, os


# Load configurations from .env file
load_dotenv()
project_folder = Path(os.getenv('PROJECT_FOLDER_PATH', '/default/path/to/working/directory'))
openai_api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom input function adapted for chat
def get_chat_input(user_message) -> str:
    return user_message

# Load tools with the human input function
llm = ChatOpenAI(temperature=0.0)
human_tool = HumanInputRun(input_func=get_chat_input)
tools = load_tools(["human", "llm-math"], llm=llm, input_func=get_chat_input)

# Initialize CrewAI agents
project_def_agent = Agent(
    role='Project Definition Specialist',
    goal="""To meticulously gather, organize, and structure user-provided project details,
    ensuring they are formatted for optimal processing by LLM, with the end goal of creating a fully functional CrewAI crew application.
    
    The project details should be organized as follows
    Project Name:
    Project Objective:
    Features(If Applicable):
    Technology Stack(If Applicable):
    Other information:
    """,
    backstory="""
    A proficient agent adept at dissecting and arranging complex project inputs into coherent, actionable formats.
    This agent serves as the foundation for the CrewAI crew, transforming initial ideas into structured project plans.""",
    verbose=True,
    llm='gpt-4',
    allow_delegation=False
)

agent_list_agent = Agent(
    role='Agent List Developer',
    goal="""
    To systematically evaluate the project specifications and curate a comprehensive list of necessary CrewAI agents,
    ensuring each aspect of the user's project is addressed in the creation of the CrewAI crew application.

    Agent properties are: role, goal, backstory, llm, verbose, allow_delegation, & tools.
    
    This is how an agent is structured:
    #example agent
    example_agent = Agent(
    role='Data Analyst',
    goal='Analyze data and provide insights',
    backstory='A skilled analyst with a keen eye for data trends and patterns.',
    llm='gpt-4',
    verbose=True,
    allow_delegation=True,
    tools=['DataProcessingTool', 'VisualizationTool']
    )
    """,
    backstory='An expert in agent role analysis, this agent plays a critical role in assembling the right mix of skills and functionalities required for the successful deployment of the CrewAI crew.',
    verbose=True,
    llm='gpt-4',
    allow_delegation=False
)

task_list_agent = Agent(
    role='Task List Organizer',
    goal="""
    To strategically break down the project into a series of well-defined sequentially organized tasks,
    each contributing effectively to the overarching goal of developing a complete CrewAI crew application.
        Task attributes are: description, agent, tools 

        Task structure is:

        #example task
        example_task = Task(
            description='this is an example of how a task should be structure",
            agent=example_agent,
            tools=['Langchain_Tool']
        )
        The tools that can be implemented are available here https://python.langchain.com/docs/integrations/tools/
    """,
    backstory="""
    A master of task organization, this agent is responsible for breaking down the project into a series of well-defined tasks,
    each contributing to the successful development of the CrewAI application.
    """,
    verbose=True,
    llm='gpt-4',
    allow_delegation=False
)
    backstory="""
    Known for its organizational acumen,
    this agent is adept at converting project goals into a structured series of tasks,
    facilitating the smooth progression of CrewAI application development.
    """,
    verbose=True,
    llm='gpt-4',
    allow_delegation=False
)

compiler_agent = Agent(
    role='CrewAI Compiler',
    goal="""
    To compile, configure, and package the CrewAI application into a user-friendly format, ready for deployment and use
    The structure of the application should be as follows:
    Project directory == Project Name
    PROJECT_DIRECTORY/main.py
    PROJECT_DIRECTORY/tasks.py
    PROJECT_DIRECTORY/agents/agents.py
    """,
    backstory='Specializing in the final assembly and verification of CrewAI applications, this agent ensures that all components are correctly integrated and packaged, delivering a complete and functional application to the user.',
    verbose=True,
    llm='gpt-4',
    allow_delegation=False
)

# Define CrewAI tasks
project_definition_task = Task(
    description="""
    Conduct a thorough analysis and structuring of user-inputted project details,
    categorizing information into Project Name, Objective, Features, Technology Stack,and other key aspects,
    to form the foundation of the CrewAI application then Pass this information to the next agent
    """,
    agent=project_def_agent,
    tools=["NLP_Parsing_Tool"]
)

agent_list_task = Task(
    description="""
    Develop a detailed JSON list of CrewAI agents in the appropriate format,
    considering the application's main goals, features, and technological requirements,
    to ensure comprehensive coverage of all project facets.

    Agent properties are: role, goal, backstory, llm, verbose, allow_delegation, & tools.
    
    This is how an agent is structured:
    
    #example agent
    example_agent = Agent(
    role='Example Role',
    goal='The goal should be to accomplish whatever task or expertise this agent is needed for',
    backstory='A skilled agent the extraordinary ability to handle the specific task(s) assigned to it',
    llm='gpt-4',
    verbose=True,
    allow_delegation=True,
    tools=['SomeLangChainTool', 'SomeOtherLangChainTool']

    The tools that can be implemented are available here https://python.langchain.com/docs/integrations/tools/

    Ensure agents.json file is user-approved before finalization.
    Complete your task, then pass the list of agents and the project info to the next agent.
    
    """,
    agent=agent_list_agent,
    tools=["Agent_Analysis_Tool"]
).",

task_list_task = Task(
    description="""
    Formulate and sequentially organize tasks essential for the CrewAI application's development,
    focusing on aligning each task with the application's primary goals and technical specifications.
    The tasks should be assigned to the agent that best fits the goal description of the task.

    Task attributes are: description, agent, tools 

    Task structure is:

    #example task
    example_task = Task(
        description='this is an example of how a task should be structured",
        agent=example_agent,
        tools=['Langchain_Tool']
    )
    The tools that can be implemented are available here https://python.langchain.com/docs/integrations/tools/.
    Ensure file is user-approved before finalization.
    Complete your task and pass the list of tasks, the list of agents, and the project info to the next agent.
    """,
    agent=task_list_agent,
    tools=["Task_Organization_Tool"]
)

compiler_task = Task(
    description="""Compile and organize the necessary files for the CrewAI crew application,
    including PROJECT_DIRECTORY/main.py, PROJECT_DIRECTORY/agents/agents.json, and PROJECT_DIRECTORY/tasks.py.
    Ensure each file is user-approved before finalization.
    Here are some examples of how main.py, tasks.py, and agents.json should look
    ### PROJECT_DIRECTORY/main.py ###
        # main.py
        import json
        from crewai import Agent, Task, Crew, Process

        # Function to initialize agents from a JSON file
        def initialize_agents_from_json(json_file):
            with open(json_file, 'r') as file:
                agents_data = json.load(file)
                return [Agent(**data) for data in agents_data]

        # Function to initialize tasks from a Python file
        def initialize_tasks_from_py(tasks_file):
            tasks_module = __import__(tasks_file.replace('.py', ''))
            return tasks_module.tasks

        # Initialize agents and tasks
        agents = initialize_agents_from_json('PROJECT_DIRECTORY/agents/agents.json')
        tasks = initialize_tasks_from_py('PROJECT_DIRECTORY/tasks')

        # Assemble the CrewAI crew with a sequential process
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential
        )

        # Kickoff the CrewAI crew to start processing tasks
        result = crew.kickoff()

        # Output the result
        print("CrewAI Crew Execution Result:", result)
    ### END PROJECT_DIRECTORY/main.py ###

    ### PROJECT_DIRECTORY/tasks.py ###
        # tasks.py
        from crewai import Task

        # Example Task 1
        example_task_1 = Task(
            description='Example description one showcasing a detailed task.',
            agent=example_agent_1,
            tools=['ExampleToolFromLangChain']
        )

        # Example Task 2
        example_task_2 = Task(
            description='Example description two showcasing another detailed task.',
            agent=example_agent_2,
            tools=['ExampleToolFromLangChain']
        )

        # Example Task 3
        example_task_3 = Task(
            description='Example description three showcasing yet another detailed task.',
            agent=example_agent_3,
            tools=['ExampleToolFromLangChain']
        )

        # Example Task 4
        example_task_4 = Task(
            description='Example description four showcasing a different kind of detailed task.',
            agent=example_agent_4,
            tools=['ExampleToolFromLangChain']
        )

        # List of tasks to be executed by the CrewAI crew
        tasks = [
            example_task_1,
            example_task_2,
            example_task_3,
            example_task_4
        ]
    ### END PROJECT_DIRECTORY/tasks.py ###

    ### PROJECT_DIRECTORY/agents/agents.json ###

            {
        "agents": [
            {
            "role": "Agent One",
            "goal": "Perform task one",
            "backstory": "Expert in task one with extensive experience and knowledge.",
            "llm": "gpt-4",
            "verbose": true,
            "allow_delegation": true,
            "tools": ["ToolA1", "ToolA2"]
            },
            {
            "role": "Agent Two",
            "goal": "Perform task two",
            "backstory": "Specialist in task two with a focus on efficiency and accuracy.",
            "llm": "gpt-4",
            "verbose": false,
            "allow_delegation": false,
            "tools": ["ToolB1", "ToolB2"]
            },
            {
            "role": "Agent Three",
            "goal": "Perform task three",
            "backstory": "Dedicated to task three with a track record of successful outcomes.",
            "llm": "gpt-4",
            "verbose": true,
            "allow_delegation": true,
            "tools": ["ToolC1", "ToolC2"]
            },
            {
            "role": "Agent Four",
            "goal": "Perform task four",
            "backstory": "Adept at task four with a focus on innovative solutions.",
            "llm": "gpt-4",
            "verbose": false,
            "allow_delegation": false,
            "tools": ["ToolD1", "ToolD2"]
            }
        ]
        }
    ### END PROJECT_DIRECTORY/agents/agents.json ###
    
    Conclude by packaging the files into a zipped format for user delivery upon final approval.

    """,
    agent=compiler_agent,
    tools=["File_Generation_Tool"]
)

# Assemble the CrewAI crew
crew = Crew(
    agents=[project_def_agent, agent_list_agent, task_list_agent, compiler_agent],
    tasks=[project_definition_task, agent_list_task, task_list_task, compiler_task],
    process=Process.sequential
)

# State management variables
current_stage = 'initial_prompt'  # Updated to start with the initial prompt
project_info = {}
agent_list = []
task_list = []

def send_message_to_dify(message, conversation_id):
    url = 'http://localhost:5001/api/chat-messages'  # Local Dify server endpoint
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'query': message,
        'conversation_id': conversation_id
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Flask endpoint to interact with CrewAI agents and Dify
@app.route('/chat-with-project', methods=['POST'])
def chat_with_project():
    global current_stage, project_info, agent_list, task_list

    try:
        data = request.json
        user_message = data.get('message')
        conversation_id = data.get('conversation_id', 'default-conversation-id')


        # Dynamically select the agent based on the current stage and pass the user message
        if current_stage == 'initial_prompt':
            response_message = project_def_agent.execute_task(
                task="Process initial user input.",
                context=user_message
            )
            current_stage = 'project_definition'  # Update the stage based on the agent's response
        elif current_stage == 'project_definition':
            project_info = json.loads(user_message)  # Assuming user message is in JSON format
            response_message = project_def_agent.execute_task(
                task="Define project details.",
                context=json.dumps(project_info)
            )
            current_stage = 'agent_list'
        elif current_stage == 'agent_list':
            response_message = agent_list_agent.execute_task(
                task="Generate agent list.",
                context=json.dumps(project_info)
            )
            agent_list = json.loads(response_message)  # Assuming the agent returns JSON formatted string
            current_stage = 'task_list'
        elif current_stage == 'task_list':
            response_message = task_list_agent.execute_task(
                task="Organize task list.",
                context=json.dumps(agent_list)
            )
            task_list = json.loads(response_message)
            current_stage = 'compiler'
        elif current_stage == 'compiler':
            compiled_files = compiler_agent.execute_task(
                task="Compile CrewAI configuration.",
                context=json.dumps({"agent_list": agent_list, "task_list": task_list, "project_folder": str(project_folder)})
            )
            response_message = compiled_files

        # Send response back to Dify
        dify_response = send_message_to_dify(response_message, conversation_id)
        if not dify_response or dify_response.get('status') != 'success':
            error_message = dify_response.get('error', 'Failed to send response to Dify')
            logger.error(error_message)
            return jsonify({"status": "error", "message": error_message})

    except Exception as e:
        logger.error(f"Error in chat_with_project endpoint: {e}")
        return jsonify({"status": "error", "message": str(e)})

    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True)