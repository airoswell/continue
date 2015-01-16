#### Attribute error: cannot get 'id' ...
- Calling function expects return value of the form `tuple`, but returned
one variable:

        # originally
        instance, error = some_function(....)
        # some_function
        def some_function():
            ...
            return instance
