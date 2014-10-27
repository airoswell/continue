# Note on Model

### Frequently used `module`s

- `datetime`: `import datetime`

### admin

- To register the models into admin interface

        admin.site.register(<Model-name>, <ModelAdmin-name>)

### `Query`

#### Modifying the database

- To add new item into a `ManyToManyField`, use

        <Model-name>.<M2M-name>.add(item_1, item_2, ...)

#### Retrieving data from database

###### `filter`

- Usual `filter`s: `filter`, `exclude`

- `filter` can be chained, and applies starting from the left. This is because `filter()` returns a `queryset` object, which is also a `python` `list`.

- `filter` is used as

        <Model-name>.objects.filter(<field-name>='<string>')

- kwargs in `filter()` can be enhanced by adding `__<built-in-operator>`. For instance,

        Article.objects.filter('pub_date__year'='2006')

searches for rows in `Article` with `DateTimeField` `pub_date` where the year is `2006`.

- To apply several criteria simultaneously, just put them as kwargs in `filter()`.

There are many built-in operators

- - `string` matching: `__startwith`, `__endwith`, `__exact`, `__iexact`(case-insensitive exact matching), `__contains`, `__icontains`(case-insensitive).

- - numerical comparison: `lte`, `a`

- Cross table look up can also be done, using `<field-name>__<sub-field_name>`. For instance, if a `Entry` has a `ForeignKey = Blog` `field` called `blog`, then

        Entry.objects.filter(blog__name="Some Blog")

will search in `Entry` table for rows whose `blog` field has `name = 'Some Blog'`. Of course, one can further specify operators, like `blog__name__contain="Blog"`


