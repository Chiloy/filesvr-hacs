from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from pam.forms import UserPasswordHideForm
from pam.models import PamUsers


# Create your views here.
def create_user(request):
    if request.method == 'POST':
        form = UserPasswordHideForm(request.POST)
        if form.is_valid():
            article = form.save()  # 自动保存到数据库
            return redirect('/success/')
    else:
        form = UserPasswordHideForm()

    return render(request, 'pam/user_form.html', {'form': form})


def update_user(request, pk):
    user = PamUsers.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserPasswordHideForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=pk)
    else:
        form = UserPasswordHideForm(instance=user)

    return render(request, 'pam/user_form.html', {'form': form})