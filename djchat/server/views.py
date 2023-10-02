from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import viewsets
from .models import Server
from .serializers import ServerSerializer
from rest_framework.response import Response
from django.db.models import Q
from django.db.models import Count
from .schema import server_list_docs


class ServerListViewSet(viewsets.ViewSet):
    """
    A ViewSet for interacting with Server objects.
    Provides list functionality with optional filters and quantity limit.

    Attributes:
        queryset (QuerySet): The initial queryset to include all servers.

    Methods:
        list(request):
            Get a list of servers with optional filters based on category, user, and quantity.

    """

    queryset = Server.objects.all()  # Set the initial queryset to include all servers.

    @server_list_docs
    def list(self, request):
        """
        Get a list of servers with optional filters based on category, user, and quantity.

        Args:
            request (Request): The request object containing optional query parameters.

        Returns:
            Response: Serialized data of servers based on applied filters and quantity.

        Raises:
            AuthenticationFailed: If 'by_user' filter is requested but the user is not authenticated.
            ValidationError: If there's a validation error in the provided filters.

            Notes:
            - This method allows the following optional query parameters:
              - 'category' (str): Filters servers based on a specified category.
              - 'quantity' (int): Limits the number of servers returned.
              - 'by_user' (bool): Filters servers by the authenticated user.
              - 'by_server_id' (int): Filters servers by a specific server ID.
              - 'with_num_members' (bool): Includes the number of members for each server.

        """

        # Rest of the existing code...

        # Retrieve optional query parameters for filtering and quantity.
        category = request.query_params.get("category")
        quantity = request.query_params.get("quantity")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Apply filtering based on category if specified.
        if category:
            self.queryset = self.queryset.filter(
                Q(category__name__icontains=category)
                | Q(category__id__icontains=category)
            )

        # Apply filtering based on user if 'by_user' filter is requested.
        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(
                    detail="You should authenticate first to access the filter"
                )

        # Annotate the queryset with the number of members if 'with_num_members' filter is requested.
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Limit the queryset based on the requested quantity.
        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        # Filter the queryset based on server ID if specified.
        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"server with id {by_server_id} not found"
                    )
            except ValueError:
                raise ValidationError(detail="Server value error.")

        # Serialize the queryset and return the serialized data as a response.
        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
