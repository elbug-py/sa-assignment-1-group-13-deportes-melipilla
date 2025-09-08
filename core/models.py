import mongoengine as me

class Author(me.Document):
    name = me.StringField(required=True, max_length=200, unique=True)
    birthday = me.DateField()
    origin_country = me.StringField(max_length=100)
    description = me.StringField()
    image = me.StringField()

    def __str__(self):
        return self.name


class Book(me.Document):
    author = me.ReferenceField(Author, reverse_delete_rule=me.CASCADE, required=True)
    name = me.StringField(required=True, max_length=200)
    summary = me.StringField()
    publication_date = me.DateField()
    cover_image = me.StringField()
    meta = {
        'indexes': [
            {'fields': ['author', 'name'], 'unique': True}
        ]
    }

    def __str__(self):
        return self.name


class Review(me.Document):
    book = me.ReferenceField(Book, reverse_delete_rule=me.CASCADE, required=True)
    score = me.IntField(min_value=0, max_value=5, required=True)
    up_votes = me.IntField(default=0)


class Sale(me.Document):
    book = me.ReferenceField(Book, reverse_delete_rule=me.CASCADE, required=True)
    count = me.IntField(min_value=0, required=True)
    year = me.IntField(required=True)
    meta = {
        'indexes': [
            {'fields': ['book', 'year'], 'unique': True}
        ]
    }