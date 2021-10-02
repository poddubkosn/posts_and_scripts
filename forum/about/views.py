from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super().get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым
        #  значением

        context['some_data'] = 'Я изучаю python!'
        return context


# class AboutTechView(TemplateView):
#     template_name = 'about/tech.html'
