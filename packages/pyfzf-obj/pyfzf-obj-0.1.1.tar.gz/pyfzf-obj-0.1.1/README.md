# Forked changes

This is a very lightweight fork  of Sean Breckenridge's `pyfzf-iter`.

This is the behavior of the original project.

```
one_digit = FzfPrompt.prompt([x for x in range(10)])
type(one_digit)     # list
type(one_digit[0])  # str
```

I disliked sending Python objects to `FzfPrompt` and receiving back strings, so I implemented a dictionary to retrieve the original object. Beats setting a dictionary every time, though I have questions about performance. You can find it as `retrieval` in the `FzfPrompt.prompt()` method. Kosher enough.

What might cause dissent, however, is that if only one item is selected, it returns that item, not an enclosing list. Since I mostly use the tool in interactive, viz. `ipython` sessions, my goal was to get the following to work:

```
one_digit = FzfPrompt.prompt([x for x in range(10)])
type(one_digit)     # int
```

The problem I anticipate is that one can't reliably iterate through the results of `FzfPrompt.prompt(my_variable)`, in structures like the following, since int or str might not be iterable. That is, one doesn't know what one is iterating through: the list of chosen objects, or the objects themselves? Take, for instance:

```
# set up your preferred fzf defaults
mypyfzf = FzfPrompt('fzf-tmux', '-p 50%', '--reverse')

# if we happen to choose only one number, for will try and fail to iterate over it
for number in mypyfzf.prompt([x for x in range(10)], "--multi"):
    print(number ** 2)
```

This is hardly a problem apart from use in APIs. Tools like `gum choose` may be superior here. Furthermore, 
our iterables are usually 'regulated' objects. I.e., there's some rule binding all the objects together. IMO, you're better off filtering with boolean conditions and declaring outliers manually, and using the present class for variable assignments in interactive scripts.

## Next steps
If '--multi' is in the list of options when `FzfPrompt.prompt()` is called, return a list, no matter the length of the result.
Or inversely, only activate this 'isolating' behavior if '--no-multi' is in the options.
