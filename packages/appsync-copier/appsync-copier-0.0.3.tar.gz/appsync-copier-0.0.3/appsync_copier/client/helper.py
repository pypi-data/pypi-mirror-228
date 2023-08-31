from typing import List


class QueryHelper:

    def model_to_create_appsync_mutation(modelName):
        mutation_name = f'create{modelName}'
        input_variable_name = 'input'

        return f'''
  mutation Create{modelName}(${input_variable_name}: Create{modelName}Input!) {{
    {mutation_name}({input_variable_name}: ${input_variable_name}) {{
      id
    }}
  }}
  '''

    def model_to_update_mutation(modelName):
        mutation_name = f'update{modelName}'
        input_variable_name = 'input'

        return f'''
  mutation Update{modelName}(${input_variable_name}: Update{modelName}Input!) {{
    {mutation_name}({input_variable_name}: ${input_variable_name}) {{
      id
    }}
  }}
  '''

    def model_to_list_query(modelName, attributes: List):
        formatted_attributes = '\n'.join(attributes)
        list_query = f'''
  query List{modelName}s {{
    list{modelName}s {{
      items {{
        {formatted_attributes}
      }}
    }}
  }}
  '''

    def model_to_list_query_with_filter(modelName, filter_by: str, filter_val: str,  attributes: List):
        formatted_attributes = '\n'.join(attributes)
        list_query = f'''
query MyQuery {{
  list{modelName}s(filter: {{{filter_by}: {{eq: "{filter_val}"}}}}) {{
    items {{
      {formatted_attributes}
    }}
  }}
}}

  '''

        return list_query

    def model_to_get_query(modelName, id, attributes: List):
        formatted_attributes = '\n'.join(attributes)
        return f'''
  query Get{modelName} {{
    get{modelName}(id: "{id}") {{
      {formatted_attributes}
    }}
  }}
  '''
