with open('apps/staff/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''@login_required
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related("items__item").order_by("-created_at")
    return render(request, "store/customer_dashboard.html", {"orders": orders})'''

new_func = '''@login_required
def customer_dashboard(request):
    try:
        orders = Order.objects.filter(customer=request.user).prefetch_related("items__item").order_by("-created_at")
    except Exception:
        orders = []
    return render(request, "store/customer_dashboard.html", {"orders": orders})'''

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('apps/staff/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Updated customer_dashboard view!")
else:
    print("View is already updated or pattern matched.")