import requests
from urllib.parse import urljoin


class Client:
    def __init__(self, api_key: str):
        """
        Initializes a new Client instance for interacting with the BitSkins API.
        Docs: https://bitskins.com/docs/api/v2

        :param api_key: Bitskins api-key
        :type api_key: str
        """

        # REST api specifications
        self.BASE_URL = "https://api.bitskins.com"

        # Creating session
        self.session = requests.session()
        self.session.headers.update({
            "x-apikey": api_key
        })

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict | list:
        url = urljoin(self.BASE_URL, endpoint)
        response = self.session.request(method, url, json=data)
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def _get(self, endpoint: str) -> dict | list:
        return self._request("GET", endpoint)

    def _post(self, endpoint: str, data: dict = None) -> dict | list:
        return self._request("POST", endpoint, data=data)

    def get_current_session(self) -> dict:
        """
        Get current session information.
        Endpoint: "/account/profile/me"
        """
        return self._get("/account/profile/me")

    def get_account_balance(self) -> dict:
        """
        Get account balance.
        Endpoint: "/account/profile/balance"
        """
        return self._post("/account/profile/balance")

    def get_currency_rates(self) -> dict:
        """
        Get fiat and crypto rates on the platform. Fiat rates are used for provisional preview only. All
        in-platform transactions are calculated in USD. Crypto currencies are used as based rates for depositing and
        withdrawing.
        Endpoint: "/config/currency/list"
        """
        return self._get("/config/currency/list")

    def get_fee_plans(self) -> dict:
        """
        Get available sale fee plans.
        Endpoint: "/config/fee_plan/list"
        """
        return self._get("/config/fee_plan/list")

    def get_platform_status(self) -> dict:
        """
        Get platform status.
        Endpoint: "/config/status/get"
        """
        return self._get("/config/status/get")

    def get_sales(self, app_id: int, skin_id: int, limit: int = None) -> list:
        """
        Get latest sales for item.
        Endpoint: "/market/pricing/list"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param skin_id: Number identifying skin
        :type skin_id: int

        :param limit: Limits the returned results
        :type limit: int, optional
        """
        data = {"app_id": app_id, "skin_id": skin_id, "limit": limit}
        return self._post("/market/pricing/list", data=data)

    def get_pricing_summary(self, app_id: int, skin_id: int,
                            date_from: str = None, date_to: str = None) -> list:
        """
        Get sales stats for item, can be filtered by date.
        Endpoint: "/market/pricing/summary"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param skin_id: Number identifying skin
        :type skin_id: int

        :param date_from: From which date to calculate stats from
        :type date_from: str, optional

        :param date_to: To which date to calculate stats to
        :type: date_to: str, optional
        """
        data = {"app_id": app_id, "skin_id": skin_id}
        if date_from:
            data["date_from"] = date_from
        if date_to:
            data["date_to"] = date_to
        return self._post("/market/pricing/summary", data=data)

    def get_item_details(self, app_id: int, id: str = None, asset_id: str = None, hash: str = None) -> dict:
        """
        Get item details of single item.
        Endpoint: "/market/search/get"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param id: Id of item
        :type id: str

        :param asset_id: Asset id of item
        :type asset_id: str

        :param hash: Hash of item
        :type hash: str
        """
        data = {"app_id": app_id}
        if id:
            data["id"] = id
        if asset_id:
            data["asset_id"] = asset_id
        if hash:
            data["hash"] = hash
        return self._post("/market/search/get", data=data)

    def search_skin(self, where: dict, limit: int = None) -> list:
        """
        Search for item skins in game.
        Endpoint: "/market/search/skin_name"

        :param where: Filter dict with the optional keys: skin_name, id, paint_id, category_id, collection_id, type_id, app_id
        :type where: dict

        :param limit: Limits the returned results
        :type limit: int, optional
        """
        data = {"where": where, "limit": limit}
        if "skin_name" in where:
            where["skin_name"] = f"%{where['skin_name']}%"
        return self._post("/market/search/skin_name", data=data)

    def get_search_filters(self, app_id: int) -> dict:
        """
        Get available items filters for game.
        Endpoint: "/market/search/filters"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int
        """
        data = {"app_id": app_id}
        return self._post("/market/search/filters", data=data)

    def buy_single_item(self, app_id: int, id: str, max_price: float, hash: str = None) -> dict:
        """
        Purchases a single item.
        Endpoint: /market/buy/single

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param id: Id of item to purchase
        :type id: str

        :param max_price: Maximum price to pay for item
        :type max_price: float

        :param hash: Hash of item
        :type hash: str


        """
        data = {"app_id": app_id, "id": id, "max_price": max_price}
        if hash:
            data["hash"] = hash
        return self._post("/market/buy/single", data=data)

    def buy_multiple_items(self, app_id: int, items: list[dict]) -> dict:
        """
        Purchases multiple specified items.
        Endpoint: "/market/buy/many"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param items: List of dicts for each item to purchase. Ex: [{"id": "1", "max_price": 100}]
        :type items: list[dict]
        """
        data = {"app_id": app_id,  "items": items}
        return self._post("/market/buy/many", data=data)

    def buy_bulk_items(self, app_id: int, skin_id: int, max_price: float, quantity: int) -> dict:
        """
        Purchases an item in bulk with a specified max-price.
        Endpoint: "/market/buy/bulk"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param skin_id: Number identifying skin
        :type skin_id: int

        :param max_price: Maximum price to pay for item
        :type max_price: float

        :param quantity: Number of items to purchase
        :type quantity: int
        """
        data = {"app_id": app_id, "skin_id": skin_id,
                "max_price": max_price, "quantity": quantity}
        return self._post("/market/buy/bulk", data=data)

    def withdraw_single_item(self, app_id: int, id: str) -> dict:
        """
        Withdraw item from BitSkins inventory to your Steam account. Steam trade will be created.
        Endpoint: "/market/withdraw/single"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param id: Id of item to withdraw
        :type id: str
        """
        data = {"app_id": app_id, "id": id}
        return self._post("/market/withdraw/single", data=data)

    def withdraw_multiple_items(self, items: list[dict]) -> dict:
        """
        Withdraw multiple items from BitSkins inventory to your Steam account. Steam trades will be created.
        Endpoint: "/market/withdraw/many"

        :param items: List of dicts for each item to withdraw. Ex: [{"id": "1", "app_id": 730}]
        :type items: list[dict]
        """
        data = {"items": items}
        return self._post("/market/withdraw/many", data=data)

    def delist_single_item(self, app_id: int, id: str) -> dict:
        """
        Delist item from market. Item will be moved to BitSkins inventory.
        Endpoint: "/market/delist/single"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param id: Id of item to delist
        :type id: str
        """
        data = {"app_id": app_id, "id": id}
        return self._post("/market/delist/single", data=data)

    def delist_multiple_items(self, items: list[dict]) -> dict:
        """
        Delist multiple items from market. Items will be moved to BitSkins inventory.
        Endpoint: "/market/delist/many"

        :param items: List of dicts for each item to delist. Ex: [{"id": "1", "app_id": 730}]
        :type items: list[dict]
        """
        data = {"items": items}
        return self._post("/market/delist/many", data=data)

    def relist_single_item(self, app_id: int, id: str, price: float, type: int = 1) -> dict:
        """
        Relist single item from BitSkins inventory to market.
        Endpoint: "/market/relist/single"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param id: Id of item to relist
        :type id: str

        :param price: Price to relist item for
        :type price: float

        :param type: Type (1, 2 or 3) Default at 1.
        :type: int
        """
        data = {"app_id": app_id, "id": id, "price": price, "type": type}
        self._post("/market/relist/single", data=data)

    def relist_multiple_items(self, items: list[dict]) -> dict:
        """
        Relist multiple items from BitSkins inventory to market.
        Endpoint: /market/relist/many

        :param items: List of dicts for each item to relist. Ex: [{"id": "1", "app_id": 730, "type": 1, "price": 100}]
        :type items: list[dict]
        """
        data = {"items": items}
        return self._post("/market/relist/many", data=data)

    def update_single_item_price(self, app_id: int, id: str, price: float) -> dict:
        """
        Update single item price on market.
        Endpoint: "/market/update_price/single"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param id: Id of item to update price
        :type id: str

        :param price: Price to update to
        :type price: float
        """
        data = {"app_id": app_id, "id": id, "price": price}
        return self._post("/market/update_price/single", data=data)

    def update_multiple_items_price(self, items: list[dict]) -> dict:
        """
        Update multiple items on market.
        Endpoint: "/market/update_price/many"

        :param items: List of dicts for each item to update price of. Ex: [{"id": "1", "app_id": 730, "price": 100}]
        :type items: list[dict]
        """
        data = {"items": items}
        return self._post("/market/update_price/many", data=data)

    def get_items_history(self, type: str, limit: int = None, offset: int = None) -> dict:
        """
        Get history of bought and sold items.
        Endpoint: "/market/history/list"

        :param type: One of ["buyer", "seller"]
        :type type: str

        :param limit: Limits the returned results
        :type limit: int, optional

        :param offset: Offset of items to return
        :type offset: int, optional
        """
        data = {"type": type}
        if limit:
            data["limit"] = limit
        if offset:
            data["offset"] = offset
        return self._post("/market/history/list", data=data)

    def get_item_history(self, type: str, id: str) -> dict:
        """
        Get history of single bought or sold item.
        Endpoint: "/market/history/get"

        :param type: One of ["buyer", "seller"]
        :type type: str

        :param id: Id of bought or sold item
        :type id: str
        """
        data = {"type": type, "id": id}
        return self._post("/market/history/get", data=data)

    def bump_single_item(self, app_id: int, id: str) -> dict:
        """
        Bumps a single item.
        Endpoint: "/market/bump/single"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param id: Id of item to bump
        :type id: str
        """
        data = {"app_id": app_id, "id": id}
        return self._post("/market/bump/single", data=data)

    def get_bumped_items(self, app_id: int) -> dict:
        """
        Gets bumped items.
        Endpoint: "/market/bump/list"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int
        """
        data = {"app_id": app_id}
        return self._post("/market/bump/list", data=data)

    def buy_bumps_package(self, id: int) -> dict:
        """
        Purchases a bumps package.
        Endpoint: "/market/bump/buy_package"

        :param id: Id of package. One of [1, 2, 3, 4, 5, 6, 7, 8]
        :type: int
        """
        data = {"id": id}
        return self._post("/market/bump/buy_package", data=data)

    def get_all_items_list(self, app_id: int) -> list:
        """
        Get list of all skins for a specified app-id.
        Endpoint: /market/skin/app_id

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int
        """
        return self._get(f"/market/skin/{app_id}")

    def get_all_items_for_sale_list(self, app_id: int) -> dict:
        """
        Get list of all skins for a specified app-id.
        Endpoint: /market/insell/app_id

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int
        """
        return self._get(f"/market/insell/{app_id}")

    def get_steam_inventory(self, app_id: int) -> dict:
        """
        Get list of items in your Steam inventory.
        Endpoint: /steam/inventory/list

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int
        """
        data = {"app_id": app_id}
        return self._post("/steam/inventory/list", data=data)

    def deposit_steam_items(self, app_id: int, items: list[dict], type: int = 1) -> dict:
        """
        Deposit Steam item and list it on BitSkins market. Steam trade will be created.
        Endpoint: "/steam/deposit/many"

        :param app_id: Steam app-id. 730 for csgo, 570 for dota, 440 for tf2, 252490 for rust
        :type app_id: int

        :param items: List of dicts for each item to deposit. Ex: [{"asset_id": "11111", "price": 100}]
        :type items: list[dict]

        :param type: One of [1, 2, 3]. Default at 1.
        :type type: int
        """
        data = {"app_id": app_id, "items": items, "type": type}
        return self._post("/steam/deposit/many", data=data)
