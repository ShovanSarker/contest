from django.conf.urls import patterns, include, url
from django.contrib import admin
from frontend.views import contest_page, contest_page1, get_info
from admin_user.views import login_page, login_auth, logout_now, home, profile, change_password, admins_list,\
    add_new_contest, add_contest_info, contest_list, change_contest_status, show_images, add_admin, add_admin_info, \
    change_admin_status, upload_photo
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'contest.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^superadmin/', include(admin.site.urls)),
                       url(r'^$', view=contest_page, name='home'),
                       # url(r'^ff', view=contest_page1, name='home'),
                       url(r'^shajgoj/get_info/', view=get_info, name='home'),
                       url(r'^shajgoj/contest_list/', view=contest_list, name='home'),
                       url(r'^shajgoj/admin/', view=login_page, name='home'),
                       url(r'^shajgoj/login_auth/', view=login_auth, name='home'),
                       url(r'^shajgoj/home/', view=home, name='home'),
                       url(r'^shajgoj/profile/', view=profile, name='home'),
                       url(r'^shajgoj/change_password/', view=change_password, name='home'),
                       url(r'^shajgoj/logout/', view=logout_now, name='home'),
                       # url(r'^adminlist/', view=ad mins_list, name='home'),
                       url(r'^shajgoj/list/', view=admins_list, name='home'),
                       url(r'^shajgoj/add_new_contest/', view=add_new_contest, name='home'),
                       url(r'^shajgoj/add_contest_info/', view=add_contest_info, name='home'),
                       url(r'^shajgoj/change_contest_status/', view=change_contest_status, name='home'),
                       url(r'^shajgoj/show_images/', view=show_images, name='home'),
                       url(r'^shajgoj/add_admin/', view=add_admin, name='home'),
                       url(r'^shajgoj/add_admin_info/', view=add_admin_info, name='home'),
                       url(r'^shajgoj/change_admin_status/', view=change_admin_status, name='home'),
                       url(r'^shajgoj/upload_photo/', view=upload_photo, name='home'),

                       )
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
