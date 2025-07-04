from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")


class CustomAPIViewSetMixin:
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="type",
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by page type (e.g., blog.BlogPage).",
                type=str,
                examples=[OpenApiExample("Example type", value="blog.BlogPage")],
            ),
            OpenApiParameter(
                name="fields",
                required=False,
                location=OpenApiParameter.QUERY,
                description="Comma-separated list of fields to include in the response.",
                type=str,
                examples=[
                    OpenApiExample("Example fields", value="published_date,body")
                ],
            ),
            OpenApiParameter(
                name="slug",
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by page slug (e.g., about).",
                type=str,
                examples=[OpenApiExample("Example slug", value="about")],
            ),
            OpenApiParameter(
                name="child_of",
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by parent page ID to get direct children of that page.",
                type=int,
                examples=[OpenApiExample("Example child_of", value=1)],
            ),
            OpenApiParameter(
                name="offset",
                required=False,
                location=OpenApiParameter.QUERY,
                description="The starting position of the results (pagination).",
                type=int,
                examples=[OpenApiExample("Example offset", value=20)],
            ),
            OpenApiParameter(
                name="limit",
                required=False,
                location=OpenApiParameter.QUERY,
                description="The maximum number of results to return (pagination).",
                type=int,
                examples=[OpenApiExample("Example limit", value=20)],
            ),
            OpenApiParameter(
                name="order",
                required=False,
                location=OpenApiParameter.QUERY,
                description="The ordering of the results. Use field names prefixed with '-' for descending order.",
                type=str,
                examples=[OpenApiExample("Example ordering", value="title,-slug")],
            ),
        ]
    )
    def listing_view(self, request):
        return super().listing_view(request)


class CustomPagesAPIViewSet(CustomAPIViewSetMixin, PagesAPIViewSet):
    pass


class CustomImagesAPIViewSet(CustomAPIViewSetMixin, ImagesAPIViewSet):
    pass


class CustomDocumentsAPIViewSet(CustomAPIViewSetMixin, DocumentsAPIViewSet):
    pass


# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint("pages", CustomPagesAPIViewSet)
api_router.register_endpoint("images", CustomImagesAPIViewSet)
api_router.register_endpoint("documents", CustomDocumentsAPIViewSet)
