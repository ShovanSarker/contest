from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from admin_user.models import AdminUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from contest_panel.models import ContestPanel, ContestImage
# Create your views here.


@csrf_exempt
def login_page(request):
    return render(request, 'admin_login.html')


@csrf_exempt
def login_auth(request):
    postdata = request.POST
    print(postdata)
    if 'username' and 'password' in postdata:
        print(postdata['username'])
        print(postdata['password'])
        user = authenticate(username=postdata['username'], password=postdata['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = postdata['username']
                if user.is_superuser:
                    res = redirect('/superadmin')
                else:
                    res = redirect('/home')
            else:
                res = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'The password is valid, but the account has been disabled!'})
        else:
            res = render(request, 'admin_login.html',
                         {'wrong': True,
                          'text': 'The username and password you have entered is not correct. Please retry'})
    else:
        res = render(request, 'admin_login.html', {'wrong': False})

    res['Access-Control-Allow-Origin'] = "*"
    res['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    res['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
    return res


@login_required(login_url='/admin/')
def home(request):
    page_title = 'Home'
    user = request.session['user']
    admin_user = AdminUser.objects.get(username__exact=user)
    if AdminUser.objects.filter(username__exact=user).exists() and admin_user.Active:
        loggedinuser = admin_user.Name
        all_contests = ContestPanel.objects.all()
        display = render(request, 'dashboard.html', {'loggedInUser': loggedinuser,
                                                     'page_title': page_title,
                                                     'all_contests': all_contests})
    else:
        display = render(request, 'admin_login.html',
                         {'wrong': True,
                          'text': 'You are not authorized to login. Please contact administrator for more details'})
    return display


def logout_now(request):
    logout(request)
    return redirect('/admin')


@login_required(login_url='/admin/')
def profile(request):
    page_title = 'Profile'
    user = request.session['user']
    admin_user = AdminUser.objects.get(username__exact=user)
    if AdminUser.objects.filter(username__exact=user).exists() and admin_user.Active:
        admin_user = AdminUser.objects.get(username__exact=user)
        loggedinuser = admin_user.Name
        username = user
        email = admin_user.Email
        phone = admin_user.Phone
        active = admin_user.Active
        isadmin = admin_user.Admin
        joined_since = admin_user.DateAdded
        if admin_user.Active:
            display = render(request, 'profile.html', {'loggedInUser': loggedinuser,
                                                       'page_title': page_title,
                                                       'username': username,
                                                       'email': email,
                                                       'phone': phone,
                                                       'active': active,
                                                       'isadmin': isadmin,
                                                       'joined_since': joined_since})
        else:
            logout(request)
            display = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        logout(request)
        display = render(request, 'admin_login.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please LOGIN again.'})
    return display


@login_required(login_url='/admin/')
def change_password(request):
    page_title = 'Change Password'
    user = request.session['user']
    post_data = request.POST
    wrong = False
    text = ''
    if 'csrfmiddlewaretoken' in post_data:
        if post_data['password'] == post_data['re-password']:
            if User.objects.filter(username=user).exists():
                u = User.objects.get(username=user)
                u.set_password(post_data['password'])
                u.save()
                wrong = True
                text = 'Password is successfully changed'
            else:
                wrong = True
                text = 'Something Wrong'
        else:
            wrong = True
            text = 'Passwords do NOT match. Please try again'
    admin_user = AdminUser.objects.get(username__exact=user)
    if AdminUser.objects.filter(username__exact=user).exists() and admin_user.Active:
        admin_user = AdminUser.objects.get(username__exact=user)
        loggedinuser = admin_user.Name
        if admin_user.Active:
            display = render(request, 'changePassword.html', {'loggedInUser': loggedinuser,
                                                              'page_title': page_title,
                                                              'wrong': wrong,
                                                              'text': text})
        else:
            logout(request)
            display = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        logout(request)
        display = render(request, 'admin_login.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please LOGIN again.'})
    return display


@login_required(login_url='/admin/')
def admins_list(request):
    user = request.session['user']
    # if admin
    print('here')
    admin_user = AdminUser.objects.get(username__exact=user)
    if AdminUser.objects.filter(username__exact=user).exists() and admin_user.Active:
        # admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedInUser = admin_user.Name
        if admin_user.Active and admin_admin:
            all_admin_users = AdminUser.objects.all()
            display = render(request, 'admin_list.html',
                             {'loggedInUser': loggedInUser,
                              'page_title': 'List Of Admins',
                              'all_admin_users': all_admin_users})
        else:
            logout(request)
            display = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login.'
                                      ' Please contact administrator for more details'})
    else:
        display = redirect('/')
    return display


