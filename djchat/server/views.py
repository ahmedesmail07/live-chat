from rest_framework import viewsets
from .models import Server
from .serializers import ServerSerializer
from rest_framework.response import Response


class ServerListViewSet(viewsets.ViewSet):
    # Initialize the queryset with all Server objects
    queryset = Server.objects.all()

    def list(self, request):
        # Get the 'category' parameter from the request's query parameters
        category = request.query_params.get("category")

        # Check if 'category' parameter is provided in the request
        if category:
            # Filter the queryset based on the 'category' parameter by name
            self.queryset = self.queryset.filter(category__name__icontains=category)

        # Serialize the filtered queryset to prepare the response data
        serializer = ServerSerializer(self.queryset, many=True)

        # Return a Response containing the serialized data
        return Response(serializer.data)
