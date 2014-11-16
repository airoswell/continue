## Error handlers

### 1. No record found
#### post_writer()
    item_post_relation = ItemPostRelation.objects.get(
        item=item,
        post=post,
    )

#### user_create_post()
    owner = RegUser.objects.get(id=user.id)

#### user_edit_post()
    post = Post.objects.get(id=post_data['post_id'])