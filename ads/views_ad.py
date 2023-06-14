import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from homework import settings
from user.models import User


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        data_ad = self.object_list.order_by('-price')

        paginator = Paginator(data_ad, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        all_ads = []
        for ad in page_obj:
            all_ads.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": str(User.objects.get(pk=ad.author_id)),
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
                "category_id": ad.category_id,
            })

        response = {
            "items": all_ads,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "is_published", "category_id", "image"]

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)
        ads = Ad.objects.create(
            name=ads_data['name'],
            author_id=ads_data.get("author_id"),
            price=ads_data['price'],
            description=ads_data['description'],
            is_published=ads_data['is_published'],
            category_id=ads_data.get("category_id")
        )

        return JsonResponse({
            "name": ads.name,
            "author": str(User.objects.get(pk=ads.author_id)),
            "author_id": ads.author_id,
            "price": ads.price,
            "description": ads.description,
            "is_published": ads.is_published,
            "image": ads.image if ads.image else None,
            "category_id": ads.category_id,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "is_published", "category_id", "image"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ads_data = json.loads(request.body)

        if ads_data['name'] is not None:
            self.object.name = ads_data['name']
        if ads_data.get("author_id"):
            self.object.author_id = ads_data.get("author_id")
        if ads_data.get("category_id"):
            self.object.category_id = ads_data.get("category_id")
        if ads_data['price'] is not None:
            self.object.price = ads_data['price']
        if ads_data['description'] is not None:
            self.object.description = ads_data['description']

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": str(User.objects.get(pk=self.object.author_id)),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        }, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": str(User.objects.get(pk=self.object.author_id)),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        }, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": str(User.objects.get(pk=self.object.author_id)),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, safe=False, json_dumps_params={'ensure_ascii': False})