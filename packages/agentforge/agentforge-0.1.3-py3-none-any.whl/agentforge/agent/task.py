from .agent import Agent


class TaskCreationAgent(Agent):

    def load_data_from_memory(self):

        result_collection = self.storage.load_collection({
            'collection_name': "Results",
            'include': ["documents"]
        })

        try:
            result = result_collection[0] if result_collection else ["No results found"]
        except Exception as e:
            result = ["No results found"]

        task_collection = self.storage.load_collection({
            'collection_name': "Tasks",
            'include': ["documents"],
        })

        x = 0
        task_list = []
        for task in task_collection['documents']:
            task_list.append(f"{x+1}. {task_collection['documents'][x]}")
            x += 1
        # print(task_list)
        # task_list = [task['documents'] for task in task_collection]

        # task_list = task_collection if task_collection else []
        # task = task_list[0] if task_collection else None

        return {'result': result, 'task_list': task_list}

    def parse_result(self, result, **kwargs):
        new_tasks = result.split("\n")

        result = [{"Description": task_desc} for task_desc in new_tasks]
        filtered_results = [task for task in result if task['Description'] and task['Description'][0].isdigit()]

        try:
            order_tasks = [{
                'Order': int(task['Description'].split('. ', 1)[0]),
                'Description': task['Description'].split('. ', 1)[1]
            } for task in filtered_results]
        except Exception as e:
            raise ValueError(f"\n\nError ordering tasks. Error: {e}")

        return {"Tasks": order_tasks}

