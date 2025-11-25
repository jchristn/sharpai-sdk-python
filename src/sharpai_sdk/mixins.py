import json
from typing import List, Optional, Type

from pydantic import BaseModel

from .configuration import get_client
from .models.enumeration_query import EnumerationQueryModel
from .models.enumeration_result import EnumerationResultModel
from .utils.url_helper import _get_url_v1, _get_url_v2

JSON_CONTENT_TYPE = {"Content-Type": "application/json"}


class ExistsAPIResource:
    """
    Mixin class for checking if a resource exists.
    If the resource exists, the method returns `True`, otherwise it returns `False`.
    """

    RESOURCE_NAME: str = ""

    @classmethod
    def exists(cls, guid: str) -> bool:
        client = get_client()
        url = _get_url_v1(cls, guid)

        try:
            client.request("HEAD", url)
            return True
        except Exception:
            return False


class CreateableAPIResource:
    """
    A mixin class for creating resources.
    This class implements a generic creation pattern for resources using Pydantic models
    for data validation and serialization.
    """

    MODEL: Optional[Type[BaseModel]] = None
    RESOURCE_NAME: str = ""
    CREATE_METHOD: str = "PUT"

    @classmethod
    def create(cls, **kwargs) -> "BaseModel":
        """
        Creates a new resource.

        Args:
            **kwargs: Keyword arguments for the request, including the resource data.
                - headers (dict, optional): Additional headers for the request.
                - _data (dict, optional): The data to be sent in the request body.

        Returns:
            BaseModel: The created resource, validated against the MODEL if defined.
        """
        client = get_client()
        headers = kwargs.pop("headers", {})

        # Extract data from kwargs
        _data = kwargs.pop("_data", kwargs.copy())

        # Build URL
        url = _get_url_v1(cls)
        if cls.MODEL is not None:
            data = cls.MODEL(**_data).model_dump(
                mode="json", by_alias=True, exclude_unset=True
            )
        else:
            data = _data

        # Make request and validate response
        instance = client.request(cls.CREATE_METHOD, url, json=data, headers=headers)
        return cls.MODEL.model_validate(instance) if cls.MODEL else instance


class CreateableMultipleAPIResource:
    """
    A mixin class for creating multiple resources at once.
    This class implements a generic creation pattern for multiple resources using Pydantic models
    for data validation and serialization.
    """

    MODEL: Optional[Type[BaseModel]] = None
    RESOURCE_NAME: str = ""

    @classmethod
    def create_multiple(cls, data: List[dict]) -> List[BaseModel]:
        """
        Creates multiple nodes or edges in a single request.
        """
        if data is None:
            raise TypeError("Nodes parameter cannot be None")

        if not data:
            return []

        client = get_client()

        # Validate and serialize each node if MODEL is provided
        if cls.MODEL is not None:
            validated_nodes = [
                cls.MODEL(**node).model_dump(mode="json", by_alias=True)
                for node in data
            ]
        else:
            validated_nodes = data

        # Construct URL for multiple creation
        url = _get_url_v1(cls, "bulk")

        # Make the request
        instances = client.request("PUT", url, json=validated_nodes)

        # Validate response data if MODEL is provided
        if cls.MODEL is not None:
            return [cls.MODEL.model_validate(instance) for instance in instances]
        return instances


class RetrievableAPIResource:
    """
    A mixin class for retrieving resources.
    This class implements a generic retrieval pattern for resources using Pydantic models
    (for data validation and deserialization).
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None

    @classmethod
    def retrieve(cls, guid: str, **kwargs) -> "BaseModel":
        """
        Retrieve a specific instance of the resource by its ID.
        """
        client = get_client()
        include = {}
        if kwargs.get("include_data"):
            include["incldata"] = None
        if kwargs.get("include_subordinates"):
            include["inclsub"] = None

        url = _get_url_v1(cls, guid, **include)
        instance = client.request("GET", url)

        return cls.MODEL.model_validate(instance) if cls.MODEL else instance


class UpdatableAPIResource:
    """
    A mixin class for updating resources.
    This class implements a generic update pattern for resources using Pydantic models(for data validation and serialization).
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None

    @classmethod
    def update(cls, guid: str, **kwargs) -> "BaseModel":
        """
        Update a specific instance of the resource by its ID.
        """
        client = get_client()
        url = _get_url_v1(cls, guid)

        if cls.MODEL is not None:
            # For updates, we only send the fields that are provided
            # We don't validate against the full model since updates are partial
            data = kwargs
        else:
            data = kwargs
        instance = client.request("PUT", url, json=data)

        return cls.MODEL.model_validate(instance) if cls.MODEL else instance


