from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from .models import Author, Recipe
from .forms import AddAuthor, AddRecipe, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    recipes= Recipe.objects.all()
    return render(request, 'index.html', {'recipes':recipes})


def recipe(request, recipe_id):
    recipedetail= Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe.html', {'recipedetail':recipedetail})


def author(request, author_id):
    authordetail= Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_id)
    return render(request,'author.html', {'authordetail':authordetail, 'recipes':recipes})

@login_required
def add_author(request):
    if request.user.is_staff:

        if request.method == 'POST':
            form = AddAuthor(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get('username'), password=data.get('password'))
                Author.objects.create(name=data.get('username'), user=new_user, bio=data.get('bio'))
                login(request, new_user)

                return HttpResponseRedirect(reverse('homepage'))
    else:
        return render(request, 'noaccess.html')
    form = AddAuthor()
    return render(request, 'generic_form.html', {'form':form})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipe(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=request.user.author,
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions')
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = AddRecipe()
    return render(request, 'generic_form.html', {'form':form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))
    form=LoginForm()
    return render(request, 'generic_form.html', {'form':form})  


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
    

        

