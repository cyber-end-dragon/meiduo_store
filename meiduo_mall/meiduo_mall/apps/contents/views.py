from django.shortcuts import render
from django.views import View
from collections import OrderedDict

from goods.models import GoodsChannelGroup, GoodsChannel, GoodsCategory
from contents.models import ContentCategory, Content
from contents.utils import get_categories
# Create your views here.


class IndexView(View):

    def get(self, request):
        # 查询商品频道和分类
        categories = get_categories()

        # 广告数据
        contents = OrderedDict()
        content_categories = ContentCategory.objects.all()
        for content_category in content_categories:
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents
        }


        return render(request, 'index.html', context)