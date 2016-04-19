Json utils
===========

This repository contains python modules for handling json in various situations. 
For me the use cases have been e.g. processing web data (datalayers, snowplow events and such). 

If you need to go through all the elements in a nested json, you can find them by using the extract_keys or extract_paths.
extract_paths is useful when used together with get_json_path_element, which picks the value from a nested json, given the path to the specific element. 

See docstrings in code for more details. 