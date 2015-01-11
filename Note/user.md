## Basic structure

### Sign up form
- `id = 'signup_form'`
- `method = 'post'`
- `ng-submit='submit'`: after validation, use `$event.target.submit()`:

        $scope.submit = function($event){
            ...
            $event.target.submit();
        }
- #### Child input fields
- - `{% csrf_token %}`
- - `<input id='id_username' name='username' type='text'>`
- - `<input id='id_email' name='email' type='email'>`
- - `<input id='id_password1' name='password1' type='password'>`
- - `<input id='id_password2' name='password2' type='password'>`