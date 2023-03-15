# Latext

[![justforfunnoreally.dev badge](https://img.shields.io/badge/justforfunnoreally-dev-9ff)](https://justforfunnoreally.dev)

Natural language -> latex. That's basically what this thing does.
This is just another [just for fun](https://justforfunnoreally.dev/) project for learning openai library and basic prompt engineering.

### Example

```python
from latext import Latext

l = Latext()

l("5/sqrt(x+3) = z")
print(l.get_answer())
```

```bash
Estimated cost: 7.28 IDR
Estimated tokens: 235
Actual cost: 7.93 IDR
Actual tokens: 256
\frac{5}{\sqrt{x+3}} = z
```

### Limitation

1. If you are using jupyter notebooks, you'll need to delete the extra "\\". This happens due to python escape character on "\\"
2. USD to IDR conversion is hardcoded because it's not the main concern
