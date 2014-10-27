from app.models import RegUser, Item, Post, PassEvent

RegUser.objects.all()
lelouch = RegUser.objects.create(name="Lelouch", email='lelouch@gmail.com')
lili = RegUser.objects.create(name="Lili", email="lili@yahoo.com")

macbook = Item.objects.create(title='laptop', quantity=1, condition='Ln', description="A macbook air", link='')

free_macbook = Post.objects.create(title='Free Macbook Air!!!', owner=lelouch)

pass_batter_event = PassEvent.objects.create(item=macbook, post=free_macbook, giver=lelouch, receiver=lili)

title = ['Cookies', 'drawer', 'King size bed', 'ipad', 'mug', 'cups']

for item in title:
    Item.objects.create(title=item, quantity = 1)

Item.objects.all()