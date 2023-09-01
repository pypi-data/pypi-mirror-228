from dicts import Use
from devtools import debug

d = {
    'id': 1,
    'data': ''
}

with Use(d) as _:
    _.id = 2
    _.data = 'algo'
Use.set(d)
# print(f'\n{_}\n')
debug(_)
debug(d)
