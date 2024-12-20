from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import AgriculturalProduct, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .forms import AgriculturalProductForm
from .forms import CommentForm
from django.utils.timezone import localtime
import random
from random import sample
from django.http import JsonResponse
from .models import Purchase
from django.contrib import messages






class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name','email']
    template_name = 'myapp/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def profile_view(request):
    user = request.user
    # 这里可以根据需要从数据库中获取更多关于用户的信息，比如农业产品的购买记录等
    context = {
        'user': user,
        # 'additional_info': ...  # 可能的额外信息
    }
    return render(request, 'myapp/profile.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 登录新用户
            login(request, user)
            return redirect('login')  #
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('recommendation')  #
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')




class ProductListView(ListView):
    model = AgriculturalProduct
    context_object_name = 'products'
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 添加所有分类到上下文
        context['categories'] = Category.objects.all()

        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = AgriculturalProduct.objects.filter(category=self.object)
        return context

def some_view(request):
    categories = Category.objects.all()  # 获取所有分类
    return render(request, 'base.html', {'categories': categories})

def home(request):
   return render(request, 'home.html',{'name': 'home'})

def product_create(request):
    if request.method == 'POST':
        form = AgriculturalProductForm(request.POST, request.FILES)  # 添加 request.FILES
        if form.is_valid():
            form.save()
            return redirect('product_list')  # 假设你有一个产品列表的 URL
    else:
        form = AgriculturalProductForm()
    return render(request, 'product_form.html', {'form': form})


def product_list(request):
    categories = Category.objects.all()
    products = list(AgriculturalProduct.objects.all())
    random.shuffle(products)  # 随机排序

    return render(request, 'your_template.html', {
        'products': products,
        'categories': categories
    })


def product_search(request):
    query = request.GET.get('q')  # 获取搜索查询
    products = AgriculturalProduct.objects.all()  # 获取所有产品

    if query:
        products = products.filter(name__icontains=query)  # 根据名称过滤产品

    return render(request, 'products/product_search.html', {'products': products, 'query': query})


def product_detail(request, pk):
    product = get_object_or_404(AgriculturalProduct, pk=pk)

    # Increment click_count
    product.click_count += 1
    product.save()
    comments = product.comments.all()  # 获取该商品的所有评论

    # 转换评论的创建时间为亚洲/上海时区的本地时间
    for comment in comments:
        comment.created_at = localtime(comment.created_at)

    # 如果请求方法为POST，则尝试处理评论表单
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # 将当前登录的用户赋值给评论的user字段
            comment.agricultural_product = product  # 将当前商品赋值给评论的商品字段
            comment.save()
            return redirect('product_detail', pk=pk)  # 提交成功后重定向回商品详情页
    else:
        form = CommentForm()

    return render(request, 'products/product_detail.html', {'product': product, 'form': form, 'comments': comments})


def recommendation_view(request):
    products = AgriculturalProduct.objects.all()

    # 示范用户点击次数最高的前6个商品
    recommended_products = AgriculturalProduct.objects.order_by('-click_count')[:6]

    # 如果没有推荐商品则随机选择6个商品
    if recommended_products.count() == 0:
        if products.count() > 6:
            recommended_products = sample(list(products), 6)
        else:
            recommended_products = products

    # 获取所有类别
    categories = Category.objects.all()

    return render(request, 'myapp/recommendation.html', {
        'recommended_products': recommended_products,
        'categories': categories
    })

def product_suggestion(request):
    query = request.GET.get('q', '')
    suggestions = AgriculturalProduct.objects.filter(name__icontains=query)[:5]  # 限制返回前5个结果
    results = [{'id': product.id, 'name': product.name} for product in suggestions]
    return JsonResponse(results, safe=False)

def about(request):
   return render(request, 'about.html',{'name': 'about'})



@login_required
def purchase_product(request, product_id):
    product = get_object_or_404(AgriculturalProduct, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # 从表单获取数量，默认为1
        purchase = Purchase(user=request.user, agricultural_product=product, quantity=quantity)
        purchase.save()

        # 可选：重定向到成功页面或产品详细页面
        return redirect('purchase_success')

    return render(request, 'products/product_detail.html', {'product': product})

def purchase_success(request):
    return render(request, 'purchase/purchase_success.html')

@login_required
def user_orders(request):
    orders = Purchase.objects.filter(user=request.user)  # 获取当前用户的所有订单
    return render(request, 'order/user_orders.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Purchase, id=order_id, user=request.user)  # 确保用户只能取消自己的订单
    if not order.is_cancelled:  # 确保订单未被取消
        order.is_cancelled = True
        order.save()
        messages.success(request, '订单已成功取消。')
    else:
        messages.warning(request, '该订单已被取消。')
    return redirect('my_orders')  # 重定向回我的订单页面

@login_required
def create_purchase(request, product_id):
    product = get_object_or_404(AgriculturalProduct, id=product_id)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        # 创建订单并存储地址信息
        Purchase.objects.create(
            user=request.user,
            agricultural_product=product,
            quantity=quantity,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            zip_code=zip_code
        )

        messages.success(request, f'您已成功购买 {quantity} 个 {product.name}!')
        return redirect('purchase_success')  # 重定向到我的订单页面

    return render(request, 'order/create_order.html', {'product': product})