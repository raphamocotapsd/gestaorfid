from django.shortcuts import render
from .forms import OrdemServicoForm
from .models import OrdemServico


def home(request):
    if request.method == "GET":
        lista = OrdemServico.objects.all()

        context = {
            'lista': lista
        }
        return render(request, "home.html", context)
    else:
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            form.save()


def os(request):
    if request.method == "GET":
        form = OrdemServicoForm()
        context = {
            'form': form
        }
        return render(request, 'formulario_modelform.html', context=context)
    elif request.method == "POST":
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            form.save()
            form = OrdemServicoForm()
        else:
            context = {
                'form': form
            }
            return render(request, 'formulario_modelform.html', context=context)
    else:
        form = OrdemServicoForm()

    context = {
        'form': form
    }
    return render(request, 'formulario_modelform.html', context=context)
