from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"

    parameter_name = "word"

    # self : 해당 클래스 객체를 의미, request : 이 메소드를 호출하는 대상인 user 객체를 의미한다. model_admin : 이 필터를 사용하는 클래스
    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

        # self : 해당 클래스 객체를 의미, request : 이 메소드를 호출하는 대상인 user 객체를 의미한다. queryset : 필터링하는 객체

    def queryset(self, request, queryset):
        word = self.value
        # 모든 필터를 삭제하여 word가 존재하지 않을 때, word가 null을 반환하여 에러가 발생할 수 있으므로 if문 삽입
        if word:
            return queryset.filter(payload__contains=word)
        else:
            return queryset

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ("__str__", "rating", "payload", )
    list_filter = ( WordFilter, "rating", "user__is_host", "room__category", "room__pet_friendly", )
