from pydantic_ai import AgentRunResult
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from aitest.controllers.sql_agent import AgentOutput, SQLAgent, SqlAgentDependencies


class CLI:
    def __init__(self, sql_agent_dependencies: SqlAgentDependencies, sql_agent: SQLAgent):
        self.__sql_agent_dependencies = sql_agent_dependencies
        self.__sql_agent = sql_agent
        self.__console = Console()

    async def main(self):
        message_history = None
        allowed_exit_keywords = ["exit", "quit", "break", "q"]
        try:
            self.__console.print(
                Panel.fit(
                    "Welcome to your AI SQL Manager!\nType your request or type [bold red]'exit'[/bold red] / press [bold red]Ctrl+C[/bold red] to quit.",
                    title="[bold cyan]🤖 SQL Agent CLI[/bold cyan]",
                    border_style="cyan",
                )
            )
            while True:
                query = self.__console.input("\n[bold green]Query > [/bold green]").strip()
                if not query:
                    continue
                if query.lower() in allowed_exit_keywords:
                    break

                result: AgentRunResult[AgentOutput] = await self.__sql_agent.run_query(
                    query=query,
                    sql_agent_dependencies=self.__sql_agent_dependencies,
                    message_history=message_history,
                )
                message_history = result.all_messages()
                self.__console.print()
                self.__console.print(Markdown(result.output.response_message))
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            self.__console.print("\n[bold yellow]👋 Program terminated by user. Goodbye![/bold yellow]")