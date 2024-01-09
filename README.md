
# CrewAI Flask Project

This project integrates CrewAI with a Flask web application to handle tasks sequentially in a chat-based environment. It showcases the use of CrewAI agents for processing tasks and managing state in a dynamic conversation flow.

I plan on making this more modular and complex soon. Will be splitting the agents and tasks into separate files.

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- Flask
- CrewAI
- Dify https://docs.dify.ai/getting-started/install-self-hosted
- An OpenAI API key

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository-url.git
   cd your-repository-directory
   ```

2. **Create and Activate a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install flask crewai langchain requests python-dotenv

   Dify can be installed following their docs.
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root directory and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   PROJECT_FOLDER_PATH=your_project_folder_path_here
   ```

5. **Run the Flask Application**:
   ```bash
   python app.py  # Replace `app.py` with your main Python script name
   ```

## Usage

The Flask application will start and listen for incoming chat messages. Interact with the application through the defined endpoints to see how CrewAI agents process tasks and handle chat-based interactions.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
