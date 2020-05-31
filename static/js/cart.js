var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			console.log('User is not authenticated')

		}else{
			updateUserOrder(productId, action)
		}
	})
}

//send idproduct to the updateview
function updateUserOrder(productId, action){
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
			body:JSON.stringify({'productId':productId, 'action':action})
		})
    //this is the respone after sending the data which is the promess turn it to jason
		.then((response) => {
		   return response.json();
		})//reload the actual page after sendind data to the view
		.then((data) => {
		    location.reload()
		});
}
