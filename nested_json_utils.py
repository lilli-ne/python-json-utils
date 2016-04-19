"""
Util functions for handling and traversing
nested json.
"""

def is_number(this):
    """
    Check if the parameter can be cast to number
    """
    try:
        int(this)
        return True
    except ValueError:
        return False


def get_json_path_element(thisjson, path):
    """
    j is the json, path is a list
    e.g. j = {"cats":[{"name":"Tiffany"},{"name":"Snowball"}]}
    path = ['cats',0,'name']
    or path = 'cats,0,name'
    will give "Tiffany"
    if path doesn't lead anywhere, empty string is returned
    """
    if not isinstance(path, list):
        path = path.split(',')
    tmp = thisjson
    try:
        for i in path:
            if is_number(i):
                tmp = tmp[int(i)]
            else:
                tmp = tmp[i]
        return tmp
    except KeyError:
        return ''


def extract_keys(thisjson):
    """
    Extracts all keys from a json with nested structures.
    E.g. running this function for the following json
    thisjson = {
        "key":"value",
        "dict":{
            "nested":"value"
        },
        "plainlist":[
            "value1",
            "value2"
        ],
        "nestedlist": [
            {
                "object":"value"
            },
            "value3"
        ]
    }

    will give ['object', 'nested', 'plainlist', 'key']
    """
    attributes = []
    for key in thisjson.keys():
        val = thisjson[key]
        if isinstance(val, dict):
            attributes.extend(extract_keys(val))
        elif isinstance(val, list):
            has_dict = False
            for item in val:
                if isinstance(item, dict):
                    has_dict = True
                    attributes.extend(extract_keys(item))
            if not has_dict:
                attributes.append(key)
        else:
            attributes.append(key)
    return attributes

#pylint: disable=dangerous-default-value
def extract_paths(thisjson, parent=[]):
    """
    Extracts all paths from a json with nested structures.
    You can use the resulting paths with get_json_path_element(j, path)
    to get all values from a nested json structure.
    E.g. running this function for the following json
    thisjson = {
        "key":"value",
        "dict":{
            "nested":"value"
        },
        "plainlist":[
            "value1",
            "value2"
        ],
        "nestedlist": [
            {
                "object":"value"
            },
            "value3"
        ]
    }

    will give ['nestedlist,0,object', 'dict,nested', 'plainlist', 'key']
    """
    attributes = []
    for key in thisjson.keys():
        val = thisjson[key]
        if isinstance(val, dict):
            attributes.extend(extract_paths(val, parent=parent+[key]))
        elif isinstance(val, list):
            has_dict = False
            for i, item in enumerate(val):
                if isinstance(item, dict):
                    has_dict = True
                    attributes.extend(extract_paths(item, parent=parent+[key, str(i)]))
            if not has_dict:
                if parent:
                    attributes.append(','.join(parent)+','+key)
                else:
                    attributes.append(key)
        else:
            if parent:
                attributes.append(','.join(parent)+','+key)
            else:
                attributes.append(key)
    return attributes


