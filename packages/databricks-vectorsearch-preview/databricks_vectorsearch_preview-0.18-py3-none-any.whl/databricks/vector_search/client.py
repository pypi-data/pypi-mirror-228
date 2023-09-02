import json
import logging
from typing import Dict, List, Optional

import requests
from mlflow.utils import databricks_utils


class VectorSearchClient:
    """
    Client for interacting with the Vector Search API for Databricks.

    Example usage:

        client = VectorSearchClient()
        response = client.create_catalog("my_catalog")
        print(response)
    """

    def __init__(self, workspace_url=None, token=None):
        """
        Initializes a VectorSearchClient instance.

        :param workspace_url: Workspace URL of Databricks
        :param token: Token for authentication.
        """
        self._workspace_url = workspace_url
        if self._workspace_url is None:
            host_creds = databricks_utils.get_databricks_host_creds()
            self._workspace_url = host_creds.host

        self._token = token
        if self._token is None:
            host_creds = databricks_utils.get_databricks_host_creds()
            self._token = host_creds.token

    def _call_endpoint(self, endpoint, method, params=None, json=None):
        headers = dict()
        headers["Authorization"] = f"Bearer {self._token}"
        cleaned_hostname = (
            self._workspace_url[:-1]
            if self._workspace_url.endswith("/")
            else self._workspace_url
        )
        url = f"{cleaned_hostname}{endpoint}"
        response = requests.request(
            url=url, headers=headers, method=method, params=params, json=json
        )
        try:
            return response.json()
        except Exception as e:
            logging.warn(f"Error processing request {e}")
            return {
                "response": response.text,
                "error": str(e),
                "status_code": response.status_code
            }

    """
        This method will create an vector search catalog in UC
        catalog will take 10 to 15 mins to get provisioned.
        Before that any operation on the cluster will fail except get_cluster
        catalog_name is the vector search catalog name to be created
    """

    def create_catalog(self, catalog_name):
        """
        Creates a Vector Search catalog.

        :param catalog_name: The name of the vector search catalog to be created.

        :return: The response from the API call.
        """
        json_data = {"name": catalog_name}
        return self._call_endpoint(
            "/api/2.0/vector-search/catalog",
            "POST",
            json=json_data,
        )

    # This method will delete the vector search catalog in UC
    # catalog_name is the vector search catalog name to be deleted
    def delete_catalog(self, catalog_name):
        """
        Deletes the specified Vector Search catalog.

        :param catalog_name: The name of the vector search catalog to be deleted.

        :return: The response from the API call.
        """
        # TODO: do we need to check if catalog already exists
        return self._call_endpoint(
            f"/api/2.0/vector-search/catalog/{catalog_name}", "DELETE"
        )

    # This method will get the vector search catalog in UC
    # catalog_name is the vector search catalog name
    def get_catalog(self, catalog_name):
        """
        Retrieves the specified Vector Search catalog.

        :param catalog_name: The name of the catalog to be retrieved.

        :return: The response from the API call.
        """
        return self._call_endpoint(
            f"/api/2.0/vector-search/catalog/{catalog_name}", "GET"
        )

    # Ingestion time can vary a lot depending on a few important factors, like: embedding model, document length, number of docs, etc
    # source_table_name is the offline Delta table name, must be a UC table and in the format of <catalog>.<schema>.<table>
    # dest_index_name is the index name to be created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    # primary_key the single primary key of the column
    # index_column indicates the column that will do the embedding
    def create_index(
        self,
        source_table_name,
        dest_index_name,
        primary_key,
        index_column,
        embedding_model_endpoint_name=None,
        embedding_dimension=None
    ):
        """
        Creates an index

        :param source_table_name: The source delta table where the pre-chunked document texts are located. Must be an Unity Catalog table in the form of <catalog>.<schema>.<table>
        :param dest_index_name: The name of the index to be created under the online catalog. must be in the format of <catalog>.<schema>.<table>
        :param primary_key: Column that represents a non-nullable unqiue identifier of the documents to be stored in the index.
        :param index_column: Column that will be embedded as vectors and persisted in the index
        :param embedding_model_endpoint_name: Embedding model endpoint to use

        :return: The response from the API call.

        Example usage:

        client = VectorSearchClient()
        response = client.create_index(
            source_table_name="my_catalog.schema1.table1",
            dest_index_name="vector.schema1.table1_index",
            primary_key="doc_id",
            index_column="text",
            embedding_model_endpoint_name="e5-large-v2")
        print(response)
        """
        vector_index_def = {"column": index_column}
        if embedding_model_endpoint_name:
            vector_index_def["embedding_model_endpoint_name"] = embedding_model_endpoint_name
        if embedding_dimension:
            vector_index_def["embedding_model_dimension"] = embedding_dimension
        json_data = {
            "index_pipeline_spec": {
                "continuous": {},
                "src_table": source_table_name,
                "dest_index": dest_index_name,
                "primary_key": primary_key,
                "vector_index": vector_index_def
            }
        }

        return self._call_endpoint(
            "/api/2.0/vector-search/index", "POST", json=json_data
        )

    # This method will get the index definition
    # index_name is the index name created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    def get_index(self, index_name):
        """
        Retrieves the specified index.

        :param index_name: The name of the index.

        :return: The response from the API call.
        """
        return self._call_endpoint(f"/api/2.0/vector-search/index/{index_name}", "GET")

    # This method will perform a vector similarity search on an index
    # index_name is the index name created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    # query_text is the query text
    # columns are the returned search results
    # filter is a json object to filter the search results
    # num_results is the number of documents to be returned
    def similarity_search(
        self,
        index_name: str,
        columns: List[str],
        query_text: Optional[str] = None,
        filter: Optional[Dict] = None,
        num_results: int = 5,
        debug_level: int = 1,
        query_vector: Optional[List[float]] = None,
    ):
        """
        Performs a vector similarity search on the specified index.

        :param index_name: The name of the index.
        :param query_text: The query text for the search.
        :param columns: The columns to be returned in the search results.
        :param filter: The JSON object of filters for the search (optional).
        :param num_results: The number of documents to be returned (optional).
        :param query_vector: Query vector for search.

        :return: The response from the API call.

        Example usage:

        client = VectorSearchClient()
        response = client.similarity_search(
            index_name="vector.schema1.table1_index",
            query_text="What is spark connect?",
            columns=["text", "source"],
            filter={"id NOT": ("10", "1")},
            num_results=3)
        print(response)
        """
        json_data = {
            "num_results": num_results,
            "columns": columns,
            "filters_json": json.dumps(filter) if filter else None,
            "debug_level": debug_level,
        }
        if query_text:
            json_data["query"] = query_text
            json_data["query_text"] = query_text
        if query_vector:
            json_data["query_vector"] = query_vector

        return self._call_endpoint(
            f"/api/2.0/vector-search/index/{index_name}/query",
            "GET",
            json=json_data,
        )

    # index_name is the index name created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    def delete_index(self, index_name):
        """
        Deletes the specified index in the Vector Search cluster.

        :param index_name: The name of the index to be deleted.

        :return: The response from the API call.
        """
        return self._call_endpoint(
            f"/api/2.0/vector-search/index/{index_name}", "DELETE"
        )

    # This method will list all the existing indexes created under the catalog
    # catalog_name is the vector search catalog name
    def list_indexes(self, catalog_name):
        """
        Lists all existing indexes created under the specified catalog.

        :param catalog_name: The name of the catalog.

        :return: The response from the API call.
        """
        json_data = {"catalog_name": catalog_name}
        return self._call_endpoint(
            "/api/2.0/vector-search/index", "GET", json=json_data
        )