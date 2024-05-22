from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from decorators import access_permission, capture_exception_logs
from usermanagement.models import AccountType
from .models import Book
from .pagination import paginate_query


@login_required(login_url="login")
@capture_exception_logs
def home(request):
    context = {}
    return render(request, "bookmanagement/home.html", context)


@login_required(login_url="login")
@access_permission([AccountType.LIBRARIAN])
@capture_exception_logs
def book_inventory(request):
    context = {}
    all_books = Book.objects.all().order_by("-id")
    context["books"] = paginate_query(all_books, items_per_page=20, page_num=request.GET.get("page", 1))
    return render(request, "bookmanagement/book_inventory.html", context)


@login_required(login_url="login")
@access_permission([AccountType.LIBRARIAN])
@capture_exception_logs
def create_book(request):
    context = {}
    if request.method == "POST":
        title: str = request.POST.get("title")
        try:
            Book.objects.get(title=title)
        except ObjectDoesNotExist:
            Book.objects.create(title=request.POST["title"], author=request.POST["author"], genre=request.POST["genre"])
            return redirect("bookmanagement:home")
        context["error"] = "Book with given title already exists"
    return render(request, "bookmanagement/create_book.html", context)


@login_required(login_url="login")
@access_permission([AccountType.LIBRARIAN])
@capture_exception_logs
def read_and_update_book(request, book_id: str):
    context = {}
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title").lower()
        book.author = request.POST.get("author")
        book.genre = request.POST.get("genre")
        book.save()

    context["book"] = book
    return render(request, "bookmanagement/book.html", context)


@login_required(login_url="login")
@access_permission([AccountType.END_USER])
@capture_exception_logs
def book_borrow_list(request):
    context = {}
    return render(request, "bookmanagement/book_borrow_list.html", context)


@login_required(login_url="login")
@access_permission([AccountType.END_USER])
@capture_exception_logs
def borrow_book(request):
    context = {}
    available_books = Book.objects.filter(borrowed_by__isnull=True)
    context["books"] = available_books
    return render(request, "bookmanagement/borrow_book.html", context)
