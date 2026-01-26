# LibraryProject

This is an introductory Django project created to learn Django setup, project structure, and running the development server.

## Permissions and Groups Setup

This project implements custom permissions and groups to control access.

### Custom Permissions
The following permissions are defined in the Article model:
- can_view
- can_create
- can_edit
- can_delete

### Groups
The following groups can be created via Django Admin:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

### Permission Enforcement
Views are protected using Django's permission_required decorator to ensure
only authorized users can access specific actions.

## Security Best Practices

This project demonstrates Django security best practices.

### Secure Settings
- DEBUG is set to False.
- Browser protections enabled:
  - SECURE_BROWSER_XSS_FILTER
  - SECURE_CONTENT_TYPE_NOSNIFF
  - X_FRAME_OPTIONS
- Cookies secured using:
  - CSRF_COOKIE_SECURE
  - SESSION_COOKIE_SECURE

### CSRF Protection
- All HTML forms include the {% csrf_token %} tag.

### SQL Injection Prevention
- Django ORM is used instead of raw SQL.
- User input is validated using Django Forms and cleaned_data.

### Content Security Policy (CSP)
- A Content-Security-Policy header is applied to restrict content sources.

These measures protect against XSS, CSRF, and SQL Injection attacks.

## HTTPS and Secure Redirects Configuration

This project enforces HTTPS to ensure secure communication between clients and the server.

### HTTPS Enforcement
- `SECURE_SSL_REDIRECT = True` ensures all HTTP requests are redirected to HTTPS.
- HTTP Strict Transport Security (HSTS) is enabled:
  - `SECURE_HSTS_SECONDS = 31536000`
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
  - `SECURE_HSTS_PRELOAD = True`

These settings instruct browsers to only access the site via HTTPS.

### Secure Cookies
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`

This ensures cookies are only transmitted over HTTPS connections.

### Secure HTTP Headers
- `X_FRAME_OPTIONS = 'DENY'` prevents clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` prevents MIME-type sniffing.
- `SECURE_BROWSER_XSS_FILTER = True` enables browser XSS protection.

### Deployment Notes
In a production environment, HTTPS should be configured at the web server level
(e.g., Nginx or Apache) using valid SSL/TLS certificates such as those provided
by Let's Encrypt.

