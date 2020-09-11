from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Author, Recipe
from .forms import AddAuthor, AddRecipe, LoginForm

# Create your views here.
def index(request):
    recipes= Recipe.objects.all()
    return render(request, 'index.html', {'recipes':recipes})


def recipe(request, recipe_id):
    recipedetail= Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe.html', {'recipedetail': recipedetail})


def author(request, author_id):
    authordetail= Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_id)
    favorite_recipes = request.Author.favorites.all()
    return render(request,'author.html', {'authordetail': authordetail, 'recipes': recipes, 'favorites': favorite_recipes})


def add_author(request):
    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio')
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = AddAuthor()
    return render(request, 'generic_form.html', {'form': form})


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipe(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions')
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = AddRecipe()
    return render(request, 'generic_form.html', {'form': form})

@login_required
def favorites_view(request, recipe_id):
    current_user = request.user.author
    target_recipe = Recipe.objects.get(id=recipe_id)
    current_user.favorites.add(target_recipe)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def recipe_edit_view(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  if request.user.author.id == recipe.author.id or request.user.is_staff:
    if request.method == "POST":
        form = AddRecipe(request.POST)
        if form.is_valid():
            recipe_data = form.cleaned_data
            recipe.title = recipe_data['title']
            recipe.description = recipe_data['description']
            recipe.time_required = recipe_data['time_required']
            recipe.instructions = recipe_data['instructions']
            recipe.save()
        return HttpResponseRedirect(reverse('recipe', args=[recipe.id]))
    data = {
        'title': recipe.title,
        'description': recipe.description,
        'time_required': recipe.time_required,
        'instructions': recipe.instructions,
    }
    form = AddRecipe(initial=data)
    return render(request, 'generic_form.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("homepage"))

    form = LoginForm()
    return render(request, 'generic_form.html', {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))

