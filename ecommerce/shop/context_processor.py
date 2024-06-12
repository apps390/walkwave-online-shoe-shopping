from shop.models import Sub_category


def men_category(request):
        men_link = Sub_category.objects.filter(category__category_name="Men's Collections")
        return {'men_link': men_link}

def women_category(request):
        wom_link = Sub_category.objects.filter(category__category_name="Women's Collections")
        return {'wom_link': wom_link}

def kids_category(request):
        kids_link = Sub_category.objects.filter(category__category_name="Kid's Collections")
        return {'kids_link': kids_link }


