
# PyGptRes

`PyGptRes` is a Python module for interacting with OpenAI's GPT-3.5 Turbo API to create natural language conversations with cutting-edge language models.

## Usage

Here's how to use this module in your Python code:

```python
from pygpt import PyGpt

if  __name__  ==  "__main__":

pygpt =  PyGpt()
pygpt.login("ACCESS TOKEN")
pygpt.init()

pygpt.send("Hello?")
```

Be sure to initialize your `PyGptRes` instance by first calling the `login` method with your access token and then calling `init` to configure the necessary URL and headers.

## Example Usage

Here's a simple example of using `PyGptRes` to send a message to the GPT-3.5 Turbo API:

```python
# Initialize PyGptRes
pygpt = PyGptRes()
pygpt.login("YOUR_ACCESS_TOKEN")
pygpt.init()
```

# Send a message to the API
```python
response = pygpt.send("Hello, how are you?")
```

# Process the API response
```python
print(response)` 
```

Make sure to replace `"YOUR_ACCESS_TOKEN"` with your actual access token.

## License

This project is licensed under the MIT License.