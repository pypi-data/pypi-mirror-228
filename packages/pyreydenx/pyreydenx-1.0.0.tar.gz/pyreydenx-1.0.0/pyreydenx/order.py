from typing import List, Optional, Union

from . import Client
from .model.date_qty import DateQty
from .model.id_qty import IdQty
from .model.new_order_parameters import TwitchOrder, YouTubeOrder
from .model.online_stat import OnlineStat
from .model.order import Order as OrderModel
from .model.payment import Payment
from .model.result import Result
from .model.site_stat import SiteStat
from .model.task import Task


class Order:
    @staticmethod
    def get_orders(client: Client, cursor: Optional[str] = None) -> Result[List[OrderModel]]:
        """
        Returns list of orders

        See: https://api.reyden-x.com/docs#/default/orders_v1_orders__get

        Parameters:
            client (Client): Instance of Client
            cursor (str): Optional parameter which allows to get next part of objects if exists.

        Returns:
            Result[List[OrderModel]]: Result object
        """
        if not cursor:
            r = client.get(f'/orders/')
        else:
            r = client.get(f'/orders/?cursor={cursor}')
        return Result[List[OrderModel]](**r)

    @staticmethod
    def details(client: Client, order_id: int) -> Result[OrderModel]:
        """
        Order details

        See: https://api.reyden-x.com/docs#/default/order_details_v1_orders__order_id___get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[OrderModel]: Result object
        """
        r = client.get(f'/orders/{order_id}/')
        return Result[OrderModel](**r)

    @staticmethod
    def payments(client: Client, order_id: int, cursor: Optional[str] = None) -> Result[List[Payment]]:
        """
        Returns list of payments for order

        See: https://api.reyden-x.com/docs#/default/order_payments_v1_orders__order_id__payments__get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            cursor (str): Optional parameter which allows to get next part of objects if exists.

        Returns:
            Result[List[Payment]]: Result object
        """
        if not cursor:
            r = client.get(f'/orders/{order_id}/payments/')
        else:
            r = client.get(f'/orders/{order_id}/payments/?cursor={cursor}')
        return Result[List[Payment]](**r)

    @staticmethod
    def online_stats(client: Client, order_id: int) -> Result[List[OnlineStat]]:
        """
        Detailed information about users online

        See: https://api.reyden-x.com/docs#/default/order_stats_online_v1_orders__order_id__statistics_online__get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[List[OnlineStat]]: Result object
        """
        r = client.get(f'/orders/{order_id}/statistics/online/')
        return Result[List[OnlineStat]](**r)

    @staticmethod
    def clicks_stats(client: Client, order_id: int) -> Result[List[DateQty]]:
        """
        Detailed information about clicks

        See: https://api.reyden-x.com/docs#/default/order_stats_clicks_v1_orders__order_id__statistics_clicks__get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[List[DateQty]]: Result object
        """
        r = client.get(f'/orders/{order_id}/statistics/clicks/')
        return Result[List[DateQty]](**r)

    @staticmethod
    def views_stats(client: Client, order_id: int) -> Result[List[DateQty]]:
        """
        Detailed information about views

        See: https://api.reyden-x.com/docs#/default/order_stats_views_v1_orders__order_id__statistics_views__get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[List[DateQty]]: Result object
        """
        r = client.get(f'/orders/{order_id}/statistics/views/')
        return Result[List[DateQty]](**r)

    @staticmethod
    def sites_stats(client: Client, order_id: int) -> Result[List[SiteStat]]:
        """
        Detailed information about sites

        See: https://api.reyden-x.com/docs#/default/order_stats_sites_v1_orders__order_id__statistics_sites__get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            Result[List[SiteStat]]: Result object
        """
        r = client.get(f'/orders/{order_id}/statistics/sites/')
        return Result[List[SiteStat]](**r)

    @staticmethod
    def multiple_views_stats(client: Client, identifiers: List[int]) -> Result[List[IdQty]]:
        """
        View statistics for multiple orders

        See: https://api.reyden-x.com/docs#/default/multiple_views_v1_orders_multiple_views__post

        Parameters:
            client (Client): Instance of Client
            identifiers (List[int]): Identifiers

        Returns:
            Result[List[IdQty]]: Result object
        """
        r = client.post(f'/orders/multiple/views/', {'identifiers': identifiers[:100]})
        return Result[List[IdQty]](**r)

    @staticmethod
    def multiple_clicks_stats(client: Client, identifiers: List[int]) -> Result[List[IdQty]]:
        """
        Click-through statistics for multiple orders

        See: https://api.reyden-x.com/docs#/default/multiple_clicks_v1_orders_multiple_clicks__post

        Parameters:
            client (Client): Instance of Client
            identifiers (List[int]): Identifiers

        Returns:
            Result[List[IdQty]]: Result object
        """
        r = client.post(f'/orders/multiple/clicks/', {'identifiers': identifiers[:100]})
        return Result[List[IdQty]](**r)

    @staticmethod
    def create(client: Client, parameters: Union[TwitchOrder, YouTubeOrder]) -> Result[Task]:
        """
        Create new order for Twitch or YouTube stream

        See: https://api.reyden-x.com/docs#/default/twitch_stream_v1_orders_create_twitch_stream__post
        See: https://api.reyden-x.com/docs#/default/youtube_stream_v1_orders_create_youtube_stream__post

        Parameters:
            client (Client): Instance of Client
            parameters (NewOrderParameters): TwitchOrder or YouTubeOrder object

        Returns:
            Result[Task]: Result object
        """
        r = client.post(f'/orders/create/{parameters.platform}/stream/', parameters.dict())
        return Result[Task](**r)
