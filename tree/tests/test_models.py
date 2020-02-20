from django.test import TestCase
from tree.models import Tree
import time
import logging


class TreeTestCase(TestCase):
    def setUp(self) -> None:
        parent = None
        for i in range(10):
            node = Tree.objects.create(name=f"Node {i}", parent=parent)
            for j in range(10):
                Tree.objects.create(name=f"Node {i}", parent=node)

    def test_children_list(self):
        children_list = Tree.objects.filter(parent__isnull=True).first().children_list()
        self.assertEqual(len(children_list), 10)

    def test_children_dict_list(self):
        instance = Tree.objects.filter(parent__isnull=True).first()
        children_dict_list = Tree.children_dict_list(instance_id=instance.pk)
        self.assertEqual(len(children_dict_list), instance.children.count())

    def test_get_tree(self):
        start_time = time.time()
        tree = Tree.get_tree()
        root_nodes = Tree.objects.filter(parent__isnull=True)

        self.assertListEqual([n.id for n in root_nodes], [n['id'] for n in tree])
        for root_node in root_nodes:
            tree_node = list(filter(lambda x: x['id'] == root_node.pk, tree))[0]
            self.assertListEqual(
                [n.id for n in root_node.children.all()],
                [n['id'] for n in tree_node['children']])

        logging.info(f"Tree generation time {time.time()-start_time}")

