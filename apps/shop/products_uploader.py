from openpyxl import load_workbook

# PRODUCT DATA
SelfFields = [
    {'name':'name',        'table_name':'Артикул'},
    {'name':'human',       'table_name':'Человеческое неазвание'},
    {'name':'application', 'table_name':'Применение'},
    {'name':'composition', 'table_name':'Состав'},
    {'name':'description', 'table_name':'Описание'},
]

ForeignKeys = {
    # BRANS
    'brand' : {
        'model' : 'Brand',
        'fieds' : [
            {'name':'name', 'table_name':'Бренд', 'type':'CharField'},
        ],
        'chlids' : [
            'model' : 'BrandSeries',
            'fileds' : [
                {'name':'name', 'table_name':'Серия бренда', 'type':'CharField'},
            ],
            'selector' : ['name'],
        ],
        'selector' : ['name'],
    },
    # VARIANT TYPE
    'unit' : {
        'model' : 'VariantType',
        'fieds' : [
            {'name':'name', 'table_name':'Тип варината',      'type':'CharField'},
            {'name':'unit', 'table_name':'Еденица измерения', 'type':'CharField'},
        ],
        'selector' : ['name'],
    },
    # COUNTRY
    'country' : {
        'model' : 'Countries',
        'fieds' : [
            {'name':'name', 'table_name':'Страна', 'type':'CharField'},
        ],
        'selector' : ['name'],
    }
}

ForeignKeysRecurcion = {
    # CATEGORY
    'category' : {
        'model' : 'Categories',
        'levels' : [
            'fileds' : [
                {'name':'name',                    'table_name':'Категория уровень 1',               'type':'CharField'},
                {'name':'name_catalogue',          'table_name':'Название категории для каталога 1', 'type':'CharField'},
                {'name':'google_product_category', 'table_name':'Номер категории Google 1',          'type':'ForeignKey', 'selector':['id']},
            ],
            'fileds' : [
                {'name':'name',                    'table_name':'Категория уровень 2',               'type':'CharField'},
                {'name':'name_catalogue',          'table_name':'Название категории для каталога 2', 'type':'CharField'},
                {'name':'google_product_category', 'table_name':'Номер категории Google 2',          'type':'ForeignKey', 'selector':['id']},
            ],
            'fileds' : [
                {'name':'name',                    'table_name':'Категория уровень 3',               'type':'CharField'},
                {'name':'name_catalogue',          'table_name':'Название категории для каталога 3', 'type':'CharField'},
                {'name':'google_product_category', 'table_name':'Номер категории Google 3',          'type':'ForeignKey', 'selector':['id']},
            ],
        ]
    }
}

Variants = {
    'country' : {
        'model' : 'Variant',
        'fieds' : [
            {'name':'name',           'table_name':'Значение варианта', 'type':'CharField'},
            {'name':'price', '         table_name':'Цена розничная',    'type':'PositiveIntegerField'},
            {'name':'whoosale_price', 'table_name':'Цена розничная',    'type':'PositiveIntegerField'},
            {'name':'barcode',        'table_name':'Штрихкод',          'type':'CharField'},
        ],
        'parent_selector' : ['name']
        'selector' :        ['parent', 'value']
    }
}




