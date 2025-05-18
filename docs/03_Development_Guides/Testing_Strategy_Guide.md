# Testing Strategy Guide

This document outlines the testing strategy for projects following this template, covering both backend (Django) and frontend (React) applications. A comprehensive testing strategy is essential for ensuring code quality, reliability, and maintainability.

## 1. Goals of Testing

*   **Verify Correctness:** Ensure the application behaves as expected according to requirements and specifications.
*   **Prevent Regressions:** Catch bugs introduced by new code or modifications to existing code.
*   **Improve Code Quality:** Writing testable code often leads to better design and modularity.
*   **Facilitate Refactoring:** Confidence to refactor code knowing that tests will catch regressions.
*   **Documentation:** Tests serve as a form of executable documentation, illustrating how components and functions are intended to be used.
*   **Reduce Manual Testing Effort:** Automate repetitive testing tasks.

## 2. Testing Pyramid

We aim to follow the principles of the testing pyramid:

*   **Unit Tests (Base - Most Numerous):**
    *   Focus: Test individual functions, methods, classes, or components in isolation.
    *   Speed: Fast.
    *   Scope: Smallest unit of code.
*   **Integration Tests (Middle):**
    *   Focus: Test the interaction between multiple components, modules, or services.
    *   Speed: Moderate.
    *   Scope: Interactions between units (e.g., API endpoint with database, multiple React components).
*   **End-to-End (E2E) Tests (Top - Fewest):**
    *   Focus: Test complete user flows through the entire application stack (UI, API, database).
    *   Speed: Slow.
    *   Scope: Entire application from the user's perspective.

## 3. Backend Testing (Django & DRF)

### 3.1. Tools

*   **Django's Test Framework:** Built on Python's `unittest` module. Provides `TestCase`, `TransactionTestCase`, test client, etc.
*   **Pytest with `pytest-django`:** A popular alternative offering a more concise syntax and powerful features (fixtures, plugins).
*   **Factory Boy (`factory_boy`):** For creating test data fixtures efficiently.
*   **Faker:** For generating realistic fake data.
*   **Coverage.py:** For measuring test coverage.
*   **DRF Test Utilities:** DRF provides `APITestCase`, `APIClient`, and other helpers for testing API views.

### 3.2. Unit Tests

*   **Models (`models.py`):**
    *   Test custom model methods, properties, and `save()` method overrides.
    *   Test model validation logic (e.g., `clean()` method).
    *   Test `__str__` representations.
    *   Example:
        ```python
        # myapp/tests/test_models.py
        from django.test import TestCase
        from myapp.models import MyModel
        from myapp.factories import MyModelFactory # Using factory_boy

        class MyModelTests(TestCase):
            def test_my_custom_method(self):
                instance = MyModelFactory(some_field="initial_value")
                self.assertEqual(instance.my_custom_method(), "expected_result")

            def test_str_representation(self):
                instance = MyModelFactory(name="Test Instance")
                self.assertEqual(str(instance), "Test Instance")
        ```
*   **Forms (`forms.py`):**
    *   Test form validation (valid and invalid data).
    *   Test form cleaning methods (`clean_<field>`, `clean()`).
    *   Test form saving logic if applicable.
*   **Serializers (`serializers.py` - DRF):**
    *   Test serialization (object to data) and deserialization (data to object).
    *   Test validation rules (`validate_<field>`, `validate()`).
    *   Test read-only/write-only fields.
    *   Test nested serializers.
*   **Utility Functions/Services (`utils.py`, `services.py`):**
    *   Test pure functions with various inputs and edge cases.
    *   Mock external dependencies if necessary.
*   **Custom Managers (`managers.py`):**
    *   Test custom queryset methods.

### 3.3. Integration Tests

*   **API Views/ViewSets (`views.py` - DRF):**
    *   Use `APIClient` or `APITestCase` to make requests to your API endpoints.
    *   Test:
        *   Correct status codes for different scenarios (200, 201, 204, 400, 401, 403, 404).
        *   Response data structure and content.
        *   Authentication and permission enforcement.
        *   Filtering, sorting, and pagination.
        *   Create, retrieve, update, delete (CRUD) operations.
        *   Custom actions.
    *   Example:
        ```python
        # myapp/tests/test_views.py
        from rest_framework.test import APITestCase
        from rest_framework import status
        from django.urls import reverse
        from myapp.models import MyModel
        from myapp.factories import MyModelFactory, UserFactory

        class MyModelAPITests(APITestCase):
            def setUp(self):
                self.user = UserFactory() # Create a test user
                self.client.force_authenticate(user=self.user) # Authenticate client
                self.list_url = reverse('mymodel-list') # Assuming 'mymodel' is basename for router

            def test_list_mymodels(self):
                MyModelFactory.create_batch(3)
                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data['results']), 3)

            def test_create_mymodel(self):
                data = {'name': 'New Model', 'description': 'A test description.'}
                response = self.client.post(self.list_url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(MyModel.objects.count(), 1)
                self.assertEqual(MyModel.objects.get().name, 'New Model')
        ```
*   **Interactions between Services/Modules:**
    *   Test scenarios where different parts of your backend interact (e.g., a service calling another service, signals).

### 3.4. Test Organization

*   Place tests in a `tests/` directory within each app (e.g., `myapp/tests/`) or in a single `tests.py` file for simpler apps.
*   Use descriptive file names (e.g., `test_models.py`, `test_views.py`, `test_forms.py`).
*   Use descriptive class and method names for tests (e.g., `TestUserModel`, `test_user_can_be_created_successfully`).

