# history/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from datetime import datetime


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unified_history(request):
    """
    Endpoint untuk melihat semua history perhitungan user dari berbagai kalkulator.
    GET /api/history/
    
    Query Parameters:
    - calculator_type: filter by type (emergency_fund, pension, gold)
    - date_from: filter dari tanggal (YYYY-MM-DD)
    - date_to: filter sampai tanggal (YYYY-MM-DD)
    - sort: sorting (newest/oldest), default: newest
    """
    user = request.user
    calculator_type = request.query_params.get('calculator_type', None)
    date_from = request.query_params.get('date_from', None)
    date_to = request.query_params.get('date_to', None)
    sort_order = request.query_params.get('sort', 'newest')
    
    history_items = []
    
    # Dana Darurat
    if not calculator_type or calculator_type == 'emergency_fund':
        from dana_darurat.models import EmergencyFundCalculation
        
        calcs = EmergencyFundCalculation.objects.filter(user=user)
        
        # Apply date filters
        if date_from:
            calcs = calcs.filter(created_at__gte=date_from)
        if date_to:
            calcs = calcs.filter(created_at__lte=date_to)
        
        for calc in calcs:
            history_items.append({
                'id': calc.id,
                'calculator_type': 'emergency_fund',
                'calculator_name': 'Dana Darurat',
                'date': calc.created_at,
                'status': calc.status,
                'is_suitable': calc.is_suitable,
                'summary': f"Target: Rp {calc.needed_fund:,.0f}, Estimasi: Rp {calc.future_value:,.0f}",
                'recommendation': calc.recommendation,
            })
    
    # Dana Pensiun
    if not calculator_type or calculator_type == 'pension':
        from dana_pensiun.models import PensionCalculation
        
        calcs = PensionCalculation.objects.filter(user=user)
        
        if date_from:
            calcs = calcs.filter(created_at__gte=date_from)
        if date_to:
            calcs = calcs.filter(created_at__lte=date_to)
        
        for calc in calcs:
            history_items.append({
                'id': calc.id,
                'calculator_type': 'pension',
                'calculator_name': 'Dana Pensiun',
                'date': calc.created_at,
                'status': calc.status,
                'is_suitable': calc.is_suitable,
                'summary': f"Kebutuhan: Rp {calc.total_need_at_retire:,.0f}, Estimasi: Rp {calc.estimated_portfolio:,.0f}",
                'recommendation': calc.recommendation,
            })
    
    # Emas
    if not calculator_type or calculator_type == 'gold':
        from emas.models import GoldCalculation
        
        calcs = GoldCalculation.objects.filter(user=user)
        
        if date_from:
            calcs = calcs.filter(created_at__gte=date_from)
        if date_to:
            calcs = calcs.filter(created_at__lte=date_to)
        
        for calc in calcs:
            if calc.mode == 'emas_to_rupiah':
                summary = f"{calc.grams_input} gram = Rp {calc.result_rupiah:,.0f}"
            else:
                summary = f"Rp {calc.rupiah_input:,.0f} = {calc.result_grams} gram"
            
            history_items.append({
                'id': calc.id,
                'calculator_type': 'gold',
                'calculator_name': 'Kalkulator Emas',
                'date': calc.created_at,
                'status': calc.mode,
                'is_suitable': None,  # Gold calculator tidak punya is_suitable
                'summary': summary,
                'recommendation': calc.notes,
            })
    
    # Sort
    reverse = (sort_order == 'newest')
    history_items.sort(key=lambda x: x['date'], reverse=reverse)
    
    return Response({
        'count': len(history_items),
        'history': history_items
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def calculator_history(request, calculator_type):
    """
    Endpoint untuk melihat history dari kalkulator tertentu.
    GET /api/history/<calculator_type>/
    
    Supported calculator_type: emergency_fund, pension, gold
    """
    # Redirect ke unified_history dengan filter calculator_type
    request.query_params._mutable = True
    request.query_params['calculator_type'] = calculator_type
    request.query_params._mutable = False
    
    return unified_history(request)
