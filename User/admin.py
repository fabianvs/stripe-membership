from django.contrib import admin

from .models import Student, Profesor, Pay_method, Document, Post_file


admin.site.register(Student)
admin.site.register(Profesor)
admin.site.register(Pay_method)
admin.site.register(Document)
admin.site.register(Post_file)