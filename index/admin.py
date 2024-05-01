import os
from django.contrib import admin
from .models import Item,Category,sendmessage,wishlistModel,Ordermodel
import base64

class Base64ImageAdmin(admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ['name','category','price','condition']

    def save_model(self, request, obj, form, change):
        if 'photos' in form.cleaned_data:
            image = form.cleaned_data['photos']
            file_path = '/tmp/' + image.name
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            with open(file_path, 'rb') as image_file:
                obj.image_encoded = base64.b64encode(image_file.read()).decode('utf-8')
            os.remove(file_path)
        super(Base64ImageAdmin, self).save_model(request, obj, form, change)

    def image_tag(self, obj):
        return u'<img src="data:image/png;base64,%s" />' % obj.base64_image
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
admin.site.register(Item,Base64ImageAdmin)
admin.site.register(sendmessage)
admin.site.register(Category)

class wishlistAdmin(admin.ModelAdmin):
    list_display = ['itemId','userId','price']

admin.site.register(wishlistModel,wishlistAdmin)


class orderAdmin(admin.ModelAdmin):
    list_display = ['productid','username','orderamount','transactionid','orderdatetime']

admin.site.register(Ordermodel,orderAdmin)


admin.site.site_header = 'Click Check Chat Buy Administration'                    # default: "Django Administration"
admin.site.index_title = 'Click Check Chat Buy system'                 # default: "Site administration"
admin.site.site_title = 'Click Check Chat Buy system' 