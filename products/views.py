from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .models import Product, Factory

from .filters import FactoryFilter
from .tables import FactoryTable
from .forms import ProductForm


@login_required(login_url='../authen/')
def product_index(request):
    products = Product.objects.all().order_by("-product_reg_date")
    return render(request, 'product_index.html', {'products': products})


@login_required(login_url='/authen/')
def product_form(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        selected_factory_id = int(request.POST['factory'])
        selected_factory = Factory.objects.filter(id=selected_factory_id).order_by("-factory_reg_date")[0]
        selected_product_name = request.POST['product-name']
        form.product_name = selected_product_name
        updated_request = request.POST.copy()
        updated_request.update({'product_name': selected_product_name})
        updated_form = ProductForm(updated_request)

        if updated_form.is_valid():
            product = updated_form.save(commit=False)
            product.product_creating_user = request.user
            product.product_factory_name = selected_factory
            updated_form.save()
            return render(request, 'product_form.html', {'form': form})
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})


class FactoryTableModalView(SingleTableMixin, FilterView):
    table_class = FactoryTable
    queryset = Factory.objects.all().order_by("-factory_reg_date")
    filterset_class = FactoryFilter
    paginate_by = 5

    def get_template_names(self):
        if self.request.htmx.target == "show-factory-modal-here":
            template_name = "modal/factory_modal.html"
        else:
            template_name = "modal/factory_modal_partial.html"
        return template_name
