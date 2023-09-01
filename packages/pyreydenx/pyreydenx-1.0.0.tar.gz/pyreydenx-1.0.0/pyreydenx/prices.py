from . import Client
from .model.platform import Platform
from .model.price import Price
from .model.result import Result


class Prices:
    @staticmethod
    def get_prices(client: Client, platform: Platform) -> Result[Price]:
        """
        Returns all rates for a specific platform.

        See: https://api.reyden-x.com/docs#/default/prices_v1_prices__platform_code___get

        Parameters:
            client (Client): Instance of Client
            platform (Platform): twitch, youtube etc.

        Returns:
            Result[Price]: Result object
        """
        r = client.get(f'/prices/{platform.value}/')
        return Result[Price](**r)
