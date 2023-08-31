from django.urls import path

from blog.views import BlogTableView, UsersTableView, UserDetailView, BlogListView, BlogGridView

app_name = 'blog'
urlpatterns = [
    path("blog/table/", BlogTableView.as_view(), name="blog-table"),
    path("blog/list/", BlogListView.as_view(), name="blog-list"),
    path("blog/grid/", BlogGridView.as_view(), name="blog-grid"),

    path("users/", UsersTableView.as_view(), name="users-table"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-details"),
    path("users/<int:pk>/<str:listing_type>/", UserDetailView.as_view(), name="user-inner"),
]
