from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 요청한 사용자와 게시물의 작성자가 같은지 확인
        return obj.writer == request.user
