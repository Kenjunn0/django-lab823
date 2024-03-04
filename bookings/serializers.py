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