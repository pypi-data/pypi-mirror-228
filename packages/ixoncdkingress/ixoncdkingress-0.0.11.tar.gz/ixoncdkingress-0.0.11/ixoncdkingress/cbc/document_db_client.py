"""
Module containing a client that is a abstraction of the MongoClient.
"""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

TIMEOUT: int = 30000

DocumentType = Dict[str, Any]


@dataclass(frozen=True)
class DocumentDBAuthentication:
    """
    Dataclass containing authentication values for the Document DB
    """

    username: str
    password: str


class DocumentDBClient:
    """
    Class for a document db client, this client connects with a document database.
    """

    _mongo_client: MongoClient[DocumentType]
    _database: str
    _collection: str
    _authentication: DocumentDBAuthentication

    def __init__(
        self,
        connection: str,
        database: str,
        collection: str,
        authentication: DocumentDBAuthentication,
        tls: bool = True
    ) -> None:
        """
        database: Company PublicId
        collection: CBC PublicId
        """

        self._database = database
        self._collection = collection
        self._authentication = authentication

        self._mongo_client = MongoClient(
            connection,
            username=self._authentication.username,
            password=self._authentication.password,
            timeoutMS=TIMEOUT,
            tls=tls
        )

    def insert_one(self, document: DocumentType) -> InsertOneResult:
        """
        Insert a single document.
        """
        return self._get_collection().insert_one(document)

    def insert_many(self, documents: Iterable[DocumentType]) -> InsertManyResult:
        """
        Insert an iterable of documents.
        """
        return self._get_collection().insert_many(documents)

    def update_one(self, filter_map: Mapping[str, Any], update: Mapping[str, Any]) -> UpdateResult:
        """
        Update a single document matching the filter.
        """
        return self._get_collection().update_one(filter_map, update)

    def update_many(self, filter_map: Mapping[str, Any], update: Mapping[str, Any]) -> UpdateResult:
        """
        Update one or more documents that match the filter.
        """
        return self._get_collection().update_many(filter_map, update)

    def delete_one(self, filter_map: Mapping[str, Any]) -> DeleteResult:
        """
        Delete a single document matching the filter.
        """
        return self._get_collection().delete_one(filter_map)

    def delete_many(self, filter_map: Mapping[str, Any]) -> DeleteResult:
        """
        Delete one or more documents matching the filter.
        """
        return self._get_collection().delete_many(filter_map)

    def find_one(
        self, *args: Any, filter_map: Optional[Any], **kwargs: Any
    ) -> Optional[DocumentType]:
        """
        Get a single document from the database.
        """
        return self._get_collection().find_one(filter_map, *args, **kwargs)

    def find(self, *args: Any, **kwargs: Any) -> Cursor[DocumentType]:
        """
        Query the database.
        """
        return self._get_collection().find(*args, **kwargs)

    def _get_collection(self, collection_name: Optional[str] = None) -> Collection[DocumentType]:
        return self._mongo_client.get_database(self._database).get_collection(
            collection_name or self._collection
        )

    def __repr__(self) -> str:
        return (
            '<DocumentDBClient'
            f' database={self._database},'
            f' collection={self._collection},'
            '>'
        )
