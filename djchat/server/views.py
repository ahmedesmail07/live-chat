from rest_framework import viewsets
from .models import Server
from .serializers import ServerSerializer
from rest_framework.response import Response
from django.db.models import Q


class ServerListViewSet(viewsets.ViewSet):
    """
    A ViewSet for interacting with Server objects.

    Provides list functionality with optional filters and quantity limit.
    """

    queryset = Server.objects.all()

    def list(self, request):
        """
        Get a list of servers with optional filters based on category, user, and quantity.

        Args:
            request (Request): The request object.

        Returns:
            Response: Serialized data of servers based on applied filters and quantity.
        """
        category = request.query_params.get("category")
        quantity = request.query_params.get("quantity")
        by_user = request.query_params.get("by_user") == "true"

        if category:
            self.queryset = self.queryset.filter(
                Q(category__name__icontains=category)
                | Q(category__id__icontains=category)
            )

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
