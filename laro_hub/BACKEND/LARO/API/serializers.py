from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer handles the conversion of User model instances to/from JSON format.
    
    Features:
    - Converts User model data to JSON for API responses
    - Validates incoming JSON data for user creation/updates
    - Handles password hashing during user creation and updates
    - Ensures passwords are write-only and never included in responses
    
    Fields:
    - id: User's unique identifier
    - firstname: User's first name
    - lastname: User's last name
    - middlename: User's middle name (optional)
    - email: User's email address (used for authentication)
    - password: User's password (write-only)
    """
    
    class Meta:
        model = User
        fields = ["id", "firstname", "lastname", "middlename", "email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures password is never included in responses
        }

    def create(self, validated_data):
        """
        Creates a new user instance with a hashed password.
        
        This method overrides the default create to ensure passwords are properly
        hashed using Django's password hashing system via create_user().
        
        Args:
            validated_data: Dictionary of validated user data from the request
            
        Returns:
            Newly created User instance
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            middlename=validated_data.get('middlename', '')
        )
        return user

    def update(self, instance, validated_data):
        """
        Updates an existing user instance.
        
        Handles password updates separately to ensure proper hashing.
        All other fields are updated normally.
        
        Args:
            instance: Existing User instance to update
            validated_data: Dictionary of validated user data from the request
            
        Returns:
            Updated User instance
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)