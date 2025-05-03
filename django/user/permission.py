from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBerlinUnited(BasePermission):
    """
    Permission class to check if a user's organization matches a specific value.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # check if user is member of berlin_united
        return (
            request.user.organization
            and request.user.organization.name == "berlin_united"
        )


class IsBerlinUnitedOrReadOnly(BasePermission):
    """
    Allows authenticated users to retrieve data and BU Users to modify data
    Returns:
        True -> Request is allowed
        False -> Request is not allowed
    """

    def has_permission(self, request, view):
        # request.user is the user django could authenticate with by provided
        # authentication methods
        # if no authentication method is provided the user is AnonymousUser
        """
        # For debugging
        print(f"\n--- Permission Check ---")
        print(f"User: {request.user} (Authenticated: {request.user.is_authenticated})")
        print(request.user.organization)
        print(f"Method: {request.method}")
        print(f"View action: {view.action}")
        """
        # user.is_authenticated is always true if user is VAT_User and false if user is AnonymousUser
        # this only happens if user provides no authentication, invalid authentication like wrong passwords or tokens are blocked somewhere else
        if not request.user.is_authenticated:
            return False

        # for authenticated users we allow methods that don't change data
        if request.method in SAFE_METHODS:
            return True

        # check if user is member of berlin_united
        # would throw an error if user has no organization attribute

        if request.user.organization is None:
            return False
        return request.user.organization.name == "berlin_united"
