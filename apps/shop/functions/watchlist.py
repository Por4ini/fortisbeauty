from project import settings 


class WatchList():
    def __init__(self, request):
        self.session = request.session
        watchlist = self.session.get(settings.WATCHLIST_SESSION_ID)
        if not watchlist:
            self.session[settings.WATCHLIST_SESSION_ID] = []
            watchlist = self.session[settings.WATCHLIST_SESSION_ID]
        self.watchlist = watchlist

    def __iter__(self):
        for item in self.watchlist:
            yield item

    def add(self, product_id):
        if product_id in self.watchlist:
            self.watchlist.remove(product_id)
        self.watchlist.insert(0, product_id)
        self.session[settings.WATCHLIST_SESSION_ID] = self.watchlist

    def remove(self, id):
        self.watchlist.remove(id)
        self.session[settings.WATCHLIST_SESSION_ID] =self.watchlist
        self.save()

    def clear(self):
        del self.session[settings.WATCHLIST_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True