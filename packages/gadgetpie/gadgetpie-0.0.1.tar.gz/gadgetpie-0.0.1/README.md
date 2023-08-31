# Gadget
A wide variety of tools in the software development.

## 1 Gadget Abstract List

### 1.1 dict2class

Convert a parameter from "dict" type to simple User-defined class type.

Such as:
```python
# Import required packages
from gadget import Dict2Class
import datetime

# Defines a dictionary
test_dict = {
    'now': datetime.datetime.now(),
    'num': 77,
    'txt': 'Hello!',
    'dct': {
        't_num': 667,
        't_txt': 'hello!'
    },
    'lst': [1, 2, 3, 'abc'],
    'set': {1, 3, 3, 4, 'abc'},
    'tpl': (1, 2, 3, 5, 'abc')
}

# Converts to user-defined class here
ud_class = Dict2Class().convert(test_dict)
```



