from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe
from .models import *
from PIL import Image

class NotebookAdminForm(ModelForm):

	

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].help_text = mark_safe(f'<span style="color:red">Загружайте изображение между {Product.MIN_RESOLUTION[0]}*{Product.MIN_RESOLUTION[1]} и  {Product.MAX_RESOLUTION[0]}*{Product.MAX_RESOLUTION[1]}</span>')


	def clean_image(self):
		image = self.cleaned_data['image']
		img = Image.open(image)
		print(img.width, img.height)
		min_height, min_width =  Product.MIN_RESOLUTION
		max_height, max_width =  Product.MAX_RESOLUTION
		print(Product.MAX_IMAGE_SIZE)
		if image.size > Product.MAX_IMAGE_SIZE:
			raise ValidationError(f'Рарешение изображения не должно превышать 3 мегабайта, вы пытаетесь загрузить {image.size}')
		if img.height < min_height or img.width < min_height:
			raise ValidationError('Минимальное разрешение изображения {}*{}, вы пытаетесь загрузить {}*{}'.format(*Product.MIN_RESOLUTION, *(img.width, img.height,)))
		if img.height > max_height or img.width > max_width:
			raise ValidationError('Максимальное разрешение изображения {}*{}, вы пытаетесь загрузить {}*{}'.format(*Product.MAX_RESOLUTION, *(img.width, img.height,)))
		return image

class NotebookAdmin(admin.ModelAdmin):

	form = NotebookAdminForm
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
	    if db_field.name == 'category':
	        return ModelChoiceField(Category.objects.filter(slug='notebooks'))
	    return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)




