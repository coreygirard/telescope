# telescope

## What

**Telescope** is a library for creating virtual object hierarchies to simplify user interaction. What does this actually mean? I wrote it to aid in crafting elegant interfaces to codebases that are three things:
- Inner mechanics aren't well-matched to our cognitive model of the concepts involved (examples: Matplotlib, LIFX API)
- Impossible to refactor (perhaps because it's third-party, perhaps because structure is dictated by computational efficiency requirements)
- Unreasonable to hand-craft a solution, often because it would require passing around internal state in an unwieldy and/or computationally expensive fashion

How does **Telescope** help? It allows the user to follow a tree of objects defined via a Domain-Specific Language in a separate YML file, and then calls a `.handle()` function at the root object with three things:

- the virtual path followed
- any arguments used
- any keyword arguments used

For a concrete example, imagine executing this line:

`example.aaa.bbb.ccc('test-arg', kwarg='hello')`

Assuming this was a valid path specified in the YML file, `example.handle()` would be called with three arguments:

- `.aaa.bbb.ccc()`
- `('test-arg', )`
- `{'kwarg': 'hello'}`

`example.handle()` then returns some value, which is passed back and returned to whatever made that call in the first place. The entire process is as seamless as though `example.aaa.bbb.ccc()` actually existed.



### Hello World

`example.yml`
```yml
example
    .hello
        .world()
```

`example.py`
```python
from telescope import Telescope, fuse

class Example(Telescope('example.yml','example')):
    def __init__(self):
        # init stuff

    def handle(self, route, *args, **kwargs):
        return route

example = Example()
print(example.hello.world())
```
```
.hello.world()
```


## YML format

The roots of the file can be used as templates elsewhere in the file or can be imported into a `Telescope()` class to define structure. For example:

`sample.yml`
```yml
ccc
    ddd()

aaa
   bbb
   {ccc}
```

If we create an object named `sample` based on the `aaa` root, the following will be valid paths:

```python
sample.bbb
sample.ddd()
```

Note that `sample.ccc` is not a valid path. The text of the roots within the YML file is never referenced, only used as a link or ID.

### Types

There are three types that can be specified:

`types.yml`
```yml
aaa
   .bbb
       .ccc()
       .ddd
       .eee[]
```

- An entry ending in `()` (`.ccc()` in this example) will act as a method, and will funnel its route, its args, and its kwargs back to the root, returning whatever the root's `.handle` function returns
- An entry ending in `[]` (`.eee()` in this example) will act as a member attribute that is a `dict`, and will funnel its route and args back to the root, returning whatever the root's `.handle` function returns
- An entry without any `()` or `[]` ending (`.ddd` in this example) will act as an attribute, and will funnel its route back to the root, returning whatever the root's `.handle` function returns


`example.py`
```python
from telescope import Telescope

class Example(Telescope('types.yml','aaa')):
    def __init__(self):
        # init stuff

    def handle(self, route, *args, **kwargs):
        print(route, args, kwargs)

example = Example()
```

### Examples: virtual methods

executed | route | args | kwargs
--- | --- | --- | ---
`example.bbb.ccc()` | '.bbb.ccc()' | () | {}
`example.bbb.ccc('arg1')` | '.bbb.ccc()' | ('arg1',) | {}
`example.bbb.ccc('arg1','arg2',kw1=1,kw2=2)` | '.bbb.ccc()' | ('arg1','arg2') | {'kw1':1, 'kw2':2}



### Examples: virtual dictionaries

executed | route | args | kwargs
--- | --- | --- | ---
`example.bbb.eee[5]` | '.bbb.eee[]' | (5,) | {}
`example.bbb.eee[5:10]` | '.bbb.eee[]' | (slice(5, 10, None),) | {}
`example.bbb.eee[5:10:2]` | '.bbb.eee[]' | (slice(5, 10, 2),) | {}
`example.bbb.eee[1,4,5]` | '.bbb.eee[]' | ((1, 4, 5),) | {}
`example.bbb.eee[1:4,5]` | '.bbb.eee[]' | ((slice(1, 4, None), 5),) | {}
`example.bbb.eee[lambda t: t**2]` | '.bbb.eee[]' | (`<function <lambda> at 0x100000000>`,) | {}



### Examples: virtual attributes


executed | route | args | kwargs
--- | --- | --- | ---
`example.bbb.ddd` | '.bbb.ddd' | () | {}










## Advanced

`Telescope(...,fuse_route=False)` turns off the automatic fusing of the path, returning something like `['.', 'aaa', '.', 'bbb', '.', 'ccc', '()']` instead of the default `'.aaa.bbb.ccc()'`

## Todo

- [ ] Enable `*` in the DSL to allow arbitrary wildcards
