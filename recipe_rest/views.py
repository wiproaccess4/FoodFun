from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import action
from recipe.models import Recipe
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import RecipeSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RecipeApiView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        print(request.user)
        recipes = Recipe.objects.all()#values("id", "recipe_name", "ingredients")
        ser_obj = RecipeSerializer(recipes, many=True)
        return Response(ser_obj.data)
        # return Response(recipes)

    def put(self, request):
        if not request.data.get("recipe_id") or not request.data.get("name"):
            return Response({"message": "Not a valid request"}, status=status.HTTP_400_BAD_REQUEST)
        recipe_id = request.data["recipe_id"]
        name = request.data["name"]
        recipe_obj = Recipe.objects.get(id=recipe_id)
        recipe_obj.recipe_name = name
        recipe_obj.save()
        return Response({"message": "Successfully Updated"})

    def post(self, request):
        serializer_obj = RecipeSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        return Response({"message": serializer_obj.errors})


class UserApiView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({"message": "Successfully Logged out"})


class RecipeViewset(viewsets.ViewSet):
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    @action(methods=["GET"], detail=False)
    def get_recipes(self, request):
        recipes = list(Recipe.objects.values("id", "recipe_name", "ingredients"))
        return Response(recipes)

    @action(methods=["GET"], detail=False)
    def get_recipe_by_name(self, request):
        recipes = list(Recipe.objects.filter(recipe_name=request.GET.get("name")).values("id", "recipe_name", "ingredients"))
        return Response(recipes)

    @action(methods=["GET", "POST"], detail=False)
    def recipe(self, request):
        if request.method == "GET":
            recipes = list(Recipe.objects.filter(id=request.data.get("id")).values("id", "recipe_name", "ingredients"))
            return Response(recipes)
        elif request.method == "POST":
            recipes = list(Recipe.objects.filter(id=request.data.get("id")).values("id", "recipe_name", "ingredients"))
            return Response(recipes)
