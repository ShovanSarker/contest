from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from contest_panel.models import ContestImage, ContestPanel
# Create your views here.


@csrf_exempt
def contest_page(request):
    contest_running = ContestPanel.objects.filter(Active=True).exists()

    return render(request, 'ContestPage.html', {'contest_running': contest_running})


@csrf_exempt
def contest_page1(request):
    return render(request, 'test.html')


@csrf_exempt
def get_info(request):
    post_data = request.POST
    file_data = request.FILES
    # print(post_data)
    # print(file_data)
    running_contest = ContestPanel.objects.get(Active=True)
    new_contest_image = ContestImage(Contest=running_contest,
                                     NameOfTheContestant=post_data['NameOfTheContestant'],
                                     EmailOfTheContestant=post_data['EmailOfTheContestant'],
                                     PhoneOfTheContestant=post_data['PhoneOfTheContestant'],
                                     FBLinkOfTheContestant=post_data['FBLinkOfTheContestant'],
                                     ProfessionOfTheContestant=post_data['ProfessionOfTheContestant'],
                                     InstituteOfTheContestant=post_data['InstituteOfTheContestant'],
                                     PhotoOfTheContestant=file_data['PhotoOfTheContestant'],
                                     CaptionOfThePhoto=post_data['CaptionOfThePhoto'])
    new_contest_image.save()
    running_contest.NumberOfPhotos += 1
    running_contest.save()
    return redirect('/')




