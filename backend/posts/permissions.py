from rest_framework.permissions import BasePermission
from .models import UserProvinceAccess

class HasProvinceAccess(BasePermission):
    message = "شما به این استان دسترسی ندارید."

    def has_object_permission(self, request, view, obj):
        # اجازه ببینیم کاربر به استان obj دسترسی دارد
        return UserProvinceAccess.objects.filter(
            user=request.user,
            province=obj.province
        ).exists()

    def has_permission(self, request, view):
        # برای لیست یا ایجاد جدید، دسترسی به استان‌های مجاز چک شود
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return True  # منطق فیلتر در View انجام می‌شود
        return False