@login_required(login_url='/admin/')
def add_new_contest(request):
    user = request.session['user']
    if AdminUser.objects.filter(username__exact=user).exists():
        # admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedInUser = admin_user.Name
        if admin_user.Active and admin_admin:
            all_admin_users = AdminUser.objects.all()
            display = render(request, 'add_contest.html',
                             {'loggedInUser': loggedInUser,
                              'page_title': 'Add New Contest',
                              'all_admin_users': all_admin_users})
        else:
            logout(request)
            display = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login.'
                                      ' Please contact administrator for more details'})
    else:
        display = redirect('/')
    return display



@login_required(login_url='/admin/')
def add_contest_info(request):
    user = request.session['user']
    post_data = request.POST
    file_data = request.FILES
    admin_user = AdminUser.objects.get(username__exact=user)
    if AdminUser.objects.filter(username__exact=user).exists() and admin_user.Active:
        # admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedInUser = admin_user.Name
        if admin_user.Active and admin_admin:
            if 'csrfmiddlewaretoken' in post_data:
                name_of_the_contest = post_data['contest_name']
                photo_of_the_contest = file_data['contest_photo']
                page_id = post_data['page_id']
                album_id = post_data['album_id']
                new_contest = ContestPanel(ContestName=name_of_the_contest, ContestImage=photo_of_the_contest,
                                           PageID=page_id, AlbumID=album_id)
                new_contest.save()
                display = redirect('/home')
        else:
            logout(request)
            display = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login.'
                                      ' Please contact administrator for more details'})
    else:
        display = redirect('/home')
    return display


@login_required(login_url='/admin/')
def contest_list(request):
    user = request.session['user']

    if AdminUser.objects.filter(username__exact=user).exists():
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedInUser = admin_user.Name
        if admin_user.Active:
            all_contests_list = ContestPanel.objects.all()
            display = render(request, 'contest_list.html',
                             {'all_contests_list': all_contests_list,
                              'loggedInUser': loggedInUser,
                              'page_title': 'List Of Contests',
                              'admin_admin': admin_admin})
        else:
            logout(request)
            display = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login.'
                                      ' Please contact administrator for more details'})
    else:
        display = redirect('/home')
    return display


@login_required(login_url='/admin/')
def change_contest_status(request):
    user = request.session['user']
    if AdminUser.objects.filter(username__exact=user).exists():
        get_data = request.GET
        contest_id = get_data['id']
        selected_contest = ContestPanel.objects.get(id=contest_id)
        if selected_contest.Active:
            selected_contest.Active = False
        else:
            all_contests = ContestPanel.objects.all()
            for every_contest in all_contests:
                every_contest.Active = False
                every_contest.save()
            selected_contest.Active = True
        selected_contest.save()
        display = redirect('/contest_list')
    else:
        display = redirect('/home')
    return display


@login_required(login_url='/admin/')
def show_images(request):
    user = request.session['user']
    if AdminUser.objects.filter(username__exact=user).exists():
        get_data = request.GET
        admin_user = AdminUser.objects.get(username__exact=user)
        loggedInUser = admin_user.Name
        contest_id = get_data['contest_id']
        selected_contest = ContestPanel.objects.get(id=contest_id)
        all_images = ContestImage.objects.filter(Contest=selected_contest)
        display = render(request, 'gallery.html', {'loggedInUser': loggedInUser,
                                                   'page_title': 'Album',
                                                   'all_images': all_images,
                                                   'contest_id': contest_id})
    else:
        display = redirect('/home')
    return display



