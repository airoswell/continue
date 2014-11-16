from app.models import RegUser, Item, Post, PassEvent, ItemPostRelation

ItemPostRelation.objects.all()

ItemPostRelation.objects.create(item=item, post=post)