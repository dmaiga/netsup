from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
 

from sites.models import Site
from controles.models import ControleSite

from users.models import User
from users.forms import UserForm

def redirect_dashboard(user):

    if user.role == "superviseur":
        return "dashboard_superviseur"

    if user.role in ["admin", "direction"]:
        return "dashboard_admin"

    return "login"

def login_view(request):

    if request.method == "POST":

        telephone = request.POST.get("telephone")
        password = request.POST.get("password")

        user = authenticate(request, telephone=telephone, password=password)

        if user is not None:

            if not user.is_active:
                messages.error(request, "Compte désactivé")
                return redirect("login")

            login(request, user)

            return redirect(redirect_dashboard(user))

        else:
            messages.error(request, "Téléphone ou mot de passe incorrect")

    return render(request, "users/auth/login.html")


def logout_view(request):

    logout(request)

    return redirect("login")

@login_required
def dashboard_admin(request):

    return render(request, "users/dashboard/admin.html")




@login_required
def dashboard_superviseur(request):

    total_sites = Site.objects.filter(actif=True).count()

    total_controles = ControleSite.objects.filter(
        superviseur=request.user
    ).count()

    last_controles = ControleSite.objects.filter(
        superviseur=request.user
    ).order_by("-date")[:5]

    context = {

        "total_sites": total_sites,
        "total_controles": total_controles,
        "last_controles": last_controles

    }

    return render(request, "users/dashboard/superviseur.html",context)


def user_list(request):

    users = User.objects.filter(is_deleted=False)

    return render(request, "users/list.html", {"users": users})

 
def user_detail(request, pk):

    user = get_object_or_404(User, pk=pk)

    return render(request, "users/detail.html", {
        "user": user
    })

 
def user_create(request):

    if request.method == "POST":

        form = UserForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save(commit=False)

            password = form.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()

            return redirect("user_list")

    else:

        form = UserForm()

    return render(request, "users/create.html", {"form": form})
 
def user_update(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():

            user = form.save(commit=False)

            password = form.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()

            return redirect("user_list")

    else:

        form = UserForm(instance=user)

    return render(request, "users/create.html", {
        "form": form,
        "user": user
    })

 
def user_toggle_active(request, pk):

    user = User.objects.get(pk=pk)

    user.is_active = not user.is_active

    user.save()

    return redirect("user_list")
 
def user_soft_delete(request, pk):

    user = User.objects.get(pk=pk)

    user.is_deleted = True
    user.is_active = False

    user.save()

    return redirect("user_list")