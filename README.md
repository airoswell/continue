# The View structure

### `index()`

### `List()`

### `User()`



# The database structure

### `RegUser` `class`

- `name` (`CharField`)
- `email` (`EmailField`)
- `posts` (`ForeignKey`: `Post`)
- `received_item` (ManyToManyField: `Item`)
- `passed_item` (ManyToManyField: `Item`)

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
- `past_owner` (`ManyToManyField`: `RegUser`)
- `past_post` (`ManyToManyField`: `Post`)

### The `Event` `class`

- `item` (`ForeignKey`: `Item`)
- `post` (`ForeignKey`: `Post`)
- `date_passed` (`DateTimeField`)
- `from_user` (`ForeignKey`: `RegUser`, related_name="PASS_FROM")
- `to_user` (`ForeignKey`: `RegUser`, related_name="PASS_TO")