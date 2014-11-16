## Views

#### `index_view()`

#### `results_view()`

#### `user_view()`

#### `login_view()`




## Controllers

#### `get_user(request)`

check if the current user is anonymous or authenticated

#### `user_post(request)`

- `data = json.loads(request.body)`

- Use `data['type']` is to determine which action to take

- All user-post-related request go into this view function

#### 


## Global functions

#### All `post` sending around the site should follow the following structure (where `#` terms are optional depending on the situation)

        post = {
            # id: '', 
            title: 'post title',
            zip_code: '11790',
            owner: '',
            items: [],
        }
or user the `factory` `Item`

#### All 'item' sending around should follow the following structure

        item = {
            # id: '',
            title: 'item title',
            quantity: 3,
            detail: "",
            condition: 'Gd',
            status: 'av',
        }

#### `user_get_posts(user_id)`

#### `user_edit_post(post_data, post_id, user)`

- Retrieve post_id, check if the current user `user` is the same as the `post.owner`

- If so, proceed to save the new data.

#### `user_create_post(post_data, user_id)`

