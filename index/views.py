import base64
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .templatetags.custom_filters import humanize_time

from .forms import ItemForm

def index(request):
    items = Item.objects.all()
    category=Category.objects.all()
    return render(request, 'homepage.html', {'items': items,'category':category})

def category_view(request,name):
    items = Item.objects.filter(category=name)
    category=Category.objects.all()
    return render(request, 'homepage.html', {'items': items,'category':category})

def searchview(request):
    category=Category.objects.all()
    word=request.GET.get('search')
    wordset=word.split(" ")
    items = []
    for i in wordset:
        # Filter items for each word and append the results to the 'items' list
        items.extend(Item.objects.filter(Q(category__icontains=i)|Q(name__icontains=i)|Q(price__icontains=i)).distinct())
    return render(request,'homepage.html',{'items': items,'category':category})

def buypage(request, item_id):
    category=Category.objects.all()
    item = get_object_or_404(Item, pk=item_id)
    request.session['itemid']=item_id
    return render(request, 'buypage.html', {'item': item,'category':category})


def aboutus(request):
    category=Category.objects.all()
    return render(request, 'aboutus.html',{'category':category})

@login_required
def uploaditem(request):
    category=Category.objects.all()
    if request.method == 'POST':
        # Get form data
        item_name = request.POST.get('item_name')
        pcategory = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        photo = request.FILES.get('photos')
        image_encoded = base64.b64encode(photo.read()).decode('utf-8')

        current_user_id = request.user.id
        current_user = User.objects.get(pk=current_user_id)

        # Validate and save data
        if item_name and pcategory and description and price and condition:
            try:
                price = float(price)
            except ValueError:
                messages.error(request, 'Invalid price format')
                return redirect('index:uploaditem')

            new_item = Item(
                name=item_name,
                category=pcategory,
                description=description,
                price=price,
                condition=condition,
                seller_id=current_user,
                photos=photo,
                image_encoded=image_encoded
            )

            new_item.save()
            messages.success(request, 'Item added successfully')
            return redirect('index:uploaditem')
        else:
            messages.error(request, 'Please fill in all required fields')
            return redirect('index:uploaditem')
    else:
        return render(request, 'uploadpage.html',{'category':category})
@login_required
def chat(request):
    return render(request, 'chatbot.html')

@login_required
def my_profile(request):
    category=Category.objects.all()
    user = request.user
    uploaded_items = Item.objects.filter(seller_id=user)

    context = {
        'user': user,
        'uploaded_items': uploaded_items,
        'category':category
    }

    return render(request, 'myprofile.html', context)

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            if 'photos' in request.FILES:
                item.photos = request.FILES['photos']
                item.image_encoded = base64.b64encode(item.photos.read()).decode('utf-8')
            form.save()
            return redirect('index:my_profile')  # Redirect to item detail page
    else:
        form = ItemForm(instance=item)
    categories = Category.objects.all()  # Get all categories
    return render(request, 'edititem.html', {'form': form, 'category': categories, 'item': item})

@login_required
def deleteitem(request,id):
    item=Item.objects.get(pk=id)
    item.delete()
    return redirect('index:my_profile')

@login_required
def chat_view(request, id):
    user = request.user
    sender = User.objects.get(pk=user.pk)
    receiver = User.objects.get(pk=id)
    # Fetch messages sent by both the sender and receiver
    sent_messages = sendmessage.objects.filter(sender_id=sender, reciver_id=receiver)
    received_messages = sendmessage.objects.filter(sender_id=receiver, reciver_id=sender)
    # Combine sent and received messages
    chat_messages = (sent_messages | received_messages).order_by('time')  # Sorting by time in ascending order
    print(chat_messages)
    for i in received_messages:
        if i.read == False:
            i.read = True
            i.save(update_fields=['read'])
    if request.method == "POST":
        item_id = request.session.get('itemid', '')  # Get item_id from session, default to empty string if not found
        if 'itemid' in request.session:
            del request.session['itemid'] 
        model = sendmessage()
        model.Item_id = item_id
        model.message = request.POST.get('chat')  # Use get method to avoid KeyError
        model.sender_id = sender
        model.reciver_id = receiver
        model.save()
        return redirect('index:chat', id=id)
    return render(request, 'chatbot.html', {'user': sender, 'friend': receiver, 'chat_messages': chat_messages})

