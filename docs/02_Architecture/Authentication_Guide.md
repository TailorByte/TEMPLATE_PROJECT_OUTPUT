# Authentication Guide (JWT-based)

This document outlines the standard approach for implementing JSON Web Token (JWT) based authentication for projects following this template.

## 1. Overview

Authentication is the process of verifying the identity of a user, device, or system. For stateless web applications and APIs, JWT is a common and effective method.

**JWT Flow:**

1.  **Login:** The user submits credentials (e.g., username/password) to an authentication endpoint.
2.  **Verification:** The server verifies the credentials.
3.  **Token Generation:** If credentials are valid, the server generates two JWTs:
    *   **Access Token:** A short-lived token (e.g., 5-15 minutes) used to authorize access to protected resources.
    *   **Refresh Token:** A longer-lived token (e.g., 7-30 days) used to obtain new access tokens without requiring the user to re-enter credentials.
4.  **Token Storage (Client):**
    *   **Access Token:** Typically stored in memory (e.g., JavaScript variable, React state).
    *   **Refresh Token:** Stored securely, often in an HTTP-only cookie to prevent XSS attacks, or in secure local storage (less ideal but common for mobile).
5.  **Authenticated Requests:** The client includes the Access Token in the `Authorization` header (e.g., `Authorization: Bearer <access_token>`) for requests to protected API endpoints.
6.  **Token Validation (Server):** The server validates the Access Token's signature, expiration, and claims on each request.
7.  **Token Refresh:**
    *   If the Access Token expires, the client sends the Refresh Token to a dedicated refresh endpoint.
    *   The server validates the Refresh Token. If valid, it issues a new Access Token (and potentially a new Refresh Token for sliding sessions).
    *   If the Refresh Token is invalid or expired, the user must re-authenticate.
8.  **Logout:**
    *   Client-side: Discard the Access Token from memory and remove the Refresh Token from storage.
    *   Server-side (optional but recommended for enhanced security): Implement a token blocklist or denylist to invalidate active refresh tokens upon logout.

## 2. JWT Structure

A JWT consists of three parts separated by dots (`.`):

*   **Header:** Contains metadata about the token, such as the token type (`JWT`) and the signing algorithm (e.g., `HS256`, `RS256`).
    ```json
    {
      "alg": "HS256",
      "typ": "JWT"
    }
    ```
*   **Payload:** Contains the claims (statements about an entity, typically the user, and additional data).
    *   **Registered Claims:** Standard claims (e.g., `iss` (issuer), `exp` (expiration time), `sub` (subject), `aud` (audience)).
    *   **Public Claims:** Custom claims defined by your application, should be collision-resistant (e.g., namespaced or registered with IANA).
    *   **Private Claims:** Custom claims shared between parties that agree on using them.
    ```json
    {
      "sub": "user123", // User ID
      "username": "john.doe",
      "roles": ["user", "editor"], // Example custom claim
      "exp": 1678886400, // Expiration timestamp
      "iat": 1678882800  // Issued at timestamp
    }
    ```
    **Note:** Do not store sensitive information in the JWT payload as it is only base64 encoded, not encrypted.
*   **Signature:** Used to verify that the sender of the JWT is who it says it is and to ensure that the message wasn't changed along the way. It's created by signing the encoded header, the encoded payload, a secret (for symmetric algorithms like HS256) or a private key (for asymmetric algorithms like RS256), using the algorithm specified in the header.

## 3. Implementation Details (Django & DRF Simple JWT)

For Django projects, `djangorestframework-simplejwt` is a highly recommended library.

*   **Installation:**
    ```bash
    pip install djangorestframework-simplejwt
    ```
*   **Configuration (`settings.py`):**
    ```python
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        )
    }

    from datetime import timedelta

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15), # Adjust as needed
        'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Adjust as needed
        'ROTATE_REFRESH_TOKENS': True, # Issues a new refresh token when an old one is used
        'BLACKLIST_AFTER_ROTATION': True, # Adds the old refresh token to a blacklist
        'UPDATE_LAST_LOGIN': True,

        'ALGORITHM': 'HS256', # Ensure this matches your security requirements
        'SIGNING_KEY': SECRET_KEY, # Use your project's SECRET_KEY or a dedicated one
        # 'VERIFYING_KEY': None, # Only for asymmetric algorithms
        # 'AUDIENCE': None,
        # 'ISSUER': None,
        # 'JWK_URL': None,
        # 'LEEWAY': 0,

        'AUTH_HEADER_TYPES': ('Bearer',),
        'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
        'USER_ID_FIELD': 'id', # Or 'user_id' depending on your User model
        'USER_ID_CLAIM': 'user_id',
        'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM': 'token_type',
        'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

        'JTI_CLAIM': 'jti',

        # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
        # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
        # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    }
    ```
*   **URLs (`urls.py`):**
    ```python
    from django.urls import path
    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
        TokenVerifyView, # Optional: for client-side token verification
    )

    urlpatterns = [
        # ... your other urls
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), # Optional
    ]
    ```
*   **Customizing Token Claims (Optional):**
    You can customize the claims included in the JWT by subclassing `TokenObtainPairSerializer` and `TokenObtainPairView`.
    ```python
    # In your app's serializers.py
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)

            # Add custom claims
            token['username'] = user.username
            token['email'] = user.email
            # ... any other claims

            return token

    # In your app's views.py
    from rest_framework_simplejwt.views import TokenObtainPairView
    from .serializers import MyTokenObtainPairSerializer

    class MyTokenObtainPairView(TokenObtainPairView):
        serializer_class = MyTokenObtainPairSerializer
    ```
    Then update your `urls.py` to use `MyTokenObtainPairView`.

