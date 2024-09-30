from django.shortcuts import render, redirect
import random
import time
from datetime import datetime, timedelta
# Create your views here.
daily_specials = [
    "Boston Cream Donut",
    "Custard Donut",
    "Jelly Donut",
    "Vanilla Long John Donut",
]
frostings = {
    'strawberry': .5,
    'chocolate': .5,
    'vanilla': .5,
    'none': 0
}
donuts = {
    'Cinnamon': 1.99,
    'Glazed': 2.99,
    'Chocolate Long John': 1.99,
    'Daily Special': 3.99
}
def main(request):
    template_name = "restaurant/main.html"
    
    return render(request, template_name)

def order(request):
    template_name = "restaurant/order.html"
    context = {
        'daily_special': random.choice(daily_specials)
    }
    return render(request, template_name, context)

def confirmation(request):
    if request.POST:
        current_time = time.time()
        current_datetime = datetime.fromtimestamp(current_time)
        new_datetime = current_datetime + timedelta(minutes=random.randint(30, 60))
        
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        order = request.POST.getlist('donut')
        frosting = request.POST.get('glazed-frosting')
        price = 0
        time_ready = new_datetime
        
        
        template_name = "restaurant/confirmation.html"
        orders = []
        
        for item in order:
            if item == 'Glazed':
                price += donuts['Glazed']
                if frosting == 'none' or frosting is None:
                    orders.append('Glazed Donut with no frosting')
                else:
                    orders.append('Glazed Donut with ' + str(frosting) + ' frosting')
                    price += frostings[str(frosting)]
            else:
                orders.append(str(item) + ' Donut' )
                price += donuts[str(item)]
        print("orders: " + str(orders))
        context = {
            'name': name,
            'email': email,
            'phone_number': phone_number,
            'order': orders,
            'price': price,
            'time_ready': time_ready
        }
        return render(request, template_name, context)
    return redirect('order')
    