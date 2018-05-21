from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, \
    update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UserProfileForm, UserForm, StrongPasswordChangeForm


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too. "
                "Now you can create a profile."
            )
            return HttpResponseRedirect(reverse('accounts:edit'))
        else:
            print(form.errors)
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required(login_url='/accounts/sign_in/')
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user})
    else:
        return render(request, 'home.html')


@login_required(login_url='/accounts/sign_in/')
def edit(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST,
                             instance=request.user)
        profile_form = UserProfileForm(data=request.POST,
                                       instance=request.user.userprofile,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return HttpResponseRedirect(reverse('home'))
        else:
            # TODO make these display correctly instead of a UL
            messages.error(request, user_form.errors)
            messages.error(request, profile_form.errors)
            return HttpResponseRedirect(reverse('accounts:edit'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/edit_profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'user': request.user})


@login_required(login_url='/accounts/sign_in/')
def change_password(request):
    form = StrongPasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = StrongPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,
                             'Password changed successfully')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request,
                           'Password not changed')
    return render(request, 'accounts/change_password.html', {'form': form})


