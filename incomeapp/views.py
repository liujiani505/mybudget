from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.


@login_required(login_url="/authentication/login")
def index(request):
    sources = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context={
        'income': income,
        'page_obj': page_obj
    }
    return render(request, 'income/index.html', context)


@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    context={
        'sources': sources,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        description = request.POST['description']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)

        date = request.POST['income_date']
        source = request.POST['source']

        Income.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)

        # messages.success(request, 'Income saved successfully')

        return redirect('incomeapp')


@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context ={
        'income': income,
        'values': income,
        'sources': sources,
    }

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)

        description = request.POST['description']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)

        date = request.POST['income_date']
        source = request.POST['source']

        income.amount = amount
        income.date = date
        income.source = source
        income.description = description

        income.save()
        # messages.success(request, 'Income updated successfully')

        return redirect('incomeapp')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    # messages.success(request, 'Income deleted')
    return redirect('incomeapp')

