from django.http import HttpResponse, request
import datetime
from django.shortcuts import render,redirect,get_object_or_404
import datetime
from website.models import Qist
from django.db.models import Sum,Q
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa

# def home(request):
#     date = datetime.datetime.now()
#     name = "Ali Hassan"
#     # return HttpResponse("<h1> I am ali hassan </h1>" + str(date))
    

#     data = {
#         'name':name,
#         'date':date
#     }
#     return render(request,"home.html",data)

total_loan = 974000

def index(request):
    
    qists=Qist.objects.all()
    total_paid_amount = Qist.objects.aggregate(Sum('amount'))['amount__sum'] or 0 
    remaining_amound=total_loan-total_paid_amount
    paid_percentage = int((total_paid_amount / total_loan) * 100)
    unpaid = int(100 - paid_percentage) 

    data = {
        'total_paid_amount':total_paid_amount,
        'remaining_amount':remaining_amound,
        'paid':paid_percentage,
        'unpaid':unpaid
    }   
    
    return render(request, "index.html",data)

def history(request):
    return render(request, "history.html",{})

def paid(request):

    #fetch data from form

    if request.method == "POST":        
       
        sr = request.POST.get('sr')
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        t_id = request.POST.get('t_id')
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        

    #save fetched data in new object(row or record)

        e = Qist()
        e.sr=sr
        e.date=date
        e.amount=amount
        e.t_id=t_id
        e.sender=sender
        e.receiver=receiver

    #save object(row or record)
        e.save()    

        return redirect('/paid/')            


    else:
        print("Error submitting form data")

           # Handle GET request and search
    search_query = request.GET.get('search', '').strip()  

    if search_query:
        qists = Qist.objects.filter(t_id__icontains=search_query)
    else:
        qists = Qist.objects.all()


    sort_by = request.GET.get('sort', '')  

    
    # Start with all data
    # qists = Qist.objects.all()

   
    
    if sort_by.lstrip('-') in ['sr']:
        qists = qists.order_by(sort_by)


   


    #fetch all data from table 

    # qists=Qist.objects.all()
    qists_count=Qist.objects.count()    
    total_paid_amount = Qist.objects.aggregate(Sum('amount'))['amount__sum'] or 0 
    total_remaining = total_loan - total_paid_amount    

   #display fetched data in template

    date = datetime.datetime.now()
    

    print(date)    
    data = {    

        'qists':qists,
        'total_loan':total_loan,
        'total_paid':total_paid_amount,
        'total_remaining':total_remaining,
        'qists_count':qists_count,
        'search_query': search_query,
        'today':date,
        'sort_by': sort_by,
    }

    return render(request, "paid.html",data)





def export_qists_pdf(request):
    qists = Qist.objects.all()
    template = get_template("qists_pdf.html")
    html = template.render({'qists': qists})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="qist_records.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response