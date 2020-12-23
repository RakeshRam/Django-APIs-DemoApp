from faker import Faker

from core.models import Author, Award, AwardRecord, Publisher, Book

# from util.fake_data_creator import create_awards, create_awards_records 
# from util.fake_data_creator import create_publishers, create_authors, create_books

fake = Faker()


def create_awards(n=25):
    CATEGORY_CHOICE = (('Doc', 'Documentary'),
                        ('Ent', 'Entertainment'),
                        ('Sci-Fi', 'Science-Fiction'),
                        ('Nov', 'Novel'))
    for _ in range(n):
        award = Award()
        award.name = fake.name()
        award.country = fake.country()
        award.is_active = fake.boolean()
        award.category = fake.random_element(CATEGORY_CHOICE)
        award.save()

def create_awards_records(n=30):
    awards = Award.objects.all()
    for _ in range(n):
        award_record = AwardRecord()
        award_record.name =  fake.random_element(awards)
        award_record.awarded_on = fake.date()
        award_record.save()

def create_publishers(n=25):
    award_records = AwardRecord.objects.all()
    for _ in range(n):
        publisher = Publisher()
        publisher.name = fake.company()
        publisher.is_active = fake.boolean()
        publisher.save()
        publisher.award.add(*fake.random_elements(award_records))
        publisher.save()

def create_authors(n=50):
    award_records = AwardRecord.objects.all()
    for _ in range(n):
        author = Author()
        author.name = fake.name()
        author.age = fake.random.randint(18, 65)
        author.save()
        author.award.add(*fake.random_elements(award_records))
        author.save()

def create_books(n=100):
    award_records = AwardRecord.objects.all()
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    for _ in range(n):
        book = Book()
        book.name = fake.catch_phrase()
        book.publisher = fake.random_element(publishers)
        book.save()
        book.author.add(*fake.random_elements(authors))
        book.award.add(*fake.random_elements(award_records))
        book.save()

