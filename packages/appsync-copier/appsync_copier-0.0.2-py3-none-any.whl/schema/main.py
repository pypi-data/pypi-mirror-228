import re


class Schema:

    def __init__(self, file_name: str = 'schema.graphql') -> None:
        with open(file_name, 'r') as file:
            self.schema_content = file.read()

    def get_child_models(self, model_name):
        target_type = f': {model_name}'
        pattern = r'\b' + re.escape(target_type) + r'\b'
        matches = re.finditer(pattern, self.schema_content)
        referencing_models = []

        for match in matches:
            type_definition = re.findall(
                r'type\s+(\w+)\s*{', self.schema_content[:match.start()])
            if type_definition:
                referencing_models.append(type_definition[-1])

        attribute_references = {}

        for referencing_model in referencing_models:
            pattern = rf'({referencing_model})\s*{{([\s\S]*?)}}'
            match = re.search(pattern, self.schema_content)
            if match:
                attribute = re.search(
                    r'(\w+)\s*:\s*' + model_name, match.group(2))
                if attribute:
                    attribute_references[referencing_model] = attribute.group(
                        1)

        return (attribute_references)

    def get_model_attributes(self, model_name):
        pattern = rf'{model_name}\s*{{([\s\S]*?)}}'
        match = re.search(pattern, self.schema_content)
        if match:
            attributes = re.findall(
                r'(\w+)\s*:\s*(ID|String|Int|Float)', match.group(1))

            attributes = [x[0] for x in attributes]
            return attributes

        return []
