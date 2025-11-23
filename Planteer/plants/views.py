from django.shortcuts import render ,redirect
from .models import Plant , Review ,Country

from .forms import PlantForm 



# Create your views here.
def plants_add_view(request):
    countries=Country.objects.all()
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            plant.countries.set(request.POST.getlist("countries"))
            return redirect('main:home_view')
    else:
        form = PlantForm()

    return render(request, 'plants/add_plant.html', {'form': form,'countries': countries})



def plants_detail_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant_id)[:3]
    reviews=Review.objects.filter(plant=plant)

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'related_plants': related_plants ,"reviews":reviews
    })

def plants_update_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    countries = Country.objects.all()

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)

        if form.is_valid():

            plant.name = request.POST.get("name")
            plant.about = request.POST.get("about")
            plant.used_for = request.POST.get("used_for")
            plant.category = request.POST.get("category")
            plant.is_edible = "is_edible" in request.POST

            if "image" in request.FILES:
                plant.image = request.FILES["image"]

            plant.save()
            plant.countries.set(request.POST.getlist("countries"))


            return redirect("plants:plants_detail_view", plant_id=plant_id)

    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/plants_update.html", {
        "plant": plant,
        "form": form,
        "countries": countries,
    })




def plants_delet_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    plant.delete()
    return redirect('main:home_view')


def plants_search_view(request):
    query = request.GET.get("search")
    plants = []

    if query:
        plants = Plant.objects.filter(name__icontains=query)

    return render(request, "plants/plants_search.html", {'plants': plants, 'query': query}) 

def plants_list_view(request):
    plants = Plant.objects.all()
    countries = Country.objects.all()
    categories = Plant.CategoryChoices

    # Search
    search_query = request.GET.get("search")
    if search_query:
        plants = plants.filter(name__icontains=search_query)

    # Filter by category
    category_filter = request.GET.get("category")
    if category_filter and category_filter != "ALL":
        plants = plants.filter(category=category_filter)

    # Filter by country
    country_filter = request.GET.get("country")
    if country_filter and country_filter != "ALL":
        plants = plants.filter(countries__id=country_filter)

    plants = plants.distinct()  # important for m2m filtering
    count = plants.count()

    return render(request, "plants/plants_list.html", {
        "plants": plants,
        "count": count,
        "countries": countries,
        "categories": categories,
    })

def add_review_view(request,plant_id):
    if request.method == "POST":
        plant_odject=Plant.objects.get(pk=plant_id)
        new_review=Review(plant=plant_odject,name=request.POST.get("name"),comment=request.POST.get("comment"))
        new_review.save()

    return redirect("plants:plants_detail_view",plant_id=plant_id)

def plants_country_view(request, country_id):
    country = Country.objects.get(id=country_id)
    plants = Plant.objects.filter(countries=country)  
    count = plants.count()

    return render(request, 'plants/plants_country.html', {
        'country': country,
        'plants': plants,
        'count': count
    })
