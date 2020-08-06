from django.shortcuts import render
from .models import Author, Recipe

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
