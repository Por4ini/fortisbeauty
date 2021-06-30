def news(request):
    args={}
    args['news']=newsPost.objects.all()
    return render(request, 'shop/news.html', args)

def newsPostPage(request, year, month, day, slug):
    args={}
    args['post'] = get_object_or_404(newsPost, upload_date__year=year, upload_date__month=month, upload_date__day=day, slug=slug)
    args['images'] = newsPostImages.objects.filter(foreign_key=args['post'])
    return render(request, 'shop/news_post.html', args)





def fast_call(request):
    args={}
    if request.method == "POST":
        data = json.loads(json.loads(request.body.decode()))
        object = CallMe()
        msg = 'Запрос перезвонить %s\nИмя: %s\nТелефон: %s' %(time.strftime("%Y-%m-%d %H:%M"), data['first_name'], data['phone'])
        import urllib.request
        import urllib.parse
        msg = urllib.parse.quote(msg)

        url = "https://api.telegram.org/bot817785032:AAG-Q3s8wRhyZbkoJScSPvE2XDrCVlgZKKA/sendMessage?chat_id=-1001490724377&text="+msg
        contents = urllib.request.urlopen(url).read()
        # bot = telegram.Bot(token='817785032:AAG-Q3s8wRhyZbkoJScSPvE2XDrCVlgZKKA')
        # status = bot.send_message(chat_id="-1001490724377", text=msg, parse_mode=telegram.ParseMode.HTML)

        for key in data.keys():
            setattr(object, key, data[key])
        object.save(object)
    response = {'msg' : "Мы очень скоро Вам позвоним" }
    return JsonResponse(response)


def letter_to_director(request):
    if request.method == "POST":
        # Get JSON data
        data = json.loads(json.loads(request.body.decode()))
        # Save message
        object = letterToDirector()
        object.first_name =  data['full_name']
        object.phone = data['phone']
        object.email = data['email']
        object.text =  data['text']
        object.save(object)
        # Telegram: create message
        msg =  'Письмо директору ' + str(time.strftime("%Y-%m-%d %H:%M")) + '\n'
        msg += 'ФИО: ' + data['full_name'] + 'Телефон: %s"' % (data['phone']) + '\n'
        msg += 'email: ' + data['email'] + '\n'
        msg += 'Текст письма: ' + data['text']+ '\n'

        import urllib.request
        import urllib.parse
        msg = urllib.parse.quote(msg)

        url = "https://api.telegram.org/bot817785032:AAG-Q3s8wRhyZbkoJScSPvE2XDrCVlgZKKA/sendMessage?chat_id=-1001490724377&text=" + msg
        contents = urllib.request.urlopen(url).read()
        # Telegram: send to chanel

        # bot = telegram.Bot(token='817785032:AAG-Q3s8wRhyZbkoJScSPvE2XDrCVlgZKKA')
        # status = bot.send_message(chat_id="-1001490724377", text=msg, parse_mode=telegram.ParseMode.HTML)
        # Response text
    response = {'msg' : "Письмо отправлено директору" }
    return JsonResponse(response)