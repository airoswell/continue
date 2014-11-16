from app.models import RegUser, Item, Post, ItemPostRelation
import logging
import pdb

logger = logging.getLogger(__name__)


class ItemContent:
    def __init__(self, item_id, owner_id, title, quantity, condition, detail, status):
        self.item_id = item_id
        self.owner_id = owner_id
        self.title = title
        self.quantity = quantity
        self.condition = condition
        self.detail = detail
        self.status = status


class PostContent:
    def __init__(self, post_id, title, zip_code, owner, detail,
            date_posted, time_posted):
        # Don't use .id, which cause unknown problem
        self.post_id = post_id
        self.title = title
        self.zip_code = zip_code
        self.owner = owner
        self.items = []
        self.detail = detail
        self.date_posted = date_posted
        self.time_posted = time_posted

    def add_item(self, item_content):
        # .__dict__ turn Python object into serializable object
        self.items.append(item_content.__dict__)


def posts_writer(posts_queryset):
    """
    A global function: turn a queryset of post to
    simple JSON serializable objects
    """
    posts = []
    for post in posts_queryset:
        post_content = PostContent(
            post_id=post.id,
            title=post.title,
            zip_code=post.zip_code,
            owner=post.owner.username,
            detail=post.detail,
            date_posted=str(post.time_posted.date()),
            time_posted="sometime",
        )
        for item in post.item.all():
            # Use filter instead to avoid error when there are repeated
            # [item_post_relation, ItemPostRelation] records
            item_post_relation = ItemPostRelation.objects.filter(
                item=item,
                post=post,
            )[0]
            item_content = ItemContent(
                item_id=item.id,
                owner_id=item.current_owner.id,
                title=item.title,
                quantity=item.quantity,
                condition=item.condition,
                detail=item.detail,
                status=item_post_relation.item_status,
            )
            post_content.add_item(item_content)
        posts.append(post_content.__dict__)
    # Return the [posts, List]
    return posts


# Return all posts of a given [user, RegUser]
def user_get_posts(user):
    posts_queryset = Post.objects.filter(owner__id=user.id).all()
    posts = posts_writer(posts_queryset)
    return posts


def user_create_post(post_data, user):
    # pdb.set_trace()
    if user.is_authenticated():
        owner = RegUser.objects.get(id=user.id)
        # pdb.set_trace()
        # Build a new post
        post = Post(
            title=post_data['title'],
            detail=post_data['detail'],
            zip_code=post_data['zip_code'],
            owner=owner
        )
        post.save()         # Save [post] first to generate id for later use
        # pdb.set_trace()
        for item_data in post_data['items']:
            post.add_item(item_data)
        return True, 'Created', post


def user_edit_post(post_data, user):
    post = Post.objects.get(id=post_data['post_id'])
    if user.id != post.owner.id:
        return False, "You are not the owner!", {}
    if post:
        post.title = post_data['title']
        post.detail = post_data['detail']
        post.zip_code = post_data['zip_code']
        items = post_data['items']
        for item in items:
            if item['item_id'] != 'undefined':
                Item.objects.filter(id=item['item_id']).update(
                    title=item['title'],
                    quantity=item['quantity'],
                    condition=item['condition'],
                    detail=item['detail'],
                )
                # update item-post-relation
            else:
                owner = RegUser.objects.get(id=user.id)
                new_item = Item(
                    title=item['title'],
                    current_owner=owner,
                    quantity=item['quantity'],
                    condition=item['condition'],
                    detail=item['detail'],
                )
                # Save the item first before creating relation
                new_item.save()
                ItemPostRelation(
                    item=new_item,
                    post=post,
                    item_status='av',
                ).save()
        post.save()
        return True, "Successfully edit the post.", post


def user_delete_post(post_data, user):
    post_id = post_data['post_id']
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return True, "Successfully deleted!"
    except Post.DoesNotExist:
        return False, "The post does not exist!"
