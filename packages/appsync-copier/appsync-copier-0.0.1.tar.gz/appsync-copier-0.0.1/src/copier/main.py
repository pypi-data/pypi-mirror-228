from ..schema import Schema
from ..client import QueryHelper, AppSyncClient
from ..example import *
import json


class AppSyncCopier:

    def __init__(self,
                 schema_path: str,
                 client: AppSyncClient,
                 testing: bool = False
                 ) -> None:
        self.schema = Schema(schema_path)
        self.client = client
        self.testing = testing

    def recursive_copier(self, parent_name: str, parent_id: str, new_parent_id: str = None):

        model = None

        parent_attributes = self.schema.get_model_attributes(parent_name)
        model_get_query = QueryHelper.model_to_get_query(
            parent_name, parent_id, parent_attributes)
        model = self.client.run_query(model_get_query)
        model = model['data'][f'get{parent_name}']
        model['__typename'] = parent_name

        if model is None:
            return

        children = self.schema.get_child_models(parent_name)

        if new_parent_id is None:
            parent_creation = run_mutation(parent_name, model.copy())
            new_parent_id = parent_creation['id']

        for child_name, attribute_name in children.items():
            reference_parent = attribute_name + 'ID'

            attributes = self.schema.get_model_attributes(child_name)
            query = QueryHelper.model_to_list_query_with_filter(
                child_name,
                reference_parent,
                parent_id,
                attributes
            )

            data = self.client.run_query(query)

            if data is None or data['data'] is None:
                print(child_name)
                print(query)
                print(data)
                exit()
            data = data['data'][f'list{child_name}s']['items']
            data_list = data

            for item in data_list:
                item[reference_parent] = new_parent_id
                child_creation = run_mutation(child_name, item.copy())
                self.recursive_copier(
                    child_name, item['id'], child_creation['id'])

    def copy_model(self, parent_name: str, parent_id: str, new_parent_id: str = None):
        self.recursive_copier(parent_name, parent_id, new_parent_id)
        open('database.json', 'w').write(
            json.dumps(new_database, indent=2))
