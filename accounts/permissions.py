from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission class untuk memastikan user memiliki role ADMIN.
    Digunakan untuk endpoint-endpoint admin seperti list users, view user detail, dll.
    """
    
    message = "Anda tidak memiliki akses admin. Hanya admin yang bisa mengakses endpoint ini."
    
    def has_permission(self, request, view):
        # User harus authenticated dan memiliki role ADMIN
        return (
            request.user 
            and request.user.is_authenticated 
            and hasattr(request.user, 'role')
            and request.user.role == 'ADMIN'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class untuk memastikan user adalah owner dari object atau admin.
    Digunakan untuk endpoint yang hanya boleh diakses owner atau admin.
    """
    
    message = "Anda tidak memiliki akses ke data ini."
    
    def has_object_permission(self, request, view, obj):
        # Admin bisa akses semua data
        if hasattr(request.user, 'role') and request.user.role == 'ADMIN':
            return True
        
        # Owner bisa akses data sendiri
        # Cek apakah object memiliki field 'user'
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Jika object adalah User instance
        if obj == request.user:
            return True
        
        return False
