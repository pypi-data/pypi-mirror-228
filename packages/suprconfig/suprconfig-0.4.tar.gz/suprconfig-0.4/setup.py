from setuptools import setup

setup(
    name = "suprconfig",
    version = "0.4",
    description = "This library created for comfortable using config",
    packages = ['suprconfig'],
    author_email="keneskay@vk.com",
    author = 'h99hood',
    zip_safe = False,
    long_description_content_type = "text/markdown",
    long_description = """
## Example: ##

### ENG:

```python
import suprconfig.config as config # import module

cfg = config.Config("config.json") # Creating an instance of a class

cfg.add(name = "app-name", value = "suprconfig") # Creating the "app-name" variable with the value "suprconfig" in the config.

cfg.add(name = "version", value = "v1.0") # Creating the "version" variable with the value "v1.0" in the config.

app_name = cfg.get('app-name') # Recording the value of the "app-name" variable from the config. (if no argument is specified, the function will return all variables and config values).
version = cfg.get('version') # Recording the value of the "version" variable from the config. (if no argument is specified, the function will return all variables and config values).

print(f"App Name: {app_name}\nVersion: {version}") # Information output to the terminal
```

### RUS:
```python
import suprconfig.config as config # Импорт модуля.

cfg = config.Config("config.json") # Создание экземпляра класса.

cfg.add(name = "app-name", value = "suprconfig") # Создание переменной "app-name" со значением "suprconfig" в конфиг.

cfg.add(name = "version", value = "v1.0") # Создание переменной "version" со значением "v1.0" в конфиг.

app_name = cfg.get('app-name') # Запись значение переменной "app-name" из конфига. (если аргумент не указан, функция вернет все переменные и значения конфига).
version = cfg.get('version') # Запись значение переменной "version" из конфига. (если аргумент не указан, функция вернет все переменные и значения конфига).

print(f"App Name: {app_name}\nVersion: {version}") # Вывод информации в терминал.
``` 
""")