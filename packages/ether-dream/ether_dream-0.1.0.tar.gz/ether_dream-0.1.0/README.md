# Ether Dream for Python

Example:

```python
from ether_dream import ether_dream


class PointStream:
    def __iter__(self):
        return self

    def __next__(self):
        return (0, 0, 65535, 65535, 65535)


d = ether_dream.get_dac()
d.play_stream(iter(PointStream()))
```
