
# CrewAI Flask Project

This project integrates CrewAI with a Flask web application to handle tasks sequentially in a chat-based environment. It showcases the use of CrewAI agents for processing tasks and managing state in a dynamic conversation flow.

I plan on making this more modular and complex soon. Will be splitting the agents and tasks into separate files.

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- Flask
- CrewAI
- Dify
- An OpenAI API key

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/JimJim12/CrewBuilder.git
   cd CrewBuilder
   ```

2. **Create and Activate a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate

   On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install flask crewai langchain requests python-dotenv

   ```   

4.   **Dify can be installed as a local server following their docs**:
      ```bash
   https://docs.dify.ai/getting-started/install-self-hosted

   One of the dependencies might be broken depending on your environment. trio broke so i had to fix it by editing /lib/python3.10/site-packages/trio/_core/_io_epoll.p

   in _io_epoll.p change the import from 'import select' to 'from select import epoll', then change line 187-199

   FROM

   @attr.s(slots=True, eq=False, hash=False)
   class EpollIOManager:
      _epoll = attr.ib(factory=select.epoll)
      # {fd: EpollWaiters}
      _registered = attr.ib(
         factory=lambda: defaultdict(EpollWaiters), type=Dict[int, EpollWaiters]
      )
      _force_wakeup = attr.ib(factory=WakeupSocketpair)
      _force_wakeup_fd = attr.ib(default=None)

      def __attrs_post_init__(self):
         self._epoll.register(self._force_wakeup.wakeup_sock, select.EPOLLIN)
         self._force_wakeup_fd = self._force_wakeup.wakeup_sock.fileno()


   TO 

   @attr.s(slots=True, eq=False, hash=False)
   class EpollIOManager:
      if hasattr(select, 'epoll'):
         _epoll = attr.ib(factory=select.epoll)
         _force_wakeup: WakeupSocketpair = attr.ib(factory=WakeupSocketpair)
         _force_wakeup_fd: int | None = attr.ib(default=None)

         def __attrs_post_init__(self) -> None:
               self._epoll.register(self._force_wakeup.wakeup_sock, select.EPOLLIN)
               self._force_wakeup_fd = self._force_wakeup.wakeup_sock.fileno()
      else:
         _epoll = attr.ib(default=None)
         _registered: defaultdict[int, EpollWaiters] = attr.ib(
         factory=lambda: defaultdict(EpollWaiters)
      )
      _force_wakeup: WakeupSocketpair = attr.ib(factory=WakeupSocketpair)
      _force_wakeup_fd: int | None = attr.ib(default=None)

      def __attrs_post_init__(self) -> None:
         raise NotImplementedError("Epoll is not available on this platform")

   Now you can run the DB import from Dify docs         
   ```

5. **Set Up Environment Variables**:
   Create a `.env` file in the project root directory and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   PROJECT_FOLDER_PATH=/your/project/folder/path/here
   ```

6. **Run the Flask Application**:
   ```bash
   python main.py
   ```

## Usage

The Flask application will start and listen for incoming chat messages. Interact with the application through the defined endpoints to see how CrewAI agents process tasks and handle chat-based interactions.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

