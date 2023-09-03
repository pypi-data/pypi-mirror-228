# forest-timer
A simple runtime visualization for nested for loops
```python
from forest_timer import ForestTimer as FT
ft = FT()
for i in ft(range(100), 'add name to loop'):
  for j in ft(range(100)): # or leave blank for the name of the iterable:
     ft.step((i, j))
```
