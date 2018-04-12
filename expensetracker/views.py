# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExpenseForm
from .models import Expenses
from django.shortcuts import get_object_or_404
from django.contrib import messages
import csv
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def calculateTotalExpense(expense):
    return expense.travel + expense.food + expense.miscellaneous

def render_list( request,listExpenses ):
    total = 0  
    for expense in listExpenses:
        total += expense.total_expense
    return render(request,'list.html',{'total':total, 'expenses':listExpenses})
    
# Create your views here.
@login_required
def index(request):
    return render(request,'index.html')

@login_required
def new(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.total_expense = calculateTotalExpense(expense)
            expense.save()
        return render(request,'index.html')
    else:   
        form = ExpenseForm()
        return render(request,'new.html',{'form':form})

@login_required
def list(request):
    listExpenses = Expenses.objects.order_by('-date')
    return render_list(request,listExpenses)

@login_required
def update(request,pk):
    expense = get_object_or_404(Expenses, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expenseData = form.save(commit=False)
            expenseData.total_expense = calculateTotalExpense(expenseData)
            expenseData.save()  
        listExpenses = Expenses.objects.order_by('-date')
        return render_list(request,listExpenses)
    else:
        form = ExpenseForm(instance=expense)
        return render(request,'update.html',{'form':form})

@login_required
def delete(request,pk):
    expense = get_object_or_404(Expenses, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expenseData = form.save(commit=False)
            expenseData.total_expense = calculateTotalExpense(expenseData)
            expenseData.delete()  
        listExpenses = Expenses.objects.order_by('-date')
        return render_list(request,listExpenses)

    else:
        form = ExpenseForm(instance=expense)
        return render(request,'delete.html',{'form':form})

@login_required
def search(request):
    if request.method == "POST":
        fromdate = request.POST.get("fromdate", "")
        todate = request.POST.get("todate", "")
        if len(fromdate) == 0:
            messages.error(request, 'From date cannot be empty')
            return render(request,'list.html')
        if len(todate) == 0:
            messages.error(request, 'To date cannot be empty')
            return render(request,'list.html')
        
        listExpenses = Expenses.objects.filter(date__range=[fromdate, todate])
        return render_list(request,listExpenses)

@login_required
def export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Travel', 'Food', 'Miscellaneous', 'Description','Total Expense'])
    expenses = Expenses.objects.all()
    for expense in expenses:
        writer.writerow([expense.date, expense.travel, expense.food, expense.miscellaneous,expense.descr,expense.total_expense])
    return response
    
@login_required
def chart(request):
    now = datetime.datetime.now()
    total = []

    for count in range(1,13):
        total_expense = Expenses.objects.filter(date__year=now.year, date__month=count).aggregate(Sum('total_expense'))
        expense = total_expense.get('total_expense__sum',0)
        if expense is None:
            expense = 0
        total.append(expense)
    return render(request,'chart.html',{'expenses':total})