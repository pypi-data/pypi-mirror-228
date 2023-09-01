from . import Client
from .model.user import User as UserModel, Balance


class User:
    @staticmethod
    def account(client: Client) -> UserModel:
        """
        Returns user account

        See: https://api.reyden-x.com/docs#/default/get_user_v1_user__get

        Parameters:
            client (Client): Instance of Client

        Returns:
            UserModel: UserModel object
        """
        r = client.get('/user/')
        return UserModel(**r)

    @staticmethod
    def balance(client: Client) -> Balance:
        """
        Returns user balance

        See: https://api.reyden-x.com/docs#/default/get_balance_v1_user_balance__get

        Parameters:
            client (Client): Instance of Client

        Returns:
            Balance: Balance object
        """
        r = client.get('/user/balance/')
        return Balance(**r)
