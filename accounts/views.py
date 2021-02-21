from django.shortcuts import render,redirect
from django.contrib import  messages
from .forms import RegistrationForm,LoginForm
from django.contrib.auth  import login,authenticate,logout





def register(request):
    user= request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created !')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



def LogoutView(request):
    logout(request)
    return redirect('login')

'''def LoginView(request, *args, **kwargs):
    context= {}
    user = request.user
    if user.is_authenticated:
        return redirect('register')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data('email')
            password = form.cleaned_data('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['form'] = LoginForm()
    return render(request, 'accounts/login.html', context)

def get_redirect_if_exists(request):
    redirect= None
    if request.GET:
        if request.GET.get('next'):
            redirect (request.GET.get("next"))
    return redirect'''














