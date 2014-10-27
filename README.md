# The View structure

### `index()`

### `List()`

### `User()`



# The database structure

### `RegUser` `class`

- `name` (`CharField`)
- `email` (`EmailField`)
- `posts` (`ForeignKey`: `Post`)
- `to_users` (`ManyToManyField`: `'self'`, `symmetrical=False`, `through`=`'PassEvent'`, `through_fields=('giver', 'receiver')`)

### The `Post` `class`

- `title` (`CharField`)
- `items` (`ManyToManyField`: `Item`)
- `pub_date_time` (`DateTimeField`)

### The `Item` `class`

- `id` (`CharField`)
- `title` (`CharField`)
- `quantity` (IntegerField)
- `condition` (CharField)
- `description` (`TextField`)
- `link` (CharField)
- `time_created` (`DateTimeField`)

### The `PassEvent` `class`

- `item` (`ForeignKey`: `Item`)
- `post` (`ForeignKey`: `Post`)
- `time_happenedd` (`DateTimeField`)
- `giver` (`ForeignKey`: `RegUser`, `related_name="events_as_giver"`)
- `receiver` (`ForeignKey`: `RegUser`, `related_name="events_as_receiver"`)

### Common `query`

- Given an `Item`, retrieve all related past `giver`s
    
        RegUser.objects.filter(events_as_giver__item=<item-object>)

- Given a `RegUser` `john`, retrieve all related `to_users`

        john.to_users.all()

- Given a `RegUser` `john`, retrieve all `Item`s that `john` gave out

        Item.objects.filter(related_events__giver=john)

- Given a `RegUser` `jane`, retrieve all `Item`s that `jane` received

        Item.opbjects.filter(related_events__receiver=jane)

