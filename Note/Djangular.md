## Integrating `Django` with `AngularJS`

#### Passing data from `Django` to `AngularJS` `controller`

1. Import `serializers`

        from django.core import serializers

2. Build `queryset` object. For instance

        all_users = User.objects.all()

3. `serialize` `queryset` object

        all_users_json = serializers.serialize('json', all_users)
and return `all_users_json` as usual variable in `render()`.

4. Put enclosing tag with `ngController` and `ngInit`, and inside the enclosing tag use verbatim. In this way, `all_users_json` is passed into the `$scope.all_users_from_django` of controller <controller-name> as the initial values of the `ngModel`

        <div ng-controller='<controller-name>'
            ng-init='all_users_from_django={{ all_users_json }}'>
            {% verbatim %}
                {{ all_users_from_django }}
                // Do whatever you like with AngularJS
            {% endverbatim %}
        </div>

5. To enable CSRF in AngularJS, put

        app.config(['$httpProvider', function($httpProvider) {
          $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
          $httpProvider.defaults.xsrfCookieName = 'csrftoken';
          $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }]);


6. To POST **non-form** data to Django, first config the above CSRF configuration, then use `$http()` method

        $http({ 
          method: 'POST', 
          url: '/url/', 
          data: <js-object>
        }).success(function(data, status, headers, config){
          console.log(data)
        })
and in the `view` function, obtain data via `data = json.loads(request.body)`. Of course, one need to `import json` first.

If the data posted are **form** data, then in the view function just user `request.post[field-name]`.

7. `GET` request to Django: user

        $http({
          method: 'GET',
          url: 'url/?para1=val1&para2=val2&...',
        })
and in the corresponding view function, use `request.GET['']`