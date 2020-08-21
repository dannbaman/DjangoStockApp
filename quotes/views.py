from django.shortcuts import render,redirect,get_object_or_404
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
	# pk_979d9f9e018048b48d962c434b6cca00
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_requests = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_979d9f9e018048b48d962c434b6cca00".format(ticker))

		try:
			api = json.loads(api_requests.content)
		except Exception as e:
			api = "Error..."
		return render(request,'home.html',{'api':api})

	else:
		return render(request,'home.html',{'ticker':"Enter a ticker symbol above"})
		
def delete(request,stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,("Stock has been deleted"))
	return redirect(add_stock)


def about(request):
	return render(request,'about.html',{})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		for e in Stock.objects.all():
			if (e.ticker == request.POST['ticker']):
				print("Already exists")
				messages.error(request,"already exists")
				return redirect(add_stock)
		else:
			form = StockForm(request.POST or None)

			if form.is_valid():
				form.save()
				messages.success(request,("Stock has been added!"))
				return redirect('add_stock')
				

	else:	
		tickers = Stock.objects.all()
		output = []
		for tick in tickers:
			api_requests = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_979d9f9e018048b48d962c434b6cca00".format(str(tick)))

			try:
				api = json.loads(api_requests.content)
				output.append(api)

					#x = float(api['marketCap'])
			except Exception as e:
				api = "Error..."
		for dicts in output:
			dicts['latestPrice']=float(dicts['latestPrice'])
			dicts['week52Low']=float(dicts['week52Low'])
			dicts['marketCap']=float(dicts['marketCap'])
			if(dicts['week52Low'] / dicts['latestPrice'] > .65 ):
				dicts['signal']="Buy"
			else:
				dicts['signal']="Sell"

		return render(request,'add_stock.html',{'ticker':tickers,'output':output})