@login_required
def new_message(request):
    categories = Category.objects.all()
    user = request.user
    messages = sendmessage.objects.filter(reciver_id=user)
    unique_senders = messages.values_list('sender_id', flat=True).distinct()
    senders_info = User.objects.filter(pk__in=unique_senders)
    return render(request, 'chatmessage.html', {'messages1': messages, 'senders_info': senders_info, 'category': categories})

@login_required
def wishlist_item(request,id): 
    if request.method == "POST":
        cartModel = wishlistModel()
        cartModel.orderId = "0"
        cartModel.itemId = id
        cartModel.userId = request.user.pk
        cartModel.qty = "1"
        cartModel.price = str(request.POST['item_price'])
        cartModel.totalPrice = str(float(cartModel.qty) * float(cartModel.price) )
        cartModel.save()
        messages.success(request, 'Item added into wishlist')
        return redirect('index:buypage', item_id=id)
        

@login_required
def wishlist_view(request): 
    categories = Category.objects.all()
  
    a=wishlistModel.objects.all().filter(userId=request.user.pk) & wishlistModel.objects.all().filter(orderId="0")
    print(len(a))
    cartdataarrey=[]
    finalamt=0
    for i in a:
        finalamt += float(i.totalPrice)
        productdata=Item.objects.get(pk=i.itemId)
        productname=productdata.name
        productimage=productdata.photos
        cartdict = {'cartId':i.pk,'productId':i.itemId,'productname':productname,'productimage':productimage,'quantity':i.qty,'productprice':i.price,"totalproductprice":i.totalPrice}
        cartdataarrey.append(cartdict)       
    return render(request,'wishlist.html',{'wish':cartdataarrey,'finalamt':finalamt,'cartTotalProduct':len(cartdataarrey),'category': categories})

@login_required
def w_deleteitem(request,id):
    item=wishlistModel.objects.get(pk=id)
    item.delete()
    return redirect('index:wishlist_view')

# import razorpay
import paypalrestsdk

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.urls import reverse


PAYPAL_CLIENT_ID = 'AReBB7UpHFsSbRKLI_V6IqaHIQALhNTzOUN1Lor9CvvAbAfGMax-Ssjmc4KLr_z1PZIslFtHW_jLxx_h'
PAYPAL_SECRET = 'EDRkv2ysVsfbu8uudpXN3CLYohGmMeB2XtfoUuIsRtCws3oLnmjZ_wt2NoNDY-P-bHhalaO0G56hxf-7'
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_SECRET,
})
@login_required
def buynow(request):
    if request.method == "POST":
        product_id = request.POST['item_id']
        product = Item.objects.get(item_id=product_id)
        request.session['productid'] = product_id
        request.session['quantity'] = 1
        request.session['orderAmount'] = str(product.price)
        request.session['paymentMethod'] = "PayPal"
        request.session['transactionId'] = ""
        return redirect('index:paypal_payment')
    else:
        messages.error(request, 'Requested Faild Try After Some Time')
        return redirect(request.META.get('HTTP_REFERER', 'index:index'))

@login_required
def paypal_payment(request):
    currency = 'USD'  # Change currency if needed
    amount = float(request.session['orderAmount'])
    success_url = request.build_absolute_uri(reverse('index:paypal_payment_success'))
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": success_url,
            "cancel_url": "http://localhost:8000/payment/cancel/"
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": currency
            },
            "description": "Payment for product"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                redirect_url = link.href
                return redirect(redirect_url)
    else:
        return HttpResponseBadRequest()

