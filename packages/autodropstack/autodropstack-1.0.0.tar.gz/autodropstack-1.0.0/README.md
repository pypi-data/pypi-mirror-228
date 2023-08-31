# AutoDropStack

Simple first in last out stack data structure

```bash
pip install autodropstack
```

```python
from autodropstack import AutoDropStack

stack = AutoDropStack(3)
stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)
stack.push(5)
assert stack.stack == [3, 4, 5]
```

## License
[MIT](./LICENSE)

## Author
[thearyadev](https://github.com/thearyadev/autodropstack)
