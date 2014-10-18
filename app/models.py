from django.db import models

# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=1024, blank=False)

    def __unicode__(self):
        return self.title


class Person(models.Model):
    name = models.CharField(max_length=127, blank=False)
    item = models.ManyToManyField(Item, through='Ownership')

    def __unicode__(self):
        return self.name


class Ownership(models.Model):
    item = models.ForeignKey(Item)
    Person = models.ForeignKey(Person)

# class Item(models.Model):
#     title = models.CharField(max_length=144, blank=False, null=False)
#     quantity = models.IntegerField(default=1)
#     condition_choices = (
#         ('Ln', 'Like new'),
#         ('Gd', 'Good'),
#         ('Fr', 'Fair'),
#     )
#     description = models.TextField(default='')
#     link = models.CharField(max_length=1024, default='')
#     time_created = models.DateTimeField(auto_now_add=True)
#     past_owner = models.ManyToManyField(RegUser)
#     past_post = models.ManyToManyField(Post)

#     def __unicode__(self):
#         return self.title


# class RegUser(models.Model):
#     name = models.CharField(max_length=200, blank=False, null=False)
#     email = models.EmailField(blank=False)
#     post - models.ForeignKey(Post)
#     received_item = models.ManyToManyField(Item)
#     pass_item = models.ManyToManyField(Item)

#     def __unicode__(self):
#         return self.name


# class Post(models.Model):
#     title = models.CharField(max_length=144, blank=False, null=False)
#     item = models.ManyToManyField(Item)
#     time_created = models.DateTimeField(auto_now_add=True)

#     def __unicode__(self):
#         return self.title


# class Event(models.Model):
#     item = models.ForeignKey()
