# Getting started

- To start a project:
    
        django-admin.py startproject <project-name>

After such command, you will have a root folder <project-name>
which contains another folder with the same name <project-name>

- To run a server:

        python manage.py runserver

and a server will run immediately.

- To start a database, or to add new model into database file:

        python manage.py syncdb

and a database will be generated. After running the server, go to
    
        http://127.0.0.1:8000/admin/

will bring one to the admin interface.

- To start an app (part of a project), use

        python manage.py startapp <model-name>

A new folder called <model-name> will be created. 

- To create a model, define a class inhered from models.Model

    class <model-name>(models.Model):
        col_1 = models.CharField(max_length=120, ...)

- To register the model to admin:

    from .models import <model-name>

The `.` implies it is relative path. Then create new class

    class <model-name-admin>(admin.ModelAdmin):
        class Meta:
            model = <model-name>
and finally

     admin.site.register(<model-name>, <model-name-admin>)

- In the setting.py, set

    TEMPLATE_DIRS = (
        os.path.join(
            os.path.dirname(__file__),
            'static',
            'templates'
        ).replace('\\', '/'),
    )

will set the templates folder to folder /<project-name>/<project-name>

- To open django `shell`
        
        python manage.py shell

- - To import a `table`

            from <app-name>.models import <table-name>

- - To get the `array` of all rows of a `table`

            <table-name>.objects.all()





# Templating in Views.py

- Before anything, put templating HTML in folder `<app-name>/templates/<app-name>/`

- First one needs to import `modules` `RequestContext`, `loader`, 

        from django.template import RequestContext, loader

- Second calls `loader.get_template(url)` method, where `url` is relative to `<app-name>/templates/` to retrieve the templating `HTML` file.

- Third, build a `RequestContext` object:

        context = RequestContext(
            request,
            {
                vars: python-vars
            }
        )

- Finally, `return HttpResponse(template.render(context))` to pass all variables to the HTML file.

### Shortcut of templating

One can import `render` module

    from django.shortcuts import render

Then in controllers, `return ` a render() method

    def <controller-name>(request):
        return render(
            request,
            <template path with respect to /Templates/>,
            optional object,
        )



# Database in Views

- To import a table:

        from <app-name>.models import <table-name>

- To retrieve all records of a table

        rows = <table-name>.objects.order_by(<col-name, string>)[3: 9]

# To integrate AngularJS with Django:

- First, install Djangular via

    pip install django-angular

- In project `setting.py`, include `djangular` into 'INSTALLED_APPS'.

- Set 'STATIC_ROOT' to arbitrary absolute path in the operating system,
e.g. `/Users/Lelouch/Downloads`, any path that you can access.

- Run `python manage.py collectstatic`, which will put all static files, including the `Djangular` into that ROOT directory.

- Copy the `djangular`, which contains `css` and `js` files to under `app/static/`.

- Include the references to `djangular` in the templating `HTML` files.


# Managing static files

There are several variables in `setting.py` controlling the static files locations.

- `STATIC_ROOT`: an arbitrary directory on the machine, e.g. `/Users/Lelouch/Downloads`. This folder is a temporary folder to collect static files collected by terminal command `python manage.py collectstatic`.

- `STATIC_URL`: default to be `/static/`. With the default value, Django will look for all `/static/` folders within each `app` folder.