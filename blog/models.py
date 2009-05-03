#:coding=utf8:

from django.contrib.auth.models import User
from tagging.models import *
from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

from datetime import datetime

BLOG_LOCALES = (
    ('jp', u'日本語'),
    ('en', u'English'),
)

class PostManager(Manager):
    def active(self):
        return self.filter(pub_date__lt = datetime.now(), active=True)

class Post(Model):
    author = ForeignKey(User, verbose_name=u"author")
    slug = SlugField(u"slug", max_length=50)
    title = TextField(u"title")
    content = TextField(u"content")
    markup_type = models.CharField(max_length=10, choices=(
        ("html", "HTML"),
        ("rst", "reStructuredText"),
    ), default="html")
    locale = CharField(u'locale', max_length=20, choices=BLOG_LOCALES, default="en")
    tags = TagField()

    active = BooleanField(u'active', default=False)
    pub_date = DateTimeField(u'date', default=datetime.now)
    create_date = DateTimeField(u'created', default=datetime.now)
   
    objects = PostManager()

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ('-pub_date',)