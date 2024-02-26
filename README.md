# Contra Lisp
Experimental lisp dialect and interpreter implemented in python.


## Resources
 - [kanaka/mal](https://github.com/kanaka/mal) is an amazing project I've used to better
  understand the basic nuts and bolts that go into creating a lisp interpreter.
 - [How to write a lisp interpreter in Python](https://norvig.com/lispy.html) by Peter Norvig 
 is an amazing article that has also been incredibly helpful, as is [An even better lisp interpreter in Python](https://norvig.com/lispy2.html).


## Purpose
This is primarily for me to play around with some alternative types of syntax within a lisp dialect.

I think schemes and lisps are fascinating and beautifully simple, but I don't always enjoy
reading and writing lisp code. I like code that is easy to *visually parse* and has a very 
structured feel to it, and for me this doesn't seem to be the case with the many lisp dialects available.

So, I am calling this *Contra Lisp* because I am interested in syntax that is contrary the traditional form of pure prefix notation that lisps are known for. Obivously this is still a lisp and still incorporates 
prefix notation to a large degree, but I'm interested in breaking this up in certain ways.

**Example:**

```python
# infix notation for variable assignment
(set 
  a = 1
  b = 2
  c = 3
  d = (+ a b c)
)

# anonymous objects using infix notation for attribute assignment
(set obj = {
  a: 1
  b: 2
  c: 3
  say-hello:
    (fn [name]
      (echo (+ "hello " name)))
})

# dot notation for accessing object properties & methods
(obj.say-hello "world!")

# use of code blocks (curly braces) instead of a (do ...) form or similiar
# code blocks return nil by default unless a return statement is used (maybe; still tbd)
(fn do-something [a b] {
  (while (< a b)
    (echo (++ a)))
})

# pipe operator that works similiarly to bash/powershell, and allows removing outer layer 
# of parenthesis for pipeline expressions
(>> [1,2,3,3,4,4,5] | foreach {
  (echo @)
})
```

This is mostly just a bunch of rough ideas at this point, and the above is mainly pseudocode that isn't 
completely implemented yet. Some things I'm definitely iterested in are:
- Infix notation for variable assignment and object properties
- Dot operator used to reference object members in a way that is typical of non-lisps
- Pipeline operator/form similiar to bash, to help eliminate nested expressions and parenthesis
- Ability to serialization the AST, objects, lists and other expressions to JSON/YAML. 
- Python interop
- I'm also intersted in some alternative syntax that can be used for defining macros, possibly something that
appears similiar to jinja templates, though ultimately still allows for the same functionality as is typical
for macros in other dialects.

As stated above this is really only intended for experimentation, so I do not have any lofty goals 
with this. Maybe if this turns into something interesting it can be used as a prototype for additional 
implementations in other languages.

## Usage
Note - this requires python 3.10 or higher

1. ### Clone this repository & install locally using pip
    ```shell
    git clone https://github.com/tniedbala/contra-lisp.git
    cd contra-lisp
    pip install -e .
    ```

2. ### Run the below command to start the lisp REPL:
    ```shell
    python -m contra_lisp
    ```

3. ### You should now get a basic repl prompt that allows you to enter statements interactively:
    ```python
     > (set a=1, b=2, c=3)
    3
     > (+ a b c)
    6
     > (set obj = { uno: 1, dos: 2, tres: 3, say-hello: (fn [] (echo "hello world!" ))})
    object{uno dos tres say-hello}
     > obj.uno
    1
     > (obj.say-hello)
    hello world!
    nil
     > _
    ```

## What's been implemented
- Basic types: `block`, `s-expression`, `list`, `object`, `function`, `nil`, `bool`, `number`, `string`, `symbol`, `keyword`.
    - Note that this distinguishes between an `s-expression` versus a `list`. Lists are defined using 
    square braces, while s-expressions are defined using parenthesis. This is for convenience,
    so lists can be easily created without requiring a `quote` function or character. 

- Builtin functions: `+`, `-`, `*`, `/`, `//`, `^`, `echo`

- Special forms: `set`, `fn`, `import`, `eval`
    - This also includes some expermentation I'm doing with `return`, `break` and `continue` forms,
    though these will still need some playing around with.

- Function definitions, which can take either of the following forms:
    ```python
    # assign function to variable name using (set ...)
    (set add = (fn [a b] (+ a b)))

    # named function definition
    (fn add [a b] (+ a b))
    ```

- Object definitions within curly braces and dot-operator referencing:
    ```python
    (set obj = { uno: 1, dos: 2, tres: 3, say-hello: (fn [] (echo "hello world!" ))})
    (obj.say-hello)
    ```

- Importing python objects:
    ```python
    # form 1: import list of symbols as-is; imported python object is assigned to the rightmost name 
    # when a qualified name is imported
    (import print, urllib.parse.quote)
    (print (quote "hello world!"))

    # form 2 - alias imports using key/value pairs
    (import { println: print, urlencode: urllib.parse.quote })
    (println (urlencode "hello world!"))
    ```

- Comments - single line comments are actually denoted using the number `#` char and not a semicolon,
I have just used semicolons in these examples to benefit from the available syntax highlighting.


## What's still needed
A whole lot...
- Lots of additional builtin functions should be added for general purpose usage.
- Additional special forms such as `when`, `macro`, `let`, `loop`, `throw`, `try/catch`
and likely many others.
- User-defined macros still need to be implemented.
- `return`, `break` and `continue` forms will need some updating to ensure these work as intended.
- Objects...
    - Need the ability to `set` object properties using dot references.
    - Would be nice to use keywords to set object metadata (ex: `@readonly: true`)
    - Would be nice to work out a way to include class definitions in addition to anonymous objects.
- Pipeline form as described above does not yet exist.
- Informative exceptions system still needs to be worked out.
- Tail call optimization *should* be working, but this needs to be tested to confirm.
- Some basic documentation for the language beyond this README file.
- Unit tests.
- Probably a lot more that I'm not even thinking of.
