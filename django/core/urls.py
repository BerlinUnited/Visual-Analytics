from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema


# this is required to protect the graphql endpoint
class LoginRequiredMiddleware:
    def resolve(self, next, root, info, **args):
        if info.context.user.is_anonymous:
            raise Exception("Authentication credentials were not provided.")
        return next(root, info, **args)


urlpatterns = [
    path("", include("user.urls")),
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                graphiql=True, schema=schema, middleware=[LoginRequiredMiddleware()]
            )
        ),
    ),
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("common.urls")),
    path("api/", include("cognition.urls")),
    path("api/", include("motion.urls")),
    path("api/", include("image.urls")),
    path("api/", include("behavior.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
