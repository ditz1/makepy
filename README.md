### file directory
you must have your file directory in this format
/workspace
\
 | - src
 |   \ - main.c
 | - include
 |   \ - header.h 
 | - lib
 |   \ - lib.a
 |
 | - make.py

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

