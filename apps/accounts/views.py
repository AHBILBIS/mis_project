def user_login(request):
    """
    Standard HTML login view.
    """
    # 1. If already logged in, send directly to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    # 2. Handle Form Submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    # 3. Always render the template on GET request
    return render(request, 'accounts/login.html')