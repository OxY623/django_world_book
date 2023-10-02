from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    '''Универсальный класс представления списка книг,
    находящихся в заказе у текуего пользователя'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user). \
            filter(status__exact='2').order_by('due_back')


def index(request):
    '''Главная страница'''
    # Генерация количеств обьектов
    # Книги
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Книги со статусом на складе
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    # Авторы книг
    num_authors = Author.objects.all().count()
    # Количество посещений этого view
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    # Create HTML templates here
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 3


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4


# Получение данных из БД
# Загрузка шаблона authots_add.html

def author_add(request):
    author = Author.objects.all()
    authorsform =  AuthorsForm()
    return render(request, "catalog/author_add.html", {"form": authorsform, "author" : author} )

# Добавление автора
def create_author(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_death = request.POST.get('date_of_death')

        author = Author(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            date_of_death=date_of_death
        )

        author.save()

        return HttpResponseRedirect('/author_add/')


# Удаление автора


def delete_author(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect('/author_add/')
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")


# Изменеие данных об Авторе
# def edit_author(request, id):
#     author = Author.objects.get(id=id)
#     if request.method == 'POST':
#         author.first_name = request.POST.get('first_name')
#         author.last_name = request.POST.get('last_name')
#         author.date_of_birth = request.POST.get('date_of_birth')
#         author.date_of_death = request.POST.get('date_of_death')
#         author.save()
#         return HttpResponseRedirect('author_add')
#         #return redirect('authors_add')
#     else:
#         return render(request, 'catalog/edit1.html', {'author': author})
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Author


def edit_author(request, id):
    author = Author.objects.get(id=id)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        date_of_death = request.POST['date_of_death']

        author.first_name = first_name
        author.last_name = last_name
        author.date_of_birth = date_of_birth
        author.date_of_death = date_of_death
        author.save()

        return redirect('author_add')

    context = {'author': author}
    return render(request, 'catalog/edit1.html', context)

class BookCreateView(CreateView):
    model = Book
    fields  = '__all__'
    success_url = reverse_lazy('books')

class BookUpdateView(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

