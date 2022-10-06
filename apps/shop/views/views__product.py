from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.core.cache import cache
from django.db.models import F, Avg
from django.http import HttpResponse
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from apps.shop.models import Product, Variant, Comment
from apps.shop.serializers import ProductSerializer, ProductPageVariantsSerializer, ProductPageSerializer, ProductCategorySerializer
from apps.shop.forms import CommentForm, QuestionForm, ReplyForm
from apps.shop.functions import WatchList
from apps.user.forms.forms__auth import LoginForm
from apps.core.functions import send_telegeram
import json






@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ViewSet):
    kwargs = {}


    def get_schema(self):

        return json.dumps({
                "@context": "https://schema.org/",
                "@type": "Product",
                "sku": self.variant.code,
                "name": self.product.name,
                "image": ['https://fortisbeauty.store' + image.image_thmb['l']['path'] for image in self.variant.images.all() if image.image_thmb.get('l')],
                "description": ''.join([item for item in [
                    self.product.description, 
                    self.product.prescription, 
                    self.product.application, 
                    self.product.composition
                ] if item != None]),

            
                "sku": self.variant.code,
                "brand": {
                    "@type": "Brand",
                    "name": self.product.brand.name
                },

                "review": [{
                    "@type": "Review",
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": comment.rate
                    },
                    "name": ' '.join([item for item in [self.product.name, self.variant.value] if item != None]),
                    "author": {
                        "@type": "Person",
                        "name": ' '.join([item for item in [comment.user.first_name, comment.user.last_name] if item != None])
                    },
                    "datePublished": comment.date.strftime("%Y-%m-%d"),
                    "reviewBody": comment.text,
                    "publisher": {
                        "@type": "Organization",
                        "name": "FortisBeauty"
                    }
                } for comment in self.comments],

            
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": list(self.comments.aggregate(Avg('rate')).values())[0],
                    "reviewCount": self.product.views,
                },
                "offers": {
                    "@type": "Offer",
                    "url": "https://fortisbeauty.store" + self.variant.get_absolute_url(),
                    "priceCurrency": "UAH",
                    "price": self.variant.price,
                    "itemCondition": "https://schema.org/NewCondition",
                    "availability": "https://schema.org/InStock"
                }
            }, indent=4).encode('utf8').decode('unicode-escape')


    def add_to_watchlist(self, request, product):
        watchlist = WatchList(request)
        watchlist.add(product)


    def get_comments(self, product):
        self.comments =  Comment.objects.filter(product=product, type="COMMENT")
        comments = render_to_string('shop/product/comments/comments__list.html', {'type' : 'COMMENT', 'comments' : self.comments})
        return comments

    def get_questions(self, product):
        self.questions = Comment.objects.filter(product=product, type="QUESTION")
        questions = render_to_string('shop/product/comments/comments__list.html', {'type' : 'QUESTION','comments' : self.questions})
        return questions


    def update_views_qty(self, product_id, variant_id=None):
        Product.objects.filter(id=product_id).update(views=F('views')+1)
        if variant_id:
            Variant.objects.filter(id=variant_id).update(views=F('views')+1)


    def set_objects(self, **kwargs):
        product_id = kwargs.get('product_id')
        variant_id = kwargs.get('variant_id')
        self.update_views_qty(product_id, variant_id)
        self.product = Product.objects.filter(id=product_id).prefetch_related(
            'category','brand','variant','variant__images'
        ).first()
        self.variants = self.product.variant.all().order_by('-price')
        if variant_id:
            self.variant = self.product.variant.filter(id=variant_id).first()
        else:
            self.variant = self.product.variant.first()

        self.comments =  Comment.objects.filter(product=self.product, type="COMMENT")
        self.questions = Comment.objects.filter(product=self.product, type="QUESTION")

        return self


    def get_tempalate(self, request):
        categories = self.product.category.get_ancestors(include_self=True)
        context = {
            'comments' :   self.get_comments(self.product),
            'questions' :  self.get_questions(self.product),
            'product' :    ProductPageSerializer(self.product).data,
            'variants' :   ProductPageVariantsSerializer(self.variants, many=True).data,
            'variant'  :   ProductPageVariantsSerializer(self.variant).data,
            'variant_id' : self.variant.id,
            'categories' : ProductCategorySerializer(categories, many=True).data,
            'schema' :     self.get_schema(),
        }
        return render_to_string('shop/product/product.html', context=context, request=request)



    def send_to_telegram(self, product, comment_type):
        title = 'Коментар' if comment_type == "COMMENT" else "Запитання"
        url = reverse('admin:%s_%s_change' % (product._meta.app_label, product._meta.model_name), args=[force_text(product.pk)])
        msg = [
             title + '\n',
            'https://fortisbeauty.store' + url,
            'https://fortisbeauty.store' + product.get_absolute_url(),
        ]
        send_telegeram(msg)

        


    def get(self, request, **kwargs):
        path = request.path
        user = request.user
        
        self.add_to_watchlist(request, kwargs['product_id'])
       
        template = cache.get(path)

    
        if template is None or user.is_authenticated:
            self.set_objects(**kwargs)
            template = self.get_tempalate(request)
            if user.is_authenticated:
                return HttpResponse(template, content_type="text/html")
            cache.set(path, template, 60*60*24*365)
        return HttpResponse(template, content_type="text/html")
       


    
    def post(self, request, **kwargs):
        self.set_objects(**kwargs)
        product = ProductPageSerializer(self.product).data
        variant = ProductPageVariantsSerializer(self.variant).data
        variants_serialized = ProductPageVariantsSerializer(self.variants, many=True).data
        return Response({
            'actions' : render_to_string("shop/product/actions.html", {'product' : product, "variants" : variants_serialized, "variant" : variant}),
            'galery'  : render_to_string("shop/product/galery/galery.html", {"variant" : variant}),
        })


    def fetch_comments(self, request, product_id):
        self.product = Product.objects.get(id=product_id)
        return Response({'comments' : self.get_comments(self.product)})

    def fetch_serie(self, request, product_id):
        product =       Product.objects.get(id=product_id)
        serieProducts = Product.objects.filter(serie=product.serie)
        serialized =    ProductSerializer(serieProducts, many=True).data
        html = render_to_string('shop/product/serie/serie__products.html', {'products' : serialized, 'serie' : product.serie.name})
        return Response({'serie' : html})

    




    def comment_form(self, request, product_id, comment_type="COMMENT"):
        product = Product.objects.get(id=product_id)
        self.product = product
        if request.user.is_authenticated:
            if comment_type == 'COMMENT':
                ModelForm = CommentForm
                heading = f'Коментар до {product.human if product.human else product.name}'
            else:
                ModelForm =  QuestionForm
                heading = f'Запитання до {product.human if product.human else product.name}'
       
            if request.method == 'POST':
                form = ModelForm(data=request.POST)
                if form.is_valid():
                    form.save()
                    if comment_type == 'COMMENT':
                        resp = {'comments' : self.get_comments(product)}
                    else:
                        resp = {'questions' : self.get_questions(product)}
                    self.send_to_telegram(product, comment_type)
                    return Response(resp)
                    
                else:
                    print(form.errors)

            form = ModelForm(initial={
                'type' : comment_type,
                'user' : request.user,
                'product' : product.id,
            })
            template = render_to_string('shop/product/comments/comment_form.html', {'form' : form, 'user' : request.user, 'url' : request.path})
        else:
            form_type = 'залишити коментар' if comment_type == 'COMMENT' else 'задати запитання'
            url = product.variant.first().get_absolute_url()
            template = render_to_string('user/login__form.html', {
                'form' : LoginForm(), 
                'url' : f'/login/?redirect={url}'
            }) 
            heading = f'Для того щоб {form_type} потрібно авторизуватись'
        return Response({'form' : template, 'heading' : heading})


    def reply_form(self, request, comment_id, parent_id=None):
        
        comment = Comment.objects.get(id=comment_id)
        self.set_objects(product_id=comment.product.id)

        if (request.method == 'POST'):
            form = ReplyForm(data=request.POST)
            if form.is_valid():
                form.save()
                resp = {
                    'comments' : self.get_comments(comment.product)
                }
                cache.delete(comment.product.get_absolute_url())
                self.send_to_telegram(self, comment.product, comment.type)
                return Response(resp)

        form = ReplyForm(initial={
            'parent' : parent_id,
            'comment' : comment_id,
            'user' : request.user.id,
        })
        template = render_to_string('shop/product/comments/comment_reply_form.html', {'form' : form, 'user' : request.user, 'url' : request.path})
        return Response({'form' : template, 'heading' : 'Відповідь на коментар'})
        











class WatchListView(viewsets.ViewSet):
    def check_delted(self, watchlist, products):
        if products.count() > len(watchlist.watchlist):
            for product in products:
                if product.id not in watchlist.watchlist:
                    watchlist.remove(product.id)
        return watchlist.watchlist

    def get(self, request):
        watchlist_products, exclude = [], []
        watchlist = WatchList(request)
        products = Product.objects.filter(pk__in=watchlist.watchlist)
        
        for pk in self.check_delted(watchlist, products):
            product = products.filter(pk=pk).first()
            if product:
                watchlist_products.append(product)


        return Response({
            'watchlist' : render_to_string('shop/home/home__products.html', {
                'heading'  : 'Переглянуті товари',
                'products' : ProductSerializer(watchlist_products, many=True).data,
            })
        })






def product_qr(request, slug):
    args = {}
    args['product'] = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_qr.html', args)





class TemplatesView(viewsets.ViewSet):
    def buyer_info(self, request):
        return Response({'template' : render_to_string('shop/product/product__aditional__info.html')})