import json

def json_to_class(obj, data):
    # If input is a JSON string, parse it
    if isinstance(data, str):
        data = json.loads(data)
    
    for key, value in data.items():
        # Recursively convert nested dictionaries into class attributes
        if isinstance(value, dict):
            # If the attribute already exists and is a class, update it
            current_attr = getattr(obj, key, None)
            if current_attr and hasattr(current_attr, '__dict__'):
                json_to_class(current_attr, value)
            else:
                # Otherwise, create a new object to hold nested attributes
                nested_obj = type('DynamicObject', (), {})()
                json_to_class(nested_obj, value)
                value = nested_obj
        setattr(obj, key, value)
    
    return obj

def json_default_only(json):
    # Look for attribute with default and set with the default value
    return {
        k: (v["default"] if isinstance(v, dict) and "default" in v else v)
        for k, v in json.items()
    }