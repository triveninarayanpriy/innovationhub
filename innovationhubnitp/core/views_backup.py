from django.shortcuts import render
from django.views.generic import TemplateView
from .models import BentoCard


class HomeView(TemplateView):
    """Homepage view with bento cards."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bento_cards'] = BentoCard.objects.filter(is_active=True)
        return context


def home(request):
    """Simple function-based view for homepage."""
    context = {
        'bento_cards': BentoCard.objects.filter(is_active=True)
    }
    return render(request, 'home.html', context)
