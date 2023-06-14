import json

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from homework import settings
from ads.models import Ad, Category
from user.models import User, Location


def database_content(request):
    with open('json_data/category.json', 'r') as json_file:
        data = json.load(json_file)
        for item in data:
            obj1 = Category(name=item['name'])
            obj1.save()

    return HttpResponse(status=200)


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            ad_amount = Ad.objects.filter(author_id=user.id).count()
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "locations": [
                    str(Location.objects.get(pk=int(user.location_id)))
                ] if not user.added_by_user else [user.location_id],
                "total_ads": ad_amount,
            })

        response = {
            "items": users,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id", "added_by_user"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'],
            location_id=", ".join(user_data.get("locations")),
            added_by_user=True
        )
        user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "locations": [user.location_id],
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        if user_data['first_name'] is not None:
            self.object.first_name = user_data['first_name']
        if user_data['last_name'] is not None:
            self.object.last_name = user_data['last_name']
        if user_data['username'] is not None:
            self.object.username = user_data['username']
        if user_data['password'] is not None:
            self.object.password = user_data['password']
        if user_data['role'] is not None:
            self.object.role = user_data['role']
        if user_data['age'] is not None:
            self.object.age = user_data['age']
        if user_data.get('locations'):
            self.object.location_id = user_data.get("locations")
        self.object.added_by_user = True

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [
                str(Location.objects.get(pk=int(self.object.location_id)))
            ] if not self.object.added_by_user else [self.object.location_id]
        }, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ad_amount = Ad.objects.filter(author_id=self.object.id).count()
        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [
                str(Location.objects.get(pk=int(self.object.location_id)))
            ] if not self.object.added_by_user else [self.object.location_id],
            "total_ads": ad_amount
        }, safe=False, json_dumps_params={'ensure_ascii': False})
