# Jinx: Python Web Framework built to learn how to create a framework

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)
![PyPI](https://img.shields.io/pypi/v/jinx-web.svg)

Jinx (**Jinj**a - htm**x**) Web is a Python Web Framework, built to learn how frameworks work, and to experiment a bit with WSGI servers. Also, I'll probably be trying htmx to power the client side


## Installation
```shell
pip install jinx-web
```

## Basic usage
```python
from jinx import Jinx

app = Jinx()

@app.route("/user/{name}", allowed_methods=["get"])
def user_name(request, response, name):
    response.text = f"Hello, {name}"
```
