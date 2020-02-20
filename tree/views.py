from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from tree.models import Tree


class TreeView(TemplateView):
    template_name = 'tree.html'

    def get_context_data(self):
        context = super(TreeView, self).get_context_data()
        context['tree'] = Tree.get_tree()
        return context


class TreeJSONView(View):
    def get(self, request):
        return HttpResponse(Tree.get_tree(), content_type='application/json')