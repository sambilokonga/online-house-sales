from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from item.models import Item

# Create your views here.

@login_required
def index(request):
        """
    View function for the index page.

    Returns:
        A rendered HTML response.
    """

    items = Item.objects.filter(created_by=request.user)
    # Render the template 
    return render(request, 'dashboard/index.html', {
        'items': items,
    })
