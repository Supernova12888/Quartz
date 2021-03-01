# Quartz



## Learn

**Variables** are used for storing values such as numbers, string, booleans, lists, and objects. To create a variable, start with the `def` keyword, followed by the variable name, then the value of the variable.
```
def num: 12;
def str: "Hi";
def bool: true;
def list: (1, 2, 3);
def obj: {};
```
This is an example of a constant variable. You cannot change the value of a constant variable.
```
def num:: 12;

# Error!
num: 14;
```
This is an example of a variable that has an `in` keyword:
```
def list: (1, 2, 3);
def idx in list;
```

### Lists
**Lists** An example of a list is below. Indexing starts at zero, just like most other programming languages.
```
def list: (1, 2, 3);
print[list(0)];
```

### Objects
```
def math: {
    number: 1,
    addOne: [] {
        this.number++;
    }
};
math.number: 9;
math.addOne[];
```

### Console
Use the built-in `print[]` function to print something into the console.
```
print["Text"];
```

### Functions
**Functions** are used to execute multiple lines of code at once. You can execute a function multiple times.
```
def add[x, y] {
    output x + y;
}
add[1, 2];
```
**Inline functions** are functions in one line of code. These functions can only have *one statement*.
```
def add[x, y]: output x + y;
add[1, 2];
```

### Loops
#### For Loops
```
# Normal version
for [def i: 0, i < 10, i++] {
    print[i];
}

# Inline version
for [def i: 0, i < 10, i++]: print[i];
```
#### Each Loops
```
# Normal version
def list: (1, 2, 3);
each [def i in list] {
    print[list];
}

# Inline version
def list: (1, 2, 3);
each [def i in list]: print[list];
```
#### While Loops
```
# Normal version
def i: 0;
while [i < 10] {
    print[i];
}

# Inline version
def i: 0;
while [i < 10]: print[i];
```
#### Repeat Loops
```
# Normal version
repeat [10] {
    print["Hello world!"];
}

# Inline version
repeat [10]: print["Hello world!"];
```
#### Stop/Skip
```
for [def i: 0, i < 10, i++] {
    if [i = 3] {
        skip;
    }
    print[i];
}

for [def i: 0, i < 10, i++] {
    if [i = 6] {
        stop;
    }
    print[i];
}
```

### Operators
#### Logical Operators
```
if [x = 1 && y = 1] {
    print["Hello world!"];
}
if [x = 1 || y = 1] {
    print["Hello world!"];
}
if [~x] {
    print["Hello world!"];
}
```

### If Statements
```
if [x < 10] {
    print["x is less than 10"];
} elif [x < 20] {
    print["x is less than 20"];
} elif [x < 30] {
    print["x is less than 30"];
} else {
    print["x is greater than 29"];
}
```
#### Shorthand If-Else Statements
```
x = 1 ? print("x is 1") | print("x is not 1");
```






