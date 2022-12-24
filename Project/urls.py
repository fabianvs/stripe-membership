from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
#local urls
from User import views as user_views
from User.webpay import views as webpay
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),

    #user_views
    path('', user_views.home_view, name='home'),
    path('user/login/', user_views.login_view, name='login'),
    path('user/logout/', user_views.logout_view, name='logout'),
    path('user/signup/', user_views.signup, name='signup'),
    path('user/roll', user_views.Choise_roll.as_view(), name='roll'),
    path('user/addstudent/', user_views.student_create, name='add_student'),
    path('user/addprofesor/', user_views.profesor_create, name='add_profesor'),
    path('user/profile/', user_views.profile, name='profile'),
    path('user/profile/update/<int:pk>', user_views.profile_update, name='profile_update'),
    path('profesor/list', user_views.search_profesor, name='prof_list'),
    path('file/list', user_views.document_list, name='doc_list'),
    path('file/upload', user_views.upload_document, name='upload_file'),
    path('post/file', user_views.post_file, name='post_file'),
    path('post/list', user_views.post_list, name='post_list'),
    path('file/update/<int:pk>', user_views.DocumentUpdateView.as_view(), name='update_file'),
    path('post/update/<int:pk>', user_views.Post_fileUpdateView.as_view(), name='update_post'),
    path('post/delete/<int:pk>', user_views.Post_fileDeleteView.as_view(), name='delete_post'),
    path('file/delete/<int:pk>', user_views.DocumentDeleteView.as_view(), name='delete_file'),
    # TBK Views
    path('suscripcion/<int:pk>', webpay.TbkInit.as_view(), name='tbk_init'),
    path('suscripcion/return/', csrf_exempt(webpay.TbkReturn.as_view()), name='tbk_return'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)