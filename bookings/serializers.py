from django.utils import timezone
from rest_framework import serializers
from .models import Booking

class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "kind",
            "check_in",
            "check_out",
            "experience_time",
            "guest",
        )

class CreateRoomBookingSerializer(serializers.ModelSerializer):

    # 기존 Booking 모델은 check_in, check_out이 null=True이기 때문에 오버라이딩을 하여 check_in, check_out을 필수 입력 항목으로 만들어준다.
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guest"
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        return value

    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check in should be smaller than check out.")

        if Booking.objects.filter(
            check_in__lte=data['check_out'],
            check_out__gte=data['check_in'],
        ).exists():
            raise serializers.ValidationError("Those (or some) of those datas are already taken.")

        return data