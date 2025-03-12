from .models import Category, Municipality

def common_data(request):
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()
    return {
        'categories': categories,
        'locations': locations,
    }