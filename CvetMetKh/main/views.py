from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Client, Metal, Receipt, ReceiptHasMetal
from django.db import connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@csrf_exempt
def renderMain(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        selectQuery = """SELECT r.order_id, c.name AS 'client_name', c.email, 
                        rhm.count, m.name AS 'metal_name', 
                        os.name AS 'status' FROM receipt r
                        JOIN client c ON r.client_id = c.client_id
                        JOIN receipt_has_metal rhm ON r.order_id = rhm.order_id
                        JOIN metal m ON m.metal_id = rhm.metal_id
                        JOIN order_status os ON os.status_id = r.status_id"""
        cursor.execute(selectQuery)
        result = dictfetchall(cursor)
        return render(request, 'main/main.html', {'result': result})
    if request.method == 'POST':
        cName = request.POST["name"]
        cEmail = request.POST["email"]
        metalId = request.POST["metal"]
        cMetal = Metal.objects.filter(metal_id = metalId)
        cAmount = request.POST["amount"]
        newClient = Client(name = cName, email = cEmail)
        newClient.save()
        newRecipt = Receipt(client_id = newClient.client_id, manager_id = 1, status_id = 4)
        newRecipt.save()
        newReceiptHasMetal = ReceiptHasMetal(order_id = newRecipt.order_id, metal_id = cMetal[0].metal_id, count = cAmount, price = cMetal[0].price)
        newReceiptHasMetal.save()
        return render(request, 'main/messege.html')