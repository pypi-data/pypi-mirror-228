from . import Client
from .model.result import Result
from .model.task import Task


class Action:
    @staticmethod
    def status(client: Client, order_id: int, task_id: str) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/order_get_task_status_v1_orders__order_id__task__task_id__status__get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            task_id (str): Task identifier

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/task/{task_id}/status/')
        return Result[Task](**r)

    @staticmethod
    def run(client: Client, order_id: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/order_run_v1_orders__order_id__action_run__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/run/')
        return Result[Task](**r)

    @staticmethod
    def stop(client: Client, order_id: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/order_stop_v1_orders__order_id__action_stop__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/stop/')
        return Result[Task](**r)

    @staticmethod
    def cancel(client: Client, order_id: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/order_cancel_v1_orders__order_id__action_cancel__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/cancel/')
        return Result[Task](**r)

    @staticmethod
    def change_online_value(client: Client, order_id: int, value: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/order_change_online_v1_orders__order_id__action_change_online__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): New value

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/change/online/{value}/')
        return Result[Task](**r)

    @staticmethod
    def change_increase_value(client: Client, order_id: int, value: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/change_increase_value_v1_orders__order_id__action_increase_change__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): New value

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/increase/change/{value}/')
        return Result[Task](**r)

    @staticmethod
    def increase_on(client: Client, order_id: int, value: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/increase_on_v1_orders__order_id__action_increase_on__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): New value

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/increase/on/{value}/')
        return Result[Task](**r)

    @staticmethod
    def increase_off(client: Client, order_id: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/increase_off_v1_orders__order_id__action_increase_off__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/increase/off/')
        return Result[Task](**r)

    @staticmethod
    def add_views(client: Client, order_id: int, value: int) -> Result[Task]:
        """
        See: https://api.reyden-x.com/docs#/default/add_views_v1_orders__order_id__action_add_views__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): The number of views to add to the order

        Returns:
            Result[Task]: Result object
        """
        r = client.patch(f'/orders/{order_id}/action/add/views/{value}/')
        return Result[Task](**r)
