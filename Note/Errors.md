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