from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import csv
import datetime
import xlwt

# Create your views here.


@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context={
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url="/authentication/login")
def add_expense(request):
    categories = Category.objects.all()
    context={
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        description = request.POST['description']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)

        date = request.POST['expense_date']
        category = request.POST['category']

        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)

        # messages.success(request, 'Expense saved successfully')

        return redirect('expensesapp')


@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context ={
        'expense': expense,
        'values': expense,
        'categories': categories,
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)

        description = request.POST['description']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)

        date = request.POST['expense_date']
        category = request.POST['category']

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        # messages.success(request, 'Expense updated successfully')

        return redirect('expensesapp')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    # messages.success(request, 'Expense deleted')
    return redirect('expensesapp')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
    str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses=Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')
    
    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)

    return response