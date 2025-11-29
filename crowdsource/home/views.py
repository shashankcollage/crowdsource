from django.shortcuts import render, redirect
from django.db.models import Q  # <--- 1. Add this import
from django.contrib import messages
from .models import Issue, ActivityLog
from .forms import IssueForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile

def dash(request):
    return HttpResponse("homeeeeeeeeeeeeeeee!")
# Create your views here.
def dashboard(request):
    return render(request, 'home/index.html')


def dashboard_view(request):
    # 1. Handle Form Submission (New Issue) - KEEP AS IS
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            ActivityLog.objects.create(issue=issue, action=f"New Issue Reported: {issue.title}")
            messages.success(request, 'Issue created successfully!')
            return redirect('dashboard_view')

    # 2. Calculate Stats - KEEP AS IS
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status__in=['reported', 'verified', 'in_progress']).count()
    resolved_month = Issue.objects.filter(status='resolved').count()

    # 3. Fetch Data with SEARCH LOGIC
    search_query = request.GET.get('q', '')  # Get the search term, default to empty string
    print(search_query)

    # Start with all issues ordered by date
    issues_queryset = Issue.objects.all().order_by('-created_at')

    if search_query:
        # If searching, filter by title OR description OR status
        recent_issues = issues_queryset.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    else:
        # If NOT searching, just show the last 10 (Default Dashboard view)
        recent_issues = issues_queryset[:10]

    recent_activities = ActivityLog.objects.all().order_by('-timestamp')[:5]

    # Dropdowns
    # Note: Ensure this related_model logic works in your specific setup
    users = Issue._meta.get_field('assigned_to').related_model.objects.all()

    context = {
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'resolved_month': resolved_month,
        'recent_issues': recent_issues,
        'recent_activities': recent_activities,
        'users': users,
        'search_query': search_query, # Pass this back to template to keep input filled
    }

    return render(request, 'home/index.html', context)

def create_missing_profiles():
    """Run this once to create profiles for existing users"""
    for user in User.objects.all():
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)
            
@login_required
def user_management(request):
    # Handle POST (Add User)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='temp123'  # Set temp password
            )
            # Create profile
            UserProfile.objects.create(
                user=user,
                role=role,
                phone=phone
            )
            messages.success(request, f'User {username} created successfully!')
            return redirect('user_management')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    # Handle GET - Display users
    users = User.objects.select_related('userprofile').all()
    context = {'users': users}
    return render(request, 'home/index.html', context)