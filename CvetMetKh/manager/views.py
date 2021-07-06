from django.db.models.aggregates import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from main.models import Supply, SupplyHasMetal, Metal
from django.db import connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def renderMain(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        if(request.GET.get('Confirm')):
            orderId = request.GET.get('id')
            updateQuery = """UPDATE receipt
                            SET status_id = 1
                            WHERE order_id = %s"""
            cursor.execute(updateQuery % orderId)
        elif(request.GET.get('Reject')):
            orderId = request.GET.get('id')
            updateQuery = """UPDATE receipt
                            SET status_id = 2
                            WHERE order_id = %s"""
            cursor.execute(updateQuery % orderId)
        selectQuery = """SELECT r.order_id, c.name AS 'client_name', c.email, rhm.count, m.name AS 'metal_name' FROM receipt r
                        JOIN client c ON r.client_id = c.client_id
                        JOIN receipt_has_metal rhm ON r.order_id = rhm.order_id
                        JOIN metal m ON m.metal_id = rhm.metal_id
                        JOIN order_status os ON os.status_id = r.status_id
                        WHERE os.name = 'processing'"""
        cursor.execute(selectQuery)
        result = dictfetchall(cursor)
        allMetal = Metal.objects.all()
        return render(request, 'manager/main.html', {'result': result, 'allMetal': allMetal})
    elif request.method == 'POST':
        metalId = request.POST["metal"]
        cAmount = request.POST["amount"]
        newSupply = Supply(manager_id = 1, status_id = 2)
        newSupply.save()
        newSupplyHasMetal = SupplyHasMetal(metal_id = metalId, 
                                        supply_id = newSupply.supply_id, 
                                        count = cAmount)
        newSupplyHasMetal.save()
        selectedMetal = Metal.objects.get(pk = metalId)
        selectedMetal.amount += int(cAmount)
        selectedMetal.save()
        return render(request, 'manager/messege.html')