## 4. Frontend Testing (React)

### 4.1. Tools

*   **Jest:** Test runner, assertion library, and mocking capabilities. Often included with `create-react-app`.
*   **React Testing Library (RTL):** For testing React components by interacting with them as a user would. Focuses on accessibility and user behavior.
*   **User Event (`@testing-library/user-event`):** Companion to RTL for simulating realistic user interactions.
*   **MSW (Mock Service Worker):** For mocking API requests at the network level, allowing for more realistic integration tests without hitting a real backend.
*   **Storybook:** For developing UI components in isolation and documenting component states and use cases. Can also be used for visual regression testing.
*   **Cypress / Playwright:** For E2E testing.

### 4.2. Unit Tests

*   **Utility Functions (`utils.js`):**
    *   Test pure functions with various inputs and edge cases.
*   **Custom Hooks (`hooks/useMyHook.js`):**
    *   Use `@testing-library/react-hooks` (or RTL's `renderHook` for newer versions) to test the behavior of custom hooks.
*   **Simple Presentational Components:**
    *   Test that the component renders correctly based on different props.
    *   Verify text content, presence of elements, and attributes.
    *   Example:
        ```jsx
        // src/components/Button/Button.test.js
        import { render, screen } from '@testing-library/react';
        import userEvent from '@testing-library/user-event';
        import Button from './Button';

        describe('Button', () => {
          test('renders with correct text', () => {
            render(<Button>Click Me</Button>);
            expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
          });

          test('calls onClick handler when clicked', async () => {
            const handleClick = jest.fn();
            render(<Button onClick={handleClick}>Click Me</Button>);
            await userEvent.click(screen.getByRole('button', { name: /click me/i }));
            expect(handleClick).toHaveBeenCalledTimes(1);
          });
        });
        ```

### 4.3. Integration Tests

*   **Components with State/Logic:**
    *   Test how components behave when users interact with them (e.g., filling forms, clicking buttons that trigger state changes).
    *   Verify that the UI updates correctly in response to interactions.
*   **Components Interacting with Context/Global State:**
    *   Wrap components with necessary Context providers in your tests.
    *   Verify that components consume and update context/global state correctly.
*   **Components Making API Calls (Mocked):**
    *   Use MSW or Jest mocks (`jest.mock`) to mock API responses.
    *   Test loading states, error handling, and successful data display.
    *   Example with MSW:
        ```jsx
        // src/features/UserProfile/UserProfile.test.js
        import { render, screen, waitFor } from '@testing-library/react';
        import { rest } from 'msw';
        import { setupServer } from 'msw/node';
        import UserProfile from './UserProfile';

        const server = setupServer(
          rest.get('/api/user/:userId', (req, res, ctx) => {
            return res(ctx.json({ id: req.params.userId, name: 'John Doe' }));
          })
        );

        beforeAll(() => server.listen());
        afterEach(() => server.resetHandlers());
        afterAll(() => server.close());

        test('loads and displays user data', async () => {
          render(<UserProfile userId="1" />);
          expect(screen.getByText(/loading/i)).toBeInTheDocument();
          await waitFor(() => expect(screen.getByText(/john doe/i)).toBeInTheDocument());
        });
        ```

### 4.4. Test Organization

*   Co-locate test files with the components or modules they are testing (e.g., `Button.test.js` next to `Button.jsx`).
*   Use `__tests__` subdirectories if preferred.

## 5. End-to-End (E2E) Tests

*   **Tools:** Cypress, Playwright.
*   **Focus:** Test critical user flows from start to finish (e.g., user registration, placing an order, searching for a product).
*   **Strategy:**
    *   Identify key user paths.
    *   Write tests that mimic real user scenarios.
    *   Keep E2E tests focused on high-level functionality; avoid testing UI details already covered by component tests.
    *   Run E2E tests in a CI/CD pipeline, ideally against a staging environment.

## 6. Test Coverage

*   **Goal:** Aim for a reasonable level of test coverage, but focus on quality over quantity. High coverage of critical paths and complex logic is more important than 100% coverage of trivial code.
*   **Tools:** `coverage.py` (Django), Jest's built-in coverage (React).
*   **Review:** Regularly review coverage reports to identify untested areas.

## 7. CI/CD Integration

*   **Automation:** Integrate tests into your CI/CD pipeline (e.g., GitHub Actions, GitLab CI, Jenkins).
*   **Gating:** Fail builds if tests do not pass.
*   **Reporting:** Configure CI to report test results and coverage.

## 8. General Best Practices

*   **Write Tests First (TDD - Optional but Encouraged):** Consider Test-Driven Development for new features.
*   **Independent Tests:** Tests should not depend on each other or the order in which they are run.
*   **Fast Tests:** Keep unit tests fast. Slow tests discourage frequent running.
*   **Readable Tests:** Tests should be easy to understand. Use clear naming and structure.
*   **Deterministic Tests:** Tests should produce the same result every time they are run (avoid flakiness).
*   **Test Edge Cases and Error Conditions:** Don't just test the "happy path."
*   **Refactor Tests:** Just like production code, tests should be refactored to maintain clarity and efficiency.
*   **Don't Test Third-Party Libraries:** Assume external libraries are already tested. Focus on testing your integration with them.

---
*This testing strategy provides a framework. Adapt it to your project's specific needs, team skills, and available resources.*