from ariadne import make_executable_schema, gql, QueryType, ScalarType
from ariadne.asgi import GraphQL
from faker import Faker
import uuid
import re
import random
from mockapi.utils.logger import get_logger

fake = Faker()
logger = get_logger("graphql_handler")

any_scalar = ScalarType("Any")
@any_scalar.serializer
def serialize_any(value):
    return value

def get_faker_for_field(field_name: str, field_type: str):
    name_lower = field_name.lower()
    type_lower = field_type.lower().strip("![]")
    
    if type_lower == "id": return str(uuid.uuid4())
    if "email" in name_lower: return fake.email()
    if "name" in name_lower: return fake.name()
    if "city" in name_lower: return fake.city()
    if "country" in name_lower: return fake.country()
    if "date" in name_lower: return fake.iso8601()
    if type_lower == "string": return fake.word()
    if type_lower == "int": return fake.random_int()
    if type_lower == "float": return fake.pyfloat()
    if type_lower == "boolean": return fake.pybool()
    
    return f"mock_{field_name}"

def create_graphql_app(sdl: str) -> GraphQL:
    type_defs = gql(sdl)
    query = QueryType()
    
    type_resolvers = {}
    type_patterns = re.findall(r"type\s+(\w+)\s*{([^}]+)}", sdl, re.DOTALL)
    
    for type_name, type_body in type_patterns:
        if type_name in ["Query", "Mutation"]:
            continue
        field_resolvers = {}
        field_patterns = re.findall(r"(\w+)\s*:\s*([^(\s\n]+)", type_body)
        for field_name, field_type in field_patterns:
            # THE FIX: Correct resolver signature is (obj, info)
            field_resolvers[field_name] = lambda obj, info, _type=field_type, _name=field_name: get_faker_for_field(_name, _type)
        type_resolvers[type_name] = field_resolvers

    query_fields_match = re.search(r"type\s+Query\s*{([^}]+)}", sdl, re.DOTALL)
    if query_fields_match:
        query_body = query_fields_match.group(1)
        field_patterns = re.findall(r"(\w+)\s*:\s*([^(\s\n]+)", query_body)
        for field_name, return_type in field_patterns:
            clean_return_type = return_type.strip("[]!")
            
            # THE FIX: Correct resolver signature is (obj, info)
            def query_resolver(obj, info, _rt=clean_return_type, _fn=field_name, _full_rt=return_type):
                # If the return type is a custom object we have resolvers for
                if _rt in type_resolvers:
                    # Build a single mock object
                    mock_object = {f: r(obj, info) for f, r in type_resolvers[_rt].items()}
                    # If the schema expects a list, return a list of these objects
                    if '[' in _full_rt:
                        return [mock_object for _ in range(random.randint(2, 5))]
                    return mock_object
                
                # Otherwise, it's a scalar. Just generate a fake value for it.
                return get_faker_for_field(_fn, _full_rt)

            query.set_field(field_name, query_resolver)

    resolvers = [query]
    if "scalar Any" in sdl:
        resolvers.append(any_scalar)
        
    schema = make_executable_schema(type_defs, *resolvers)
    return GraphQL(schema, debug=True)