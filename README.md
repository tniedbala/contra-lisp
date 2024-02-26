# Contra Lisp
Experimental lisp dialect and interpreter implemented in python.

## Purpose
This is primarily for me to play around with some alternative types of syntax within a lisp dialect.

I think schemes and lisps are fascinating and beautifully simple, but I don't always enjoy
reading and writing lisp code. I like code that is easy to *visually parse* and has a very 
structured feel to it, and for me this doesn't seem to be the case with the many lisp dialects available.

So, I am calling this *Contra Lisp* because I am interested in syntax that is contrary the traditional form of pure prefix notation that lisps are known for. Obivously this is still a lisp and still incorporates 
prefix notation to a large degree, but I'm interested in breaking this up in certain ways.

**Example:**

```clojure
; infix notation for variable assignment
(set 
  a = 1
  b = 2
  c = 3
  d = (+ a b c)
)

; anonymous objects using infix notation for attribute assignment
(set obj = {
  a: 1
  b: 2
  c: 3
  say-hello:
    (fn [name]
      (echo (+ "hello " name)))
})

; dot notation for accessing object properties & methods
(obj.say-hello "world!")

; use of code blocks (curly braces) instead of a (do ...) form or similiar
; code blocks return nil by default unless a return statement is used (maybe; still tbd)
(fn do-something [a b] {
  (while (< a b)
    (echo (++ a)))
})

; pipe operator that works similiarly to bash/powershell, and allows removing outer layer 
; of parenthesis for pipeline expressions
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