## 4. Client-Side Handling (React Example)

*   **Storing Tokens:**
    *   Access Token: In React state (e.g., Context API, Redux, Zustand).
    *   Refresh Token: In an HTTP-only cookie (set by the server) or secure local storage.
*   **Making Authenticated Requests (using Axios):**
    ```javascript
    import axios from 'axios';

    const apiClient = axios.create({
      baseURL: '/api', // Your API base URL
    });

    apiClient.interceptors.request.use(
      (config) => {
        const accessToken = localStorage.getItem('accessToken'); // Or get from state
        if (accessToken) {
          config.headers['Authorization'] = `Bearer ${accessToken}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
    ```
*   **Handling Token Expiry and Refresh:**
    Implement an Axios interceptor to handle 401 errors (token expired) and attempt to refresh the token.
    ```javascript
    // (Continuing from above apiClient setup)

    let isRefreshing = false;
    let failedQueue = [];

    const processQueue = (error, token = null) => {
      failedQueue.forEach(prom => {
        if (error) {
          prom.reject(error);
        } else {
          prom.resolve(token);
        }
      });
      failedQueue = [];
    };

    apiClient.interceptors.response.use(
      (response) => {
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest._retry) {
          if (isRefreshing) {
            return new Promise(function(resolve, reject) {
              failedQueue.push({ resolve, reject });
            }).then(token => {
              originalRequest.headers['Authorization'] = 'Bearer ' + token;
              return apiClient(originalRequest);
            }).catch(err => {
              return Promise.reject(err);
            });
          }

          originalRequest._retry = true;
          isRefreshing = true;

          const refreshToken = localStorage.getItem('refreshToken'); // Or get from cookie
          if (!refreshToken) {
            // Handle logout: redirect to login, clear user state
            console.error("No refresh token available.");
            isRefreshing = false;
            // window.location.href = '/login'; // Example redirect
            return Promise.reject(error);
          }

          try {
            const rs = await axios.post('/api/token/refresh/', {
              refresh: refreshToken,
            });

            const { access } = rs.data;
            localStorage.setItem('accessToken', access); // Update access token
            // If your backend rotates refresh tokens and sends a new one in the refresh response:
            // if (rs.data.refresh) { localStorage.setItem('refreshToken', rs.data.refresh); }

            apiClient.defaults.headers.common['Authorization'] = 'Bearer ' + access;
            originalRequest.headers['Authorization'] = 'Bearer ' + access;
            processQueue(null, access);
            return apiClient(originalRequest);
          } catch (_error) {
            processQueue(_error, null);
            // Handle logout: redirect to login, clear user state
            console.error("Refresh token failed or expired.", _error);
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            // window.location.href = '/login'; // Example redirect
            return Promise.reject(_error);
          } finally {
            isRefreshing = false;
          }
        }
        return Promise.reject(error);
      }
    );

    export default apiClient;
    ```
    **Note:** The above client-side refresh logic is a common pattern. Adjust paths and storage mechanisms as per your setup.

## 5. Security Considerations

*   **HTTPS:** Always use HTTPS in production to protect tokens in transit.
*   **Secret Key Strength:** Use a strong, unique `SECRET_KEY` for signing tokens (HS256). For RS256, protect your private key diligently.
*   **Token Expiration:** Keep Access Token lifetimes short. Refresh Token lifetimes can be longer but should be balanced with security risks.
*   **Refresh Token Rotation:** Rotate refresh tokens upon use to mitigate the risk of a compromised refresh token being used indefinitely.
*   **Token Blocklisting/Denylisting:** Implement a mechanism to invalidate tokens (especially refresh tokens) upon logout, password change, or suspected compromise. `djangorestframework-simplejwt` supports this via its `outstanding_token` and `blacklist` apps.
*   **XSS Prevention:** If storing refresh tokens in local storage, be vigilant against XSS. HTTP-only cookies are generally safer for web applications.
*   **CSRF Protection:** While JWTs themselves are not inherently vulnerable to CSRF if used correctly (e.g., in Authorization headers), ensure your application's non-API parts (if any) that use sessions/cookies have CSRF protection.
*   **Algorithm Choice:**
    *   `HS256` (HMAC with SHA-256) uses a single shared secret. Simpler to set up.
    *   `RS256` (RSA with SHA-256) uses a public/private key pair. Allows the authentication server to sign tokens with a private key, and resource servers to verify with a public key without needing the private key. More complex but can be more secure in distributed systems.
*   **Audience (`aud`) and Issuer (`iss`) Claims:** Use these claims if your tokens are intended for specific audiences or issued by a specific authority, especially in microservice architectures.

## 6. Logout

*   **Client-Side:**
    *   Remove the Access Token from memory/state.
    *   Remove the Refresh Token from its storage (HTTP-only cookie or local storage).
    *   Redirect the user to the login page or update UI to reflect logged-out state.
*   **Server-Side (Recommended):**
    *   If using `djangorestframework-simplejwt`'s blacklist feature:
        1.  Create an endpoint that accepts a refresh token.
        2.  When this endpoint is called, add the provided refresh token to the blacklist.
        ```python
        # Example logout view
        from rest_framework.views import APIView
        from rest_framework.response import Response
        from rest_framework import status
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework.permissions import IsAuthenticated

        class LogoutView(APIView):
            permission_classes = (IsAuthenticated,)

            def post(self, request):
                try:
                    refresh_token = request.data["refresh"]
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                    return Response(status=status.HTTP_205_RESET_CONTENT)
                except Exception as e:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        ```
        Add this view to your `urls.py`. The client would call this endpoint upon logout.

---
*This guide provides a foundational approach. Always adapt to specific project requirements and stay updated on security best practices.*