@login_required(login_url='/admin/')
def add_admin(request):
    user = request.session['user']
    if not AdminUser.objects.exists():
        print(request.session['user'])
        new_admin = AdminUser(username=user, Name=user, Email=user+'@inflack.com', Admin=True)
        new_admin.save()
    # if admin
    if AdminUser.objects.filter(username__exact=user).exists():
        admin = True
        admin_user = AdminUser.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        loggedInUser = admin_user.Name
        if admin_user.Active:
            if admin_admin:
                display = render(request, 'add_admin.html', {'admin': admin,
                                                             'loggedInUser': loggedInUser,
                                                             'page_title': 'Add An Admin',
                                                             'admin_admin': admin_admin})
            else:
                display = render(request, 'access_denied.html', {'admin': admin,
                                                                 'loggedInUser': loggedInUser,
                                                                 'admin_admin': admin_admin})
        else:
            logout(request)
            display = render(request, 'admin_login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        display = redirect('/home')
    return display


@login_required(login_url='/login/')
def add_admin_info(request):
    user = request.session['user']
    post_data = request.POST
    # print(post_data['super-admin'])
    if not AdminUser.objects.exists():
        print(request.session['user'])
        new_admin = AdminUser(username=user, Name=user, Email=user+'@inflack.com', Admin=True)
        new_admin.save()
    if 'username' in post_data and 'csrfmiddlewaretoken' in post_data:
        # if admin
        if AdminUser.objects.filter(username__exact=user).exists():
            admin = True
            admin_user = AdminUser.objects.get(username__exact=user)
            admin_admin = admin_user.Admin
            loggedInUser = admin_user.Name
            if admin_user.Active and admin_admin:
                if AdminUser.objects.filter(username__exact=post_data['username']).exists():
                    display = render(request, 'add_admin.html',
                                     {'wrong': True,
                                      'text': 'Username already taken. Please try with a different username.',
                                      'admin': admin,
                                      'loggedInUser': loggedInUser,
                                      'admin_admin': admin_admin})
                else:
                    if post_data['re-password'] == post_data['password']:
                        new_admin_username = post_data['username']
                        new_admin_name = post_data['name']
                        new_admin_phone = post_data['phone']
                        new_admin_email = post_data['email']
                        new_admin_super_admin = True
                        new_admin_password = post_data['password']
                        new_added_admin = AdminUser(username=new_admin_username,
                                                    Name=new_admin_name,
                                                    Email=new_admin_email,
                                                    Admin=new_admin_super_admin,
                                                    Phone=new_admin_phone)
                        new_added_admin.save()
                        new_user = User.objects.create_user(new_admin_username,
                                                            new_admin_email,
                                                            new_admin_password)
                        new_user.save()
                        display = render(request, 'add_admin.html',
                                         {'wrong': True,
                                          'loggedInUser': loggedInUser,
                                          'text': 'The new user is added successfully',
                                          'admin': admin,
                                          'admin_admin': admin_admin})
                    else:
                        display = render(request, 'add_admin.html',
                                         {'wrong': True,
                                          'loggedInUser': loggedInUser,
                                          'text': 'Passwords do not match. Please Try Again.',
                                          'admin': admin,
                                          'admin_admin': admin_admin})
            else:
                logout(request)
                display = render(request, 'login.html',
                                 {'wrong': True,
                                  'text': 'You are not authorized to login.'
                                          ' Please contact administrator for more details'})
        else:
            display = redirect('/')
    else:
        display = redirect('/add_admin/')
    return display


@login_required(login_url='/admin/')
def change_admin_status(request):
    user = request.session['user']
    if AdminUser.objects.filter(username__exact=user).exists():
        get_data = request.GET
        admin_id = get_data['id']
        selected_admin = AdminUser.objects.get(id=admin_id)
        if selected_admin.Active:
            selected_admin.Active = False
        else:
            selected_admin.Active = True
        selected_admin.save()
        display = redirect('/home')
    else:
        display = redirect('/home')
    return display


from fblib import facebook
import urllib2
import json


@login_required(login_url='/admin/')
def upload_photo(request):
    user = request.session['user']
    post_data = request.POST
    uid = post_data['uid']
    auth = post_data['auth']
    cid = post_data['cid']
    contest = ContestPanel.objects.get(id=cid)
    album = contest.AlbumID
    # print(album)
    pageid = contest.PageID
    # print(pageid)
    info_url = 'https://graph.facebook.com/v2.2/' + uid + '/accounts/?access_token=' + auth
    # info_url = 'https://graph.facebook.com/v2.2/me/accounts/?access_token=' + auth
    print(info_url)
    if info_url == 'https://graph.facebook.com/v2.2//accounts/?access_token=':
        display = redirect('/show_images/?contest_id='+cid)
    else:
        response = urllib2.urlopen(info_url)
        info_raw = response.read()
        info = json.loads(info_raw)
        for page in info['data']:
            # print(page['id'])
            if page['id'] == pageid:
                at = page['access_token']
                graph = facebook.GraphAPI(access_token=at)
                if AdminUser.objects.filter(username__exact=user).exists():

                    i = 0
                    # print(post_data)
                    for item in post_data:
                        if item != 'csrfmiddlewaretoken' and item != 'uid' and item != 'auth' and item != 'cid':
                            print(item)
                            pic = ContestImage.objects.get(id=post_data[item])
                            caption = str(pic.NameOfTheContestant) + ' : ' + str(pic.CaptionOfThePhoto)
                            picULR = 'inflack.net:8001/media/' + str(pic.PhotoOfTheContestant)
                            graph.put_photo(image=open("/var/www/static/media/" + str(pic.PhotoOfTheContestant)),
                                            album_path=str(album), album=str(album), message=caption)
                            # print(picULR)
                            pic.Published = True
                            pic.save()
        display = redirect('/show_images/?contest_id='+cid)
    return display
