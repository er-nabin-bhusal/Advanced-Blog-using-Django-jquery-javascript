from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe

from markdown_deux import markdown 
from comments.models import Comment 

from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time

# Create your models here.
#MVC model view controller


#Post.objects.all()
#Post.objects.create(user=user,title='title',content="contents hererelkj")
class PostManager(models.Manager):
	def active(self,*args,**kwargs):
		#Post.objects.all()=super(PostManager,self).all() 
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	# filebase,extension = filename.split(".")
	# return "%s/%s.%s" %(instance.title,instance.title, extension)
	return "%s/%s" %(instance.title, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=130)
	slug = models.SlugField(unique=True)
	image = models.ImageField(
		upload_to=upload_location , 
		null=True,
		blank=True,
		width_field='width_field',
		height_field='height_field'
		)
	height_field = models.IntegerField(null=True,default=0)
	width_field = models.IntegerField(null=True,default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	# read_time = models.TimeField(blank=True, null=True)
	read_time = models.IntegerField(default=0,blank=True,null=True)
	
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		#return "/post/%s/" %(self.id)
		return reverse('posts:detail', kwargs={'slug':self.slug})

	class Meta:
		#for sorting the data in the models
		#meta class helps in providing features in the models except any fields
		ordering = ['-timestamp','-updated']#here - sign shows that negative

	def get_markdown(self): #this is intance "method" and we have called it directly in the post_list.html 
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

	@property #since this is a property decorator it is only to display that it acts as a property of the given class
	def comments(self):#although this we dont use in rendering comments now but it can be done this way also
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs 
		
	@property
	def get_content_type(self):
		instance = self 
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


def create_slug(instance,new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists() 
	if exists:
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug



def pre_save_post_receiver(sender,instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

	if instance.content:
		html_string = instance.get_markdown()
		read_time = get_read_time(html_string)
		instance.read_time = read_time 


pre_save.connect(pre_save_post_receiver, sender=Post)


















