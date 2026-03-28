from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    new_tasks = []

    @agent
    def software_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['software_architect'],
            verbose=True,
        )

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
#    @agent
#    def test_engineer(self) -> Agent:
#        return Agent(
#            config=self.agents_config['test_engineer'],
#            verbose=True,
#            allow_code_execution=True,
#            code_execution_mode="safe",  # Uses Docker for safety
#            max_execution_time=500, 
#            max_retry_limit=3 
#        )

    @tool("create crewai task")
    def create_crewai_task(self, description: str, expected_output: str, module_name: str) -> str:
        """create a crewai task """
        output_file = "output/" + module_name + ".py"
        task = Task(
            description=description,
            expected_output=expected_output,
            agent=self.backend_engineer,
            output_file=output_file
        )
        self.new_tasks.append(task)
        return "task created"

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def delegate_task(self) -> Task:
        return Task(
            config=self.tasks_config['delegate_task'],
            tools=[self.create_crewai_task]
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

#    @task
#    def test_task(self) -> Task:
#        return Task(
#            config=self.tasks_config['test_task'],
#        )   

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )