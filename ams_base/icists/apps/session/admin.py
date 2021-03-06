from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from icists.apps.session.models import University, UserProfile
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'


def get_user_profile(obj):
    return UserProfile.objects.get(user=obj)


class UserResource(resources.ModelResource):
    univ_name = fields.Field()

    def dehydrate_univ_name(self, Application):
        try:
            userp = get_user_profile(Application)
            univ_code = userp.university
        except:
            print "ERROR"
            univ_code = "ERROR"
        return univ_code

    class Meta:
        model = User
        fields = ('id', 'last_login', 'username', 'userprofile__how_you_found_us', 'userprofile__nationality', 'userprofile__university', 'univ_name', 'userprofile__gender', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')


class StatusFilter(admin.SimpleListFilter):
    title = 'application status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Applied'),
            ('no', 'Not Applied'),
        )

    def queryset(self, request, qs):
        if self.value() == 'yes':
            return qs.filter(application__isnull=False)
        elif self.value() == 'no':
            return qs.filter(application__isnull=True)


class UniversityFilter(admin.SimpleListFilter):
    title = 'university'
    parameter_name = 'university'

    def lookups(self, request, model_admin):
        universities = set([get_user_profile(u).university for
                            u in model_admin.model.objects.all()])
        return [(u.id, u.name) for u in universities]

    def queryset(self, request, qs):
        if self.value():
            return qs.filter(userprofile__university__id__exact=self.value())
        else:
            return qs


class UserAdmin(ImportExportModelAdmin):
    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    get_name.admin_order_field = 'first_name'
    get_name.short_description = 'Name'

    def get_university(self, obj):
        return get_user_profile(obj).university.name
    get_university.admin_order_field = 'userprofile__university__name'
    get_university.short_description = 'University'

    def get_major(self, obj):
        return get_user_profile(obj).major
    get_major.admin_order_field = 'userprofile__major'
    get_major.short_description = 'Major'

    def get_phone(self, obj):
        return get_user_profile(obj).phone
    get_phone.admin_order_field = 'userprofile__phone'
    get_phone.short_description = 'Phone'

    list_display = ('get_name',
                    'get_university',
                    'get_major',
                    'email',
                    'get_phone',
                    'is_staff')
    inlines = (UserProfileInline, )
    list_filter = (StatusFilter, UniversityFilter)
    resource_class = UserResource


class UniversityResource(resources.ModelResource):
    class Meta:
        model = University


class UniversityAdmin(ImportExportModelAdmin):
    list_display = ('country', 'name', 'id')
    list_filter = ('country', )
    resource_class = UniversityResource

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(University, UniversityAdmin)
