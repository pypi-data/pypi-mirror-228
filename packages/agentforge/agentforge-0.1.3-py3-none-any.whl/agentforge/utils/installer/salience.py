from agentforge.loops.action import Action
from agentforge.agent.execution import ExecutionAgent
from agentforge.agent.taskcreation import TaskCreationAgent
from agentforge.agent.status import StatusAgent
from agentforge.agent.summarization import SummarizationAgent
from agentforge.agent.actionselection import ActionSelectionAgent
from agentforge.agent.actionpriming import ActionPrimingAgent
from agentforge.logs.logger_config import Logger
from agentforge.utils.function_utils import Functions
from agentforge.utils.storage_interface import StorageInterface


class Salience:

    def __init__(self):
        # Summarize the Search Results
        self.summarization_agent = SummarizationAgent()
        self.action = Action()
        self.exec_agent = ExecutionAgent()
        self.task_creation_agent = TaskCreationAgent()
        self.status_agent = StatusAgent()
        self.action_agent = ActionSelectionAgent()
        self.priming_agent = ActionPrimingAgent()
        self.storage = StorageInterface().storage_utils
        self.logger = Logger(name="Salience")
        self.functions = Functions()
        self.frustration = 0
        self.frustration_step = 0.1
        self.max_frustration = 0.5

        # log_tasks = self.functions.show_task_list('Objectives')
        # filename = "./Logs/results.txt"
        # with open(filename, "a") as file:
        #     file.write(log_tasks)

    def run(self, context=None, feedback=None):

        self.logger.log(f"Running Agent...", 'info')
        # Load Last Results and Current Task as Data
        data = self.load_data_from_storage()

        # Feed Data to the Search Utility
        current_task = data['current_task']
        summary = self.summarization_agent.run(query=current_task['document'])

        if summary is not None:
            self.functions.print_result(result=summary, desc="Summary Agent results")


        task_result = self.exec_agent.run(summary=summary,
                                          context=context,
                                          feedback=feedback)

        execution_results = {"task_result": task_result,
                             "current_task": current_task,
                             "context": context,
                             "Order": data['Order']}

        self.logger.log(f"Execution Results: {execution_results}", 'debug')

        self.logger.log(f"Agent Done!", 'info')
        return execution_results

    # noinspection PyTypeChecker
    def frustrate(self):
        if self.frustration < self.max_frustration:
            self.frustration += self.frustration_step
            self.frustration = min(self.frustration, self.max_frustration)
            print(f"\nIncreased Frustration Level: {self.frustration}\n")
        else:
            print(f"\nMax Frustration Level Reached: {self.frustration}\n")

    def load_data_from_storage(self):
        result_collection = self.storage.load_collection({'collection_name': "Results", 'include': ["documents"]})

        if result_collection['documents']:
            result = result_collection['documents'][0]
        else:
            result = "No results found"

        task_collection = self.storage.load_collection({'collection_name': "Tasks",
                                                        'include': ["documents", "metadatas"]})

        # first, pair up 'ids', 'documents' and 'metadatas' for sorting
        paired_up_tasks = list(zip(task_collection['ids'], task_collection['documents'], task_collection['metadatas']))

        # sort the paired up tasks by 'Order' in 'metadatas'
        sorted_tasks = sorted(paired_up_tasks, key=lambda x: x[2]['Order'])

        # split the sorted tasks back into separate lists
        sorted_ids, sorted_documents, sorted_metadatas = zip(*sorted_tasks)

        # create the ordered results dictionary
        ordered_list = {'ids': list(sorted_ids),
                        'embeddings': task_collection['embeddings'],
                        'documents': list(sorted_documents),
                        'metadatas': list(sorted_metadatas)}

        self.logger.log(f"Ordered Task List:\n{ordered_list}", 'debug')

        current_task = None
        # iterate over sorted_metadatas
        for i, metadata in enumerate(sorted_metadatas):
            # check if the Task Status is not completed
            if metadata['Status'] == 'not completed':
                current_task = {'id': sorted_ids[i], 'document': sorted_documents[i], 'metadata': metadata}
                break  # break the loop as soon as we find the first not_completed task

        if current_task is None:
            self.logger.log("Task list has been completed!!!", 'info')
            quit()

        ordered_results = {
            'result': result,
            'current_task': current_task,
            'task_list': ordered_list,
            'task_ids': sorted_ids,
            'Order': current_task["metadata"]["Order"]
        }

        self.logger.log(f"Ordered Results:{ordered_results}", 'info')

        return ordered_results

    def loop(self):
        # Add a variable to set the mode

        goal = self.functions.prepare_objective()
        if goal is not None:
            self.task_creation_agent.run(goal=goal)

        status_results = None

        while True:
            self.functions.show_task_list('Salience')

            # Allow for feedback if auto mode is disabled
            status_result = self.functions.check_status(status_results)
            feedback = self.functions.check_auto_mode()
            data = self.run(context=status_result, feedback=feedback)

            self.logger.log(f"Data: {data}", 'debug')
            self.functions.print_result(data['task_result'], "Execution Results")

            status_results = self.status_agent.run(**data)
            data['status'] = status_results['status']
            data['reason'] = status_results['reason']

            result = f"Status: {data['status']}\n\nReason: {data['reason']}"
            self.functions.print_result(result, 'Status Agent')

            if data['status'] != 'completed':
                self.frustrate()
                self.action.run(data['reason'], frustration=self.frustration)
            else:
                self.frustration = 0


if __name__ == '__main__':
    Salience().loop()
