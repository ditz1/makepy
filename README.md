### file directory
you must have your file directory in this format <br />
/workspace <br />
\ <br />
 | - src <br />
 |   \ - main.c <br />
 | - include <br />
 |   \ - header.h <br />
 | - lib <br />
 |   \ - lib.a <br />
 | <br />
 | - make.py <br />

### build
```
python3 make.py build
```

or 

```
python3 make.py b
```

(will try to build by default if no args are provided)

### other args
```
clean, c
```

```
run, r
```
(will build and run if not built)

```
rebuild, rb
```

