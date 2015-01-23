#### Attribute error: cannot get 'id' ...
- Calling function expects return value of the form `tuple`, but returned
one variable:

        # originally
        instance, error = some_function(....)
        # some_function
        def some_function():
            ...
            return instance


#### On server, `BdbQuit at /app/user/dashboard/` implies there is `pdb.set_trace()` some where.


#### Updated item, but the update did not show in the timeline or feeds, may be it is because the updated field is not in the tracked_fields.

#### Every time you want to refer to an element in a list or dict, **MAKE SURE** the element is in the list or dict, or object.

#### When everything are expected to go smoothly but errors shows up, you might have `pdb` around, having `broken pipe`.


#### If `restmod` returns response which does not get loop through, or `response.length = undefined`, that means the `response` is not an array, and it might be caused by using `$find()` instead of `$search()`


#### `restmod`: if a collection is obtained by `.$search(params)`, one should overwrite the `params` in future requests if necessary, otherwise the same `params` will be called in every future `.$fetch()`.