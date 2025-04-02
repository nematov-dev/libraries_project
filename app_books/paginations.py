from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 10  # Har bir sahifada ko'rsatiladigan kitoblar soni
    page_size_query_param = 'page_size'  # URL orqali sahifa o‘lchamini o‘zgartirish
    max_page_size = 100  # Maksimal sahifa o‘lchami