class DeletableAPIResource:
    """
    A mixin class for deleting resources.
    This class implements a generic delete pattern for resources for a specific resource.
    """

    RESOURCE_NAME: str = ""

    @classmethod
    def delete(cls, guid: str, **kwargs) -> None:
        """
        Delete a resource by its ID.
        """
        client = get_client()
        url = _get_url_v1(cls, guid, **kwargs)

        client.request("DELETE", url)


class AllRetrievableAPIResource:
    """
    A mixin class for retrieving all resources of a given type.
    This class implements a generic retrieval pattern for resources using Pydantic models(for data validation and deserialization).
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Optional[Type[BaseModel]]] = None

    @classmethod
    def retrieve_all(cls, **kwargs) -> list["BaseModel"]:
        """
        Retrieve all instances of the resource.
        """
        client = get_client()
        include = {}
        if kwargs.get("include_data"):
            include["incldata"] = None
        if kwargs.get("include_subordinates"):
            include["inclsub"] = None

        url = _get_url_v1(cls, **include)
        instances = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(instance) for instance in instances]
            if cls.MODEL
            else instances
        )


class SearchableAPIResource:
    """
    Provides a search method to search for resources based on criteria.
    This class implements a flexible search pattern against resources
    using request/response models for validation and serialization.
    """

    RESOURCE_NAME: str = ""
    SEARCH_MODELS: Optional[
        tuple[Optional[type[BaseModel]], Optional[type[BaseModel]]]
    ] = None

    @classmethod
    def search(cls, **data) -> BaseModel:
        """
        Search for resources based on the provided criteria.
        """
        client = get_client()
        if data.get("include_data"):
            data["IncludeData"] = True
        if data.get("include_subordinates"):
            data["IncludeSubordinates"] = True

        url = _get_url_v1(cls, "search")
        result_model = cls.SEARCH_MODELS[1]

        instance = client.request(
            "POST", url, data=json.dumps(data).encode(), headers=JSON_CONTENT_TYPE
        )
        return result_model(**instance)


class EnumerableAPIResource:
    """Mixin class for enumerating API resources."""

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None

    @classmethod
    def enumerate(cls, **kwargs) -> "EnumerationResultModel":
        """
        Enumerates resources of a given type.

        Returns:
            EnumerationResultModel: The enumeration results containing the list of resources
                and any pagination metadata.
        """
        client = get_client()

        if kwargs.pop("include_data", False):
            kwargs["incldata"] = None
        if kwargs.pop("include_subordinates", False):
            kwargs["inclsub"] = None

        url = _get_url_v2(cls, **kwargs)

        response = client.request("GET", url)
        return (
            EnumerationResultModel[cls.MODEL].model_validate(response)
            if cls.MODEL
            else response
        )


class EnumerableAPIResourceWithData:
    """Mixin class for enumerating API resources with data using V1 URL helper."""

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None
    ENUMERABLE_REQUEST_MODEL: Type[BaseModel] = EnumerationQueryModel

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> "EnumerationResultModel":
        """
        Enumerates resources of a given type with data using a query model.

        This method supports advanced querying capabilities through the ENUMERABLE_REQUEST_MODEL,
        which defaults to EnumerationQueryModel.

        Args:
            **kwargs: Query parameters that conform to the ENUMERABLE_REQUEST_MODEL schema.
                These parameters will be validated against the model before making the request.

        Returns:
            EnumerationResultModel: The enumeration results containing the list of resources
                and any pagination metadata.

        Raises:
            ValidationError: If the provided query parameters don't match the ENUMERABLE_REQUEST_MODEL schema.
        """
        client = get_client()

        data_dict = kwargs.pop(
            "_data", kwargs.copy()
        )  # Get 'data' if provided, else use kwargs

        if data_dict.pop("include_data", False):
            data_dict["IncludeData"] = True
        if data_dict.pop("include_subordinates", False):
            data_dict["IncludeSubordinates"] = True

        url = _get_url_v2(cls, **kwargs)

        data = cls.ENUMERABLE_REQUEST_MODEL(**data_dict).model_dump(
            mode="json", by_alias=True, exclude_unset=True
        )

        response = client.request("POST", url, json=data)
        return (
            EnumerationResultModel[cls.MODEL].model_validate(response)
            if cls.MODEL
            else response
        )
