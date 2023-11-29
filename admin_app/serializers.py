from rest_framework import serializers

class IncomeSerializer(serializers.Serializer):
    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
