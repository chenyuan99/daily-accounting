from django.shortcuts import render, redirect
import calendar
import datetime
import decimal

from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import permissions, viewsets
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from accounting.filters import *
from accounting.forms import *
from accounting.serializers import UserSerializer, GroupSerializer, TransferRecordSerializer, PhotoSerializer, AccountSerializer, \
    CurrencySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransferRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TransferRecord.objects.all()
    serializer_class = TransferRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class PhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ImageModel.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


def index(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    today = datetime.date.today()
    all_accounts = Account.objects.all()
    currencies = Currency.objects.all()
    ie_types = Category.CATEGORY_TYPES
    history_records = HistoryRecord.objects.filter(time_of_occurrence__year=today.year,
                                                   time_of_occurrence__month=today.month).order_by(
        "-time_of_occurrence")
    transfer_records = TransferRecord.objects.filter(time_of_occurrence__year=today.year,
                                                     time_of_occurrence__month=today.month).order_by(
        "-time_of_occurrence")
    income = 0
    expense = 0
    day_has_record = []
    current_month_records = {}
    day_income_expense = {}
    for hr in history_records:
        if hr.category.category_type.lower() == "expense":
            expense -= hr.amount
        elif hr.category.category_type.lower() == "income":
            income += hr.amount
        day_occur = hr.time_of_occurrence.strftime("%Y-%m-%d %A")
        if day_occur not in day_has_record:
            day_has_record.append(day_occur)
            current_month_records[day_occur] = [hr]
            day_income_expense[day_occur] = {"income": 0, "expense": 0}
            if hr.category.category_type.lower() == "expense":
                day_income_expense[day_occur]["expense"] += hr.amount
            elif hr.category.category_type.lower() == "income":
                day_income_expense[day_occur]["income"] += hr.amount
        else:
            current_month_records[day_occur].append(hr)
            if hr.category.category_type.lower() == "expense":
                day_income_expense[day_occur]["expense"] += hr.amount
            elif hr.category.category_type.lower() == "income":
                day_income_expense[day_occur]["income"] += hr.amount
    for tr in transfer_records:
        day_occur = tr.time_of_occurrence.strftime("%Y-%m-%d %A")
        if day_occur not in day_has_record:
            day_has_record.append(day_occur)
            current_month_records[day_occur] = [tr]
            day_income_expense[day_occur] = {"income": 0, "expense": 0}
        else:
            current_month_records[day_occur].append(tr)
    day_has_record.sort(reverse=True)
    context = {
        'accounts': all_accounts,
        'currencies': currencies,
        'ie_types': ie_types,
        'day_has_record': day_has_record,
        'history_records': history_records,
        'transfer_records': transfer_records,
        'current_month_income': income,
        'current_month_expense': expense,
        'surplus': income + expense,
        'current_month_records': current_month_records,
        'day_income_expense': day_income_expense
    }
    return render(request, 'accounting/index.html', context)


def retrieve_category(request):
    if request.user.is_authenticated:
        ie_type = request.POST.get('ie_type')
        categories = Category.objects.filter(category_type=ie_type)
        category_list = []
        for c in categories:
            category_list.append((c.id, c.name))
        # return HttpResponse(f'{"categories": {categories}}', content_type='application/json')
        return JsonResponse({"categories": category_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_subcategory(request):
    if request.user.is_authenticated:
        category_type = request.POST.get('category_type')
        current_category = Category.objects.filter(name=category_type)[0]
        subcategories = SubCategory.objects.filter(parent=current_category)
        subcategory_list = []
        for sc in subcategories:
            subcategory_list.append((sc.id, sc.name))
        return JsonResponse({"subcategories": subcategory_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def record_income_expense(request):
    """Handle income/expense record creation."""
    if request.method == 'POST':
        form = HistoryRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            
            # Update account balance
            account = record.account
            if record.category.category_type == 'income':
                account.amount += record.amount
            else:
                account.amount -= record.amount
            account.save()
            
            messages.success(request, 'Transaction recorded successfully!')
            return JsonResponse({
                'status': 'success',
                'message': 'Transaction recorded successfully',
                'redirect': reverse('history')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    else:
        form = HistoryRecordForm()
    
    return render(request, 'accounting/record_form.html', {
        'form': form,
        'title': 'Record Income/Expense'
    })


def retrieve_current_month_income_expense(request):
    if request.user.is_authenticated:
        post_year = request.POST.get('year')
        post_month = request.POST.get('month')
        if post_year and post_month:
            year = int(post_year)
            month = int(post_month)
        else:
            today = datetime.date.today()
            year = today.year
            month = today.month
        month_has_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, day).strftime("%Y-%m-%d") for day in range(1, month_has_days + 1)]
        days_income = []
        days_expense = []
        category_names = []
        month_category_income = {}
        month_category_expense = {}
        month_total_income = 0
        month_total_expense = 0
        month_history_records = HistoryRecord.objects.filter(time_of_occurrence__year=year,
                                                             time_of_occurrence__month=month).order_by(
            "time_of_occurrence")
        for day in days:
            day_history_records = month_history_records.filter(time_of_occurrence__day=int(day.split("-")[-1]))
            day_income = 0
            day_expense = 0
            for hr in day_history_records:
                hr_category = hr.category
                if hr_category.category_type.lower() == "expense":
                    day_expense += hr.amount
                    month_total_expense += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        month_category_expense[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        month_category_expense[hr_category.name]["value"] += hr.amount
                elif hr_category.category_type.lower() == "income":
                    day_income += hr.amount
                    month_total_income += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        month_category_income[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        month_category_income[hr_category.name]["value"] += hr.amount
            days_income.append(day_income)
            days_expense.append(day_expense)
        return JsonResponse({"days": days,
                             "days_income": days_income,
                             "days_expense": days_expense,
                             "month_total_income": month_total_income,
                             "month_total_expense": month_total_expense,
                             "month_category_names": category_names,
                             "month_category_income": list(month_category_income.values()),
                             "month_category_expense": list(month_category_expense.values())})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_current_year_income_expense(request):
    if request.user.is_authenticated:
        post_year = request.POST.get('year')
        if post_year:
            year = int(post_year)
        else:
            today = datetime.date.today()
            year = today.year
        months = [i for i in range(1, 13)]
        months_income = []
        months_expense = []
        category_names = []
        year_category_income = {}
        year_category_expense = {}
        year_total_income = 0
        year_total_expense = 0
        year_history_records = HistoryRecord.objects.filter(time_of_occurrence__year=year).order_by(
            "time_of_occurrence")
        for month in months:
            month_history_records = year_history_records.filter(time_of_occurrence__month=month)
            month_income = 0
            month_expense = 0
            for hr in month_history_records:
                hr_category = hr.category
                if hr_category.category_type.lower() == "expense":
                    month_expense += hr.amount
                    year_total_expense += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        year_category_expense[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        year_category_expense[hr_category.name]["value"] += hr.amount
                elif hr_category.category_type.lower() == "income":
                    month_income += hr.amount
                    year_total_income += hr.amount
                    if hr_category.name not in category_names:
                        category_names.append(hr_category.name)
                        year_category_income[hr_category.name] = {"value": hr.amount, "name": hr_category.name}
                    else:
                        year_category_income[hr_category.name]["value"] += hr.amount
            months_income.append(month_income)
            months_expense.append(month_expense)
        return JsonResponse({"months": months,
                             "months_income": months_income,
                             "months_expense": months_expense,
                             "year_total_income": year_total_income,
                             "year_total_expense": year_total_expense,
                             "year_category_names": category_names,
                             "year_category_income": list(year_category_income.values()),
                             "year_category_expense": list(year_category_expense.values())})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_year_has_data(request):
    if request.user.is_authenticated:
        hr_first = HistoryRecord.objects.order_by("time_of_occurrence").first()
        hr_last = HistoryRecord.objects.order_by("time_of_occurrence").last()
        year_list = [y for y in range(hr_last.time_of_occurrence.year, hr_first.time_of_occurrence.year - 1, -1)]
        return JsonResponse({"years": year_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def retrieve_month_has_data(request):
    if request.user.is_authenticated:
        year = request.POST.get('year')
        hr = HistoryRecord.objects.filter(time_of_occurrence__year=year).order_by("time_of_occurrence")
        hr_first = hr.first()
        hr_last = hr.last()
        month_list = [m for m in range(hr_last.time_of_occurrence.month, hr_first.time_of_occurrence.month - 1, -1)]
        return JsonResponse({"months": month_list})
    else:
        return JsonResponse({"error": "unauthenticated"})


def search_record(request):
    if request.user.is_authenticated:
        keyword = request.POST.get('keyword')
        categories = Category.objects.filter(name__icontains=keyword)
        subcategories = SubCategory.objects.filter(name__icontains=keyword)
        hrs = HistoryRecord.objects.filter(
            Q(category__in=categories) | Q(sub_category__in=subcategories) | Q(comment__icontains=keyword) | Q(
                amount__icontains=keyword))
        records = []
        for hr in hrs:
            day_occur = hr.time_of_occurrence.strftime("%Y-%m-%d %A")
            if hr.sub_category:
                sub_category = hr.sub_category.name
            else:
                sub_category = "no sub category"
            if hr.comment:
                comment = hr.comment
            else:
                comment = ""
            records.append({
                "day": day_occur,
                "category": hr.category.name,
                "subcategory": sub_category,
                "amount": hr.amount,
                "comment": comment,
                "account": hr.account.name,
                "ie_type": hr.category.category_type.lower()
            })
        return JsonResponse({"records": records})
    else:
        return JsonResponse({"error": "unauthenticated"})


def filter_record_by_date(request):
    if request.user.is_authenticated:
        post_year = request.POST.get('year')
        post_month = request.POST.get('month')
        history_records = HistoryRecord.objects.filter(time_of_occurrence__year=post_year,
                                                       time_of_occurrence__month=post_month).order_by(
            "-time_of_occurrence")
        transfer_records = TransferRecord.objects.filter(time_of_occurrence__year=post_year,
                                                         time_of_occurrence__month=post_month).order_by(
            "-time_of_occurrence")
        day_has_record = []
        custom_month_records = {}
        for hr in history_records:
            day_occur = hr.time_of_occurrence.strftime("%Y-%m-%d %A")
            if hr.sub_category:
                sub_category = hr.sub_category.name
            else:
                sub_category = "no sub category"
            if hr.comment:
                comment = hr.comment
            else:
                comment = ""
            new_hr = {
                "category": hr.category.name,
                "subcategory": sub_category,
                "amount": hr.amount,
                "comment": comment,
                "account": hr.account.name,
                "ie_type": hr.category.category_type.lower(),
                "record_type": "income_expense"
            }
            if day_occur not in day_has_record:
                day_has_record.append(day_occur)
                custom_month_records[day_occur] = [new_hr]
            else:
                custom_month_records[day_occur].append(new_hr)
        for tr in transfer_records:
            day_occur = tr.time_of_occurrence.strftime("%Y-%m-%d %A")
            if tr.comment:
                comment = tr.comment
            else:
                comment = ""
            new_tr = {
                "amount": tr.amount,
                "comment": comment,
                "from_account": tr.from_account.name,
                "to_account": tr.to_account.name,
                "record_type": "transfer"
            }
            if day_occur not in day_has_record:
                day_has_record.append(day_occur)
                custom_month_records[day_occur] = [new_tr]
            else:
                custom_month_records[day_occur].append(new_tr)
        return JsonResponse({'day_has_record': day_has_record, "records": custom_month_records})
    else:
        return JsonResponse({"error": "unauthenticated"})


def transfer_between_accounts(request):
    """Handle transfers between accounts."""
    if request.method == 'POST':
        form = TransferRecordForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.owner = request.user
            
            # Set currency from source account
            transfer.currency = transfer.from_account.currency
            
            # Validate currencies match
            if transfer.from_account.currency != transfer.to_account.currency:
                messages.error(request, 'Cannot transfer between accounts with different currencies')
                return JsonResponse({
                    'status': 'error',
                    'message': 'Currency mismatch between accounts'
                }, status=400)
            
            # Update account balances
            from_account = transfer.from_account
            to_account = transfer.to_account
            
            if transfer.amount > from_account.amount:
                messages.error(request, 'Insufficient funds in source account')
                return JsonResponse({
                    'status': 'error',
                    'message': 'Insufficient funds'
                }, status=400)
            
            from_account.amount -= transfer.amount
            to_account.amount += transfer.amount
            
            # Save all changes in a transaction
            try:
                with transaction.atomic():
                    transfer.save()
                    from_account.save()
                    to_account.save()
                    
                messages.success(request, 'Transfer completed successfully!')
                return JsonResponse({
                    'status': 'success',
                    'message': 'Transfer completed successfully',
                    'redirect': reverse('history')
                })
            except Exception as e:
                messages.error(request, 'An error occurred during transfer')
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    else:
        form = TransferRecordForm()
    
    return render(request, 'accounting/transfer_form.html', {
        'form': form,
        'title': 'Transfer Between Accounts'
    })


def dashboard(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    items = HistoryRecord.objects.all()
    context = {
        'items': items,
    }
    return render(request, "accounting/billList.html", context)


def display_categoryList(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    today = datetime.date.today()
    all_accounts = Account.objects.all()
    currencies = Currency.objects.all()
    ie_types = Category.CATEGORY_TYPES
    history_records = HistoryRecord.objects.filter(time_of_occurrence__year=today.year,
                                                   time_of_occurrence__month=today.month).order_by(
        "-time_of_occurrence")
    transfer_records = TransferRecord.objects.filter(time_of_occurrence__year=today.year,
                                                     time_of_occurrence__month=today.month).order_by(
        "-time_of_occurrence")
    income = 0
    expense = 0
    day_has_record = []
    current_month_records = {}
    day_income_expense = {}
    for hr in history_records:
        if hr.category.category_type.lower() == "expense":
            expense -= hr.amount
        elif hr.category.category_type.lower() == "income":
            income += hr.amount
        day_occur = hr.time_of_occurrence.strftime("%Y-%m-%d %A")
        if day_occur not in day_has_record:
            day_has_record.append(day_occur)
            current_month_records[day_occur] = [hr]
            day_income_expense[day_occur] = {"income": 0, "expense": 0}
            if hr.category.category_type.lower() == "expense":
                day_income_expense[day_occur]["expense"] += hr.amount
            elif hr.category.category_type.lower() == "income":
                day_income_expense[day_occur]["income"] += hr.amount
        else:
            current_month_records[day_occur].append(hr)
            if hr.category.category_type.lower() == "expense":
                day_income_expense[day_occur]["expense"] += hr.amount
            elif hr.category.category_type.lower() == "income":
                day_income_expense[day_occur]["income"] += hr.amount
    for tr in transfer_records:
        day_occur = tr.time_of_occurrence.strftime("%Y-%m-%d %A")
        if day_occur not in day_has_record:
            day_has_record.append(day_occur)
            current_month_records[day_occur] = [tr]
            day_income_expense[day_occur] = {"income": 0, "expense": 0}
        else:
            current_month_records[day_occur].append(tr)
    day_has_record.sort(reverse=True)
    items = Category.objects.all()
    context = {
        'items': items,
        'accounts': all_accounts,
        'currencies': currencies,
        'ie_types': ie_types,
        'day_has_record': day_has_record,
        'history_records': history_records,
        'transfer_records': transfer_records,
        'current_month_income': income,
        'current_month_expense': expense,
        'surplus': income + expense,
        'current_month_records': current_month_records,
        'day_income_expense': day_income_expense
    }
    return render(request, "accounting/categoryList.html", context)


def display_accountList(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    items = Account.objects.all()
    context = {
        'items': items,
    }
    return render(request, "accounting/accountList.html", context)


def page_demo(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    articles = HistoryRecord.objects.all()
    myFilter = historyRecordFilter(request.GET, queryset=articles)
    items = myFilter.qs
    paginator_obj = Paginator(items, 8)  # 每页5条
    request_page_num = request.GET.get('page', 1)
    page_obj = paginator_obj.page(request_page_num)
    total_page_number = paginator_obj.num_pages
    context = {
        'page_obj': page_obj,
        'paginator_obj': paginator_obj,
        'myFilter': myFilter
    }
    return render(request, 'accounting/page_demo.html', context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("index")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request=request,
                          template_name="registration/register.html",
                          context={"form": form})
    form = UserCreationForm
    return render(request=request,
                  template_name="registration/register.html",
                  context={"form": form})


def legacy(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    items = HistoryRecord.objects.all()
    context = {
        'items': items,
    }
    return render(request, "main/legacy.html", context)


def about(request):
    return render(request, "main/about.html")


def faq(request):
    return render(request, "main/faq.html")


def privacy(request):
    return render(request, "main/privacy-policy.html")
