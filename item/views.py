from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item
# Create your views here.
# Function to display a list of items
def items(request):
    # Retrieve all items from the database
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
     # Render the items template and pass the items as context
    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

# Function to display details of a specific item
def detail(request, pk):
    # Retrieve the item 
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
        # Render the detail template and pass the item as context
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })


# Function to create a new item
@login_required
def new(request):
    if request.method == 'POST':
        # Retrieve the data submitted in the form
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            # Create a new item object with the retrieved data
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            # Redirect to the items list page
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
        # Render the new item form template
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })


# Function to edit an existing item
@login_required
def edit(request, pk):
    # Retrieve the item based on the provided ID
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        # Retrieve the updated data submitted in the form
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            # Update the item object with the new data
            form.save()
            # Redirect to the item detail page
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
            # Render the edit item form template and pass the item as context
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

# Function to delete an item
@login_required
def delete(request, pk):
    # Retrieve the item based on the provided ID
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    # Delete the item from the database
    item.delete()
    
    # Render the delete confirmation template and pass the item as context
    return redirect('dashboard:index')
