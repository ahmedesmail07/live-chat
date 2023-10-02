from rest_framework import serializers
from .models import Channel, Server


# Define a serializer for the Channel model.
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"  # Include all fields from the Channel model.


# Define a serializer for the Server model.
class ServerSerializer(serializers.ModelSerializer):
    channel_server = ChannelSerializer(
        many=True
    )  # Serialize related channels for the server.
    num_members = (
        serializers.SerializerMethodField()
    )  # Custom serializer method field for num_members.

    class Meta:
        model = Server
        exclude = ("member",)  # Exclude the 'member' field from serialization.

    # Custom method to get the number of members for a server.
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        else:
            return None

    # Override the to_representation method to customize the serialized representation of the instance.
    def to_representation(self, instance):
        data = super().to_representation(
            instance
        )  # Call the parent class's to_representation method.
        num_members = self.context.get(
            "num_members"
        )  # Get the 'num_members' from the context.

        # Remove the 'num_members' field from the serialized data if 'num_members' is not requested.
        if not num_members:
            data.pop("num_members", None)
        return data  # Return the modified serialized data.