@login_required
@csrf_exempt
def paypal_payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Payment executed successfully, save order details
        order = Ordermodel(
            productid=request.session['productid'],
            qty=request.session['quantity'],
            userid=request.user.pk,
            username=request.user.username,
            useremail=request.user.email if request.user.email else "",
            orderamount=request.session['orderAmount'],
            paymentvia="online",
            paymentmethod=request.session['paymentMethod'],
            transactionid=payment_id
        )
        order.save()
        del request.session['productid']
        del request.session['quantity']
        del request.session['orderAmount']
        del request.session['paymentMethod']
        return redirect('index:orderSuccessView')
    else:
        # Payment execution failed
        return HttpResponseBadRequest()

@login_required
def paypal_payment_cancel(request):
    # Handle payment cancellation
    return HTTPResponse("Payment Cancelled")

# @login_required
# def buynow(request):
#     if request.method == "POST":
#         product_id = request.POST['item_id']
#         product = Item.objects.get(item_id=product_id)
#         request.session['productid'] = product_id
#         request.session['quantity'] = 1
#         request.session['orderAmount'] = str(product.price)
#         request.session['paymentMethod'] = "Razorpay"
#         request.session['transactionId'] = ""
#         return redirect('index:razorpayView')
#     else:
#         messages.error(request, 'Requested Faild Try After Some Time')
#         return redirect(request.META.get('HTTP_REFERER', 'index:index'))

# RAZOR_KEY_ID = 'rzp_test_PCLwUnDh0gx1EM'
# RAZOR_KEY_SECRET = '5X09bgMznDr8vOIuQ0xCkZ53'
# client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

# @login_required
# def razorpayView(request):
#     currency = 'INR'
#     amount = float(request.session['orderAmount'])*100
#     # Create a Razorpay Order
#     razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url    
#     return render(request,'razorpayDemo.html',context=context)

# @login_required
# @csrf_exempt
# def paymenthandler(request):
#     # only accept POST request.
#     if request.method == "POST":
#         try:
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')

#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
 
#             # verify the payment signature.
#             result = client.utility.verify_payment_signature(
#                 params_dict)
            
#             amount = float(request.session['orderAmount'])*100  # Rs. 200
#             # capture the payemt
#             client.payment.capture(payment_id, amount)

#             #Order Save Code
#             orderModel = Ordermodel()
#             orderModel.productid=request.session['productid']
#             orderModel.qty=request.session['quantity']
#             orderModel.userid = request.user.pk
#             orderModel.username = request.user.username
#             if request.user.email:
#                 orderModel.useremail = request.user.email
#             else:
#                 orderModel.useremail = ""
#             orderModel.orderamount = request.session['orderAmount']
#             orderModel.paymentvia = "online"
#             orderModel.paymentmethod = request.session['paymentMethod']
#             orderModel.transactionid = payment_id
#             orderModel.save()
#             del request.session['productid']
#             del request.session['quantity']
#             del request.session['orderAmount']
#             del request.session['paymentMethod']
#             # render success page on successful caputre of payment
#             return redirect('index:orderSuccessView')
#         except:
#             print("Hello")
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#         print("Hello1")
#        # if other than POST request is made.
#         return HttpResponseBadRequest()

@login_required
def successview(request):
    return render(request,'order_sucess.html')


@login_required
def myorder(request):
    categories = Category.objects.all()
    user_orders = Ordermodel.objects.filter(userid=request.user.pk)
    prolist=[]
    for i in user_orders:
        pro={}
        productdata=Item.objects.get(pk=i.productid)
        pro['img']=productdata.photos
        pro['id']=i.productid
        pro['name']=productdata.name
        pro['orderDate']=i.orderdatetime
        pro['productqty']=i.qty
        pro['transactionId']=i.transactionid
        pro['paymentMethod']=i.paymentmethod
        pro['orderAmount']=i.orderamount
        pro['image_encoded']=productdata.image_encoded

        prolist.append(pro)
        print(prolist)
    return render(request, 'myorder.html', {'category': categories, 'prolist':prolist})

