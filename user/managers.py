from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_user(self, email: str = None, password: str = None,
                    is_staff: bool = False, is_superuser: bool = False) -> "User":
        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("password is required")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_superuser(self, email: str = None, password: str = None) -> "User":
        return self.create_user(email=email, password=password, is_staff=True, is_superuser=True)
