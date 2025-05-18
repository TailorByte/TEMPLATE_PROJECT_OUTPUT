from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Module, Role, UserRole, RolePermission, AccessLevel

User = get_user_model()

class PermissionModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password')
        self.module1 = Module.objects.create(module_name='test_module', display_name='Test Module')
        self.role1 = Role.objects.create(role_name='Test Role')

    def test_module_creation(self):
        self.assertEqual(self.module1.display_name, 'Test Module')
        self.assertEqual(str(self.module1), 'Test Module')

    def test_role_creation(self):
        self.assertEqual(self.role1.role_name, 'Test Role')
        self.assertEqual(str(self.role1), 'Test Role')

    def test_user_role_assignment(self):
        user_role = UserRole.objects.create(user=self.user1, role=self.role1)
        self.assertEqual(user_role.user, self.user1)
        self.assertEqual(user_role.role, self.role1)
        self.assertEqual(str(user_role), f"{self.user1.email} - {self.role1.role_name}")
        self.assertEqual(UserRole.objects.filter(user=self.user1, role=self.role1).count(), 1)

    def test_role_permission_creation(self):
        role_perm = RolePermission.objects.create(
            role=self.role1,
            module=self.module1,
            access_level=AccessLevel.EDIT
        )
        self.assertEqual(role_perm.role, self.role1)
        self.assertEqual(role_perm.module, self.module1)
        self.assertEqual(role_perm.access_level, AccessLevel.EDIT)
        self.assertEqual(str(role_perm), f"{self.role1.role_name} - {self.module1.display_name}: Edit Access")

    def test_unique_user_role(self):
        UserRole.objects.create(user=self.user1, role=self.role1)
        with self.assertRaises(Exception): # IntegrityError or similar
            UserRole.objects.create(user=self.user1, role=self.role1)

    def test_unique_role_permission(self):
        RolePermission.objects.create(role=self.role1, module=self.module1, access_level=AccessLevel.VIEW)
        with self.assertRaises(Exception): # IntegrityError or similar
            RolePermission.objects.create(role=self.role1, module=self.module1, access_level=AccessLevel.EDIT)

# Add API tests for permission-related endpoints when views are implemented.
# Add tests for the ModulePermission class logic.