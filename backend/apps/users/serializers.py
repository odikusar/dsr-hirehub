from rest_framework import serializers

from apps.users.models import User


# Serializer = validation + JSON<->model conversion (like a Zod schema + mapper).
# ModelSerializer generates fields/validation from the model (incl. email uniqueness).
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "role"]
        extra_kwargs = {
            # write_only: accepted as input, never returned in responses.
            "password": {"write_only": True},
            # read_only: client can't set their own role (mass assignment protection).
            "role": {"read_only": True},
        }

    # Default create() would store the raw password; create_user() hashes it.
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# Read-only serializer: different use case, different field set.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
