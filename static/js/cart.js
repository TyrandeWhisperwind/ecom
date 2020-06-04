var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action

		try {
			var val= document.getElementById('qty').value
		}
			catch(err) {
  		val=1
		}

		try {
  	var val2= document.getElementById('qty2').value
		}
			catch(err) {
  		val2=1
		}
			if (val != 1)
			{valu= val}
			else{
			valu=val2
			}


try {
		var scolorsize= document.getElementById('selectbox')
		var colorsize=scolorsize.options[scolorsize.selectedIndex].value

	}
		catch(err) {
		var colorsize = this.dataset.color
	}

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action,valu,colorsize)

		}else{
			updateUserOrder(productId, action,valu,colorsize)
		}
	})
}

//send idproduct to the updateview
function updateUserOrder(productId, action,val,colorsize){
	console.log('User is authenticated, sending data...')
    //url and the view to update order
		var url = '/update_item/'
    //send data we use fetch with url and method and content type which is jason and then the data
		fetch(url, {
			method:'POST',//post data
			headers:{
				'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
			},//the body is the data to send to the backend as object
      //cant send it as object we need to stringfy it
			body:JSON.stringify({'productId':productId, 'action':action,'val':val,'colorsize':colorsize})
		})
    //this is the respone after sending the data which is the promess turn it to jason
		.then((response) => {return response.json();})//reload the actual page after sendind data to the vie
		.then((data) => { location.reload()});}


function addCookieItem(productId, action,valu,colorsize){

		if (action == 'add'){

			if (cart[productId] == undefined){
				cart[productId] ={}
				cart[productId][colorsize] =parseInt(valu)
			}else{
							if (cart[productId][colorsize]  == undefined){
								cart[productId][colorsize] =parseInt(valu)
							}else {
								cart[productId][colorsize] += parseInt(valu)
							}
			}
		}
		if (action == 'remove'){
			console.log(	cart[productId][colorsize]);
			cart[productId][colorsize] -= 1
			if (cart[productId][colorsize]<= 0){
				console.log('Item should be deleted')
				delete cart[productId][colorsize];
			}
		}
		console.log('CART:', cart)
		document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
		// so to get the totall and show it in the cart icon
		//not best way, we can use more javascript or rest apis
		location.reload()

}
