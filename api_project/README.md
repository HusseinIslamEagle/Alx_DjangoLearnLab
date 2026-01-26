## Authentication and Permissions (DRF)

This API uses Django REST Framework Token Authentication.

### Authentication
- Token authentication is enabled using `rest_framework.authtoken`.
- Users can obtain a token via:
  POST /api/token/

### Permissions
- API views are protected using `IsAuthenticated`.
- Only authenticated users can access or modify Book resources.

### Usage
Include the token in request headers:
Authorization: Token <your_token_here>
