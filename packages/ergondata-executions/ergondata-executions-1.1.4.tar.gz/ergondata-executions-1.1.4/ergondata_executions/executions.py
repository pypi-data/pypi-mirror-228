import requests
from typing_extensions import NotRequired, TypedDict
from ergondata_executions.pandas_formatter import format_db_table, format_process_table, format_tasks_table, format_queues_table, format_tasks_executions_table, format_queue_items


class AuthToken(TypedDict):
    token: str


class ExecutionToken(TypedDict):
    token: str


class Response(TypedDict):
    status: str
    message: str
    reason: NotRequired[str]
    data: NotRequired[object]


class ExecutionsController:

    __ROOT_URL = "http://ergondata-django-api.us-east-1.elasticbeanstalk.com/api/"
    # __ROOT_URL = "http://127.0.0.1:8000/api/"
    __AUTH_URL = "auth"
    __GET_DBS_URL = "get/databases"
    __GET_PROCESSES_URL = "get/tenants"
    __GET_TASKS_URL = "get/processes"
    __GET_QUEUES_URL = "executions/get/queues"
    __CREATE_EXECUTION_URL = "executions/create/execution"
    __UPDATE_EXECUTION_URL = "executions/update/execution"
    __CREATE_QUEUE_ITEM_URL = "executions/create/queue-item"
    __UPDATE_QUEUE_ITEM_URL = "executions/update/queue-item"
    __GET_QUEUE_ITEM_URL = "executions/get/queue-item"
    __GET_QUEUE_SIZE_URL = "executions/get/queue-size"
    __GET_QUEUE_ITEMS_URL = "executions/get/queue-items"
    __GET_EXECUTIONS_URL = "executions/get/executions"
    __WRITE_LOG_URL = "executions/create/log"


    __execution_id = None

    def __init__(self, username: str, password: str, timeout: int = 50) -> None:

        self.username = username
        self.password = password
        self.timeout = timeout

        self.__auth_token: AuthToken = ExecutionsController.__authenticate(
            self=self
        )
        self.__execution_token: ExecutionToken = ""

    def __authenticate(self) -> AuthToken:

        body = {
            "username": self.username,
            "password": self.password
        }

        try:
            response = requests.post(
                url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__AUTH_URL }",
                json=body,
                timeout=self.timeout
            ).json()
            return response["token"]
        except BaseException:
            raise Exception

    def get_dbs(self, json: bool = True):

        print(f"Obtaining dbs")
        headers = {"Authorization": f"Bearer {self.__auth_token}"}

        response = requests.get(
            url=f"{ExecutionsController.__ROOT_URL}{ExecutionsController.__GET_DBS_URL}",
            headers=headers,
            timeout=self.timeout
        )

        if not (response.status_code == 200):
            return

        print("Obtained dbs with success")

        if json:
            return response.json()["data"]
        else:
            return format_db_table(response.json()["data"])

    def get_processes(self, json: bool = True):

        print(f"Obtaining processes")
        headers = {"Authorization": f"Bearer {self.__auth_token}"}

        response = requests.get(
            url=f"{ExecutionsController.__ROOT_URL}{ExecutionsController.__GET_PROCESSES_URL}",
            headers=headers,
            timeout=self.timeout
        )

        if not (response.status_code == 200):
            return

        if json:
            return response.json()['data']

        return format_process_table(response.json()['data'])


    def get_tasks(self, json: bool = True) -> Response:

        print(f"Obtaining tasks")
        headers = {"Authorization": f"Bearer {self.__auth_token}"}

        response = requests.get(
            url=f"{ExecutionsController.__ROOT_URL}{ExecutionsController.__GET_TASKS_URL}",
            headers=headers,
            timeout=self.timeout
        )

        if not (response.status_code == 200):
            return

        if json:
            return response.json()['data']

        return format_tasks_table(response.json()['data'])

    def create_execution(self) -> Response:

        print("Creating execution")
        headers = {
            "Authorization": f"{ self.__auth_token }"
        }

        response = requests.post(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__CREATE_EXECUTION_URL }",
            headers=headers,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Execution created with success")
            self.__execution_token = response.json()["token"]
            self.__execution_id = response.json()['execution_id']
        else:
            print("Failed to create execution")

        return response.json()

    def update_execution(self, status: str, custom_exception_id: str = None) -> Response:

        print("Updating execution")
        headers = {
            "Authorization": f"{ self.__execution_token }"
        }
        body = {
            "type": "default",
            "status": status,
            "custom_exception_id": custom_exception_id
        }

        response = requests.post(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__UPDATE_EXECUTION_URL }",
            json=body,
            headers=headers,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Execution updated with success")
        else:
            print("Failed to updated execution")

        return response.json()

    def reset_executions(self) -> Response:

        print("Resetting executions")
        headers = {"Authorization": f"Bearer { self.__auth_token }"}
        body = {"type": "clear"}

        response = requests.post(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__UPDATE_EXECUTION_URL }",
            json=body,
            headers=headers,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Executions reset with success")
        else:
            print("Failed to reset executions")

        return response.json()

    def create_queue_item(self, item_id: str, item: object, queue_id: str = None) -> Response:

        print(f"Creating queue item id: { item_id }")
        headers = {"Authorization": f"Bearer { self.__execution_token }"}
        body = {
            "id": item_id,
            "item": item,
            "queue_id": queue_id
        }

        response = requests.post(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__CREATE_QUEUE_ITEM_URL }",
            json=body,
            headers=headers,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Queue item created with success")
        else:
            print("Failed to create queue item")

        return response.json()

    def update_queue_item(self, item_id: str, item_status: str, status_message: str = None, custom_exception_id: str = None) -> Response:

        print(f"Updating queue item id: { item_id }")
        headers = {"Authorization": f"Bearer { self.__execution_token }"}
        body = {
            "type": "default",
            "id": item_id,
            "status": item_status,
            "status_message": status_message,
            "custom_exception_id": custom_exception_id
        }

        response = requests.post(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__UPDATE_QUEUE_ITEM_URL }",
            json=body,
            headers=headers,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Queue item updated with success")
        else:
            print("Failed to update queue item")

        return response.json()

    def get_queue_item(self, queue_id: str) -> Response:

        print(f"Obtaining next queue item")
        headers = {"Authorization": f"Bearer { self.__execution_token }"}
        body = {
            "queue_id": queue_id
        }

        response = requests.get(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__GET_QUEUE_ITEM_URL }",
            headers=headers,
            json=body,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Queue item obtained with success")
        else:
            print("Failed to obtain queue item")

        return response.json()

    def reset_queue_item(self) -> Response:

        print(f"Resetting queue item")
        headers = {"Authorization": f"Bearer { self.__execution_token }"}
        body = {"type": "clear"}

        response = requests.post(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__UPDATE_QUEUE_ITEM_URL }",
            headers=headers,
            json=body,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Queue item reset with success")
        else:
            print("Failed to reset queue item")

        return response.json()

    def write_log(self, log_type: str, message: str, step: str, error: str = None) -> Response:

        print(f"Writting log")
        headers = {"Authorization": f"Bearer { self.__execution_token }"}

        body = {
            "type": log_type,
            "message": message,
            "step": step,
            "error": error
        }

        response = requests.post(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__WRITE_LOG_URL }",
            headers=headers,
            json=body,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Log written with success")
        else:
            print("Failed to write log")

        return response.json()


    def get_queues(self, json: bool = True) -> Response:

        print(f"Obtaining queues")
        headers = {"Authorization": f"Bearer { self.__auth_token }"}
        body = {}

        response = requests.get(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__GET_QUEUES_URL }",
            headers=headers,
            json=body,
            timeout=self.timeout
        )

        if not (response.status_code == 200):
            return

        if json:
            return response.json()["data"]

        return format_queues_table(response.json()["data"])

    def get_queue_size(self, queue_id) -> Response:

        print(f"Obtaining next queue item")
        headers = {"Authorization": f"Bearer { self.__execution_token }"}
        body = {}

        response = requests.get(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__GET_QUEUE_SIZE_URL }/{queue_id}",
            headers=headers,
            json=body,
            timeout=self.timeout
        )

        if response.status_code == 200:
            print("Queue item obtained with success")
        else:
            print("Failed to obtain queue item")

        return response.json()

    def get_queue_items(self, queue_id: str, days_behind: int = 0, json: bool = False) -> Response:

        print(f"Obtaining queue items")
        headers = {"Authorization": f"Bearer { self.__auth_token }"}

        body = {
            "queue_id": queue_id,
            "days_behind": days_behind
        }

        response = requests.get(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__GET_QUEUE_ITEMS_URL }",
            headers=headers,
            json=body,
            timeout=self.timeout
        )

        if not (response.status_code == 200):
            return

        if json:
            return response.json()["data"]

        return format_queue_items(response.json()["data"])



    def get_executions(self, json: bool = True):

        print(f"Obtaining executions")
        headers = {"Authorization": f"Bearer { self.__auth_token }"}
        body = {}

        response = requests.get(
            url=f"{ ExecutionsController.__ROOT_URL }{ ExecutionsController.__GET_EXECUTIONS_URL }",
            headers=headers,
            json=body,
            timeout=self.timeout
        )

        if not(response.status_code == 200):
            return

        if json:
            return response.json()["data"]

        return format_tasks_executions_table(response.json()["data"])

    def get_execution_id(self):
        return self.__execution_id

