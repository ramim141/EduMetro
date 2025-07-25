# notes/admin.py
from django.contrib import admin

from .models import Note, StarRating, Comment, Department, Course, NoteCategory,NoteRequest, Faculty, Contributor

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'email',  'id')

    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id') 
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'id')
    list_filter = ('department',)
    search_fields = ('name', 'department__name')

@admin.register(NoteCategory)
class NoteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uploader',
        'category',
        'course',
        'department',
        'faculty',
        'semester',
        'download_count',
        'average_rating',
        'is_approved',
        'created_at',
        'updated_at'
    )
    list_filter = ('category', 'department', 'faculty','course', 'semester', 'uploader', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'tags__name', 'uploader__username', 'category__name', 'course__name', 'department__name', 'faculty__name', 'semester' )
    readonly_fields = ('average_rating', 'download_count', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'uploader', 'description', 'file', 'is_approved')
        }),
        ('Categorization', {
            'fields': ('category', 'faculty', 'course', 'department', 'semester', 'tags') 
        }),
        ('Analytics (Read-Only)', {
            'fields': ('download_count', 'average_rating'),
            'classes': ('collapse',)
        }),
        ('Timestamps (Read-Only)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StarRating)
class StarRatingAdmin(admin.ModelAdmin):
    list_display = ('note_title', 'user_username', 'stars', 'created_at')
    list_filter = ('stars', 'user', 'note__department__name', 'created_at')
    search_fields = ('note__title', 'user__username', 'note__department__name')
    readonly_fields = ('created_at', 'updated_at')

    def note_title(self, obj):
        return obj.note.title
    note_title.short_description = 'Note Title'
    note_title.admin_order_field = 'note__title'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'
    user_username.admin_order_field = 'user__username'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('note_title', 'user_username', 'comment_summary', 'created_at')
    list_filter = ('user', 'note__department__name', 'created_at')
    search_fields = ('note__title', 'user__username', 'text', 'note__department__name')
    readonly_fields = ('created_at', 'updated_at')

    def note_title(self, obj):
        return obj.note.title
    note_title.short_description = 'Note Title'
    note_title.admin_order_field = 'note__title'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'
    user_username.admin_order_field = 'user__username'

    def comment_summary(self, obj):
        if obj.text:
            return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
        return "-"
    comment_summary.short_description = 'Comment'



@admin.register(NoteRequest)
class NoteRequestAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'user', 'department_name', 'status', 'created_at')
    list_filter = ('status', 'department_name', 'created_at')
    list_editable = ('status',) 
    search_fields = ('course_name', 'department_name', 'user__username', 'user__student_id')
    readonly_fields = ('user', 'course_name', 'department_name', 'message', 'created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return self.readonly_fields



@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'batch_with_section', 'note_contribution_count', 'average_star_rating', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__batch', 'user__section')
    readonly_fields = ('user', 'note_contribution_count', 'average_star_rating', 'updated_at')

    @admin.display(description='Batch & Section')
    def batch_with_section(self, obj):
        user = obj.user
        if user.batch and user.section:
            return f"{user.batch}({user.section})"
        elif user.batch:
            return user.batch
        return "N/A"
    def has_add_permission(self, request):
        return False