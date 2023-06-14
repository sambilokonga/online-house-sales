from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from item.models import Category, Item

from .forms import SignupForm
# Create your views here.

def index(request):
        """
    View function for the index page.

    Returns:
        A rendered HTML response.
    """

    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })
def contact(request):
        """
    View function for the contact page.

    Returns:
        A rendered HTML response.
    """

    return render(request, 'core/contact.html')

def signup(request):
        """
    View function for user registration.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML response.
    """

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            # Create a new user account
            # Save the user to the database

            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })


def logout(request):
        """
    View function for user logout.

    Args:
        request: The HTTP request object.

    Returns:
        A redirected response.
    """

    auth.logout(request)
    return redirect('/')
