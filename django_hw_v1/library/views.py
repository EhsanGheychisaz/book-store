import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from .forms import BookSearchForm
from .models import Book, Borrow, Category


@csrf_exempt
def home_view(request):
    if request.method == "GET":
        return render(request, "home_page.html", status=200)
    else:
        return HttpResponse("Method Not Allowed!", status=405)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        required_params = {"username", "password"}
        if not required_params.issubset(data.keys()):
            return HttpResponse("Missing required parameters", status=400)
        if set(data.keys()) != required_params:
            return HttpResponse("Unexpected parameters found", status=400)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse("User has been Logged in Successfully.", status=200)
        else:
            return HttpResponse("User Not Found!", status=404)
    else:
        return HttpResponse("Method Not Allowed!", status=405)


@csrf_exempt
def search_view(request):
    if request.method == "GET":
        search_form = BookSearchForm(request.GET)
        if search_form.is_valid():
            name = search_form.cleaned_data.get("name")
            author = search_form.cleaned_data.get("author")
            category = search_form.cleaned_data.get("category")
            available_only = search_form.cleaned_data.get("available_only")
        else:
            return HttpResponse("Bad Request!", status=400)
        books = Book.objects.all()
        if name:
            books = books.filter(name__icontains=name)
        if author:
            books = books.filter(author__icontains=author)
        if category:
            categories = Category.objects.filter(name__icontains=category)
            books = books.filter(categories__in=categories)
        if available_only:
            books = books.filter(count__gt=0)
        books = books.order_by("name", "author")
        books_data = []
        for book in books:
            book_data = {
                "name": book.name,
                "author": book.author,
                "available": book.count,
            }
            books_data.append(book_data)
        return JsonResponse({"books": books_data}, status=200)
    else:
        return HttpResponse("Method Not Allowed!", status=405)


@csrf_exempt
def book_search_view(request):
    return redirect("search")


@csrf_exempt
def book_return_view(request):
    if request.user.is_authenticated:
        if request.method == "DELETE":
            data = json.loads(request.body)
            required_params = {"name", "author"}
            if not required_params.issubset(data.keys()):
                return HttpResponse("Missing required parameters", status=400)
            if set(data.keys()) != required_params:
                return HttpResponse("Unexpected parameters found", status=400)
            name = data.get("name")
            author = data.get("author")
            borrowed_book = Borrow.objects.filter(
                book__name__icontains=name,
                book__author__icontains=author,
                user=request.user,
            ).first()
            if borrowed_book:
                the_book = Book.objects.filter(
                    name__icontains=name, author__icontains=author
                ).first()
                the_book.count += 1
                the_book.save()
                borrowed_book.delete()
                return HttpResponse(
                    "The Book has been Retured Successfully.", status=200
                )
            else:
                return HttpResponse("The Borrowed Book Not Found!", status=404)
        else:
            return HttpResponse("Method Not Allowed!", status=405)
    else:
        return HttpResponse("Unauthorized!", status=401)
