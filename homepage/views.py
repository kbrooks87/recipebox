from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Author, Recipe
from .forms import AddAuthor, AddRecipe

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
    return render(request, 'generic_form.html', {'form':form})


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
    return render(request, 'generic_form.html', {'form':form})

