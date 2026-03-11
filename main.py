import uvicorn
from  fastapi import  FastAPI
from  myproject.api import users,product,review,order,contact,courier,category,address,store,auth

glovo_app = FastAPI(title='Glovo', debug=True)
glovo_app.include_router(users.user_router)
glovo_app.include_router(product.product_router)
glovo_app.include_router(review.review_router)
glovo_app.include_router(contact.contact_router)
glovo_app.include_router(store.store_router)
glovo_app.include_router(category.category_router)
glovo_app.include_router(courier.courier_router)
glovo_app.include_router(address.address_router)
glovo_app.include_router(order.order_router)
glovo_app.include_router(auth.auth_router)

if __name__ == '__main__':
    uvicorn.run(glovo_app, host='127.0.0.1', port=8000)