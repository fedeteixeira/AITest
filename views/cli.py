from pydantic_ai import AgentRunResult

from controllers.sql_agent import AgentOutput, SQLAgent, SqlAgentDependencies


class CLI:
    def __init__(self, sql_agent_dependencies: SqlAgentDependencies, sql_agent: SQLAgent):
        self.__sql_agent_dependencies = sql_agent_dependencies
        self.__sql_agent = sql_agent

    async def main(self):
        message_history = None
        allowed_exit_keywords = ["exit", "quit", "break"]
        try:
            print("Hi, I'm your SQL manager! What do you want to do? (Ctrl+C to exit)")
            while True:
                query = input("Query > ")
                if query in allowed_exit_keywords:
                    raise KeyboardInterrupt
                result: AgentRunResult[AgentOutput] = await self.__sql_agent.run_query(query=query, sql_agent_dependencies=self.__sql_agent_dependencies, message_history=message_history)
                message_history = result.all_messages()
                print(result.output.response_message)
        except (KeyboardInterrupt, EOFError):
            print("Program terminated by user.")