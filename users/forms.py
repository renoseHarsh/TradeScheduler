from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Common Tailwind class for all fields
        common_classes = "block w-full px-3 py-2 border bg-gray-200 border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"

        # Apply the Tailwind classes to each field
        self.fields["username"].widget.attrs.update({"class": common_classes})
        self.fields["password1"].widget.attrs.update({"class": common_classes})
        self.fields["password2"].widget.attrs.update({"class": common_classes})


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    error_messages = {
        "invalid_login": "Invalid username or password",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Common Tailwind class for all fields
        common_classes = "block w-full px-3 py-2 border bg-gray-200 border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"

        # Apply the Tailwind classes to each field
        self.fields["username"].widget.attrs.update({"class": common_classes})
        self.fields["password"].widget.attrs.update({"class": common_classes})
