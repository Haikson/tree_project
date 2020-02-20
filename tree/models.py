from collections import defaultdict

from django.db import models


class Tree(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name="Родитель", related_name='children')
    name = models.CharField(max_length=255, verbose_name="Название")

    def children_list(self):
        """
        Get children as list of objects
        :return:
        """
        return list(self.children.all())

    @classmethod
    def children_dict_list(cls, instance_id):
        """
        Get object's children as list of dicts
        :param instance_id: parent instance id
        :return: list of dicts [{"id": int, "name": str}]
        """
        children = cls.objects.filter(parent_id=instance_id)
        return [
            {
                "id": child.pk,
                "name": child.name
            }
            for child in children
        ]

    @classmethod
    def get_tree(cls, root_node=None):
        """
        Get tree of objects from root node with all descendants
        Executes query to database for each node
        :param root_node: Tree object
        :type root_node: Tree
        :return: list of dicts [{"id": int, "name": str, "children": list}]
        """

        nodes = cls.objects.filter(parent=root_node).prefetch_related("children")
        return [
            {
                "id": node.pk,
                "name": node.name,
                "children": cls.get_tree(root_node=node)
            } for node in nodes
        ]

    def __str__(self):
        return self.name



