# **Ellar - ASGI Python Framework**
<p align="center">
  <a href="#" target="blank"><img src="img/EllarLogoB.png" width="200" alt="Ellar Logo" /></a>
</p>

<p align="center"> Ellar - Python ASGI web framework for building fast, efficient and scalable RESTAPIs and server-side application. </p>

![Test](https://github.com/eadwinCode/ellar/actions/workflows/test_full.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/eadwinCode/ellar)
[![PyPI version](https://badge.fury.io/py/ellar.svg)](https://badge.fury.io/py/ellar)
[![PyPI version](https://img.shields.io/pypi/v/ellar.svg)](https://pypi.python.org/pypi/ellar)
[![PyPI version](https://img.shields.io/pypi/pyversions/ellar.svg)](https://pypi.python.org/pypi/ellar)

---
## **Introduction**
Ellar is a lightweight ASGI framework for building efficient and scalable server-side python applications.
It supports both OOP (Object-Oriented Programming) and FP (Functional Programming)

Ellar is also a higher level of abstraction of [Starlette (ASGI toolkit)](https://www.starlette.io/){target="_blank"}, a lightweight ASGI framework/toolkit well-suited for developing asynchronous web services in Python.

## **Inspiration**
Ellar was deeply influenced by [NestJS](https://docs.nestjs.com/){target="_blank"} for its ease of use, project structures and patterns that aids in building small or complex project applications.
Also, Ellar took some concepts from [FastAPI](https://fastapi.tiangolo.com/){target="_blank"} in terms of request parameter handling and data serialization with Pydantic. 

The objective of Ellar is to provide a high level of abstracted interface to the web, along with a well-structured project setup, give room for object-oriented approach to web application design, 
allow you chose your desired application architecture, and ultimately, deliver speedy handling to requests.


## **Features Summary**

- **Easy to Use**: Ellar has a simple and intuitive API that makes it easy to get started with building a fast and scalable web applications or web APIs with Python.
- **Dependency Injection (DI)**: It comes with DI system makes it easy to manage dependencies and reduce coupling between components.
- **Pydantic Integration**: It is properly integrated with Pydantic, a popular Python library for data validation, to ensure that input data is valid.
- **Templating with Jinja2**: Ellar provides built-in support for Jinja2 templates, making it easy to create dynamic web pages.
- **OpenAPI Documentation**: It comes with built-in support for OpenAPI documentation, making it easy to generate `Swagger` or `ReDoc` documentation for your API. And more can be added with ease if necessary.
- **Controller (MVC) Architecture**: Ellar's controller architecture follows the Model-View-Controller (MVC) pattern, making it easy to organize your code.
- **Guards for Authentication and Authorization**: It provides built-in support for guards, allowing you to easily implement authentication and authorization in your application.
- **Modularity**: Ellar follows a modular architecture inspired by NestJS, making it easy to organize your code into reusable modules.
- **Asynchronous programming**: It allows you to takes advantage of Python's `async/await` feature to write efficient and fast code that can handle large numbers of concurrent requests

## **Installation**
To get started, you need to scaffold a project using [Ellar-CLI](https://eadwincode.github.io/ellar-cli/){target="_blank"} toolkit. This is recommended for a first-time user.
The scaffolded project is more like a guide to project setup.

```shell
$(venv) pip install ellar
```

After that, lets create a new project. 
Run the command below and change the `project-name` with whatever name you decide.
```shell
$(venv) ellar new project-name
```

then, start the app with:
```shell
$(venv) ellar runserver --reload
```

Open your browser and navigate to [`http://localhost:8000/`](http://localhost:8000/){target="_blank"}.
![Swagger UI](img/ellar_framework.png)

## **Dependency Summary**
- `Python >= 3.7`
- `Starlette`
- `Pydantic`
- `Injector`

## **Status**

Project is still in development

- Documentation - in progress
- Database Plugin with [Encode/ORM](https://github.com/encode/orm){target="_blank"}
