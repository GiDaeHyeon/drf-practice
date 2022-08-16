import os
import random
import django
import requests


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRFPractice.settings')
django.setup()

from univ_interests.models import User, Country, University, UniversityPreference


class CollectData:
    def __init__(self):
        resp = requests.get('http://universities.hipolabs.com/search')

        if resp.status_code != 200:
            raise ConnectionError

        self.data = resp.json()

    def collect_country_data(self):
        countries_set = set([(d.get('country'), d.get('alpha_two_code')) for d in self.data])
        countries = [Country(code=code, name=name) for name, code in countries_set]

        if len(countries) != 204:
            raise ValueError

        try:
            Country.objects.bulk_create(countries, batch_size=512, ignore_conflicts=True)
        except Exception as e:
            # TODO 예외 처리
            print(e)
            return False
        else:
            return True

    def collect_university_data(self):
        universities = [
            University(
                country=Country.objects.get(name=d.get('country')) if d.get('country', None) is not None else None,
                webpage=d.get('web_pages')[0] if d.get('web_pages', None) is not None else None,
                name=d.get('name') if d.get('name', None) is not None else None
            ) for d in self.data
        ]

        try:
            University.objects.bulk_create(universities, batch_size=512, ignore_conflicts=True)
        except Exception as e:
            # TODO 예외 처리
            print(e)
            return False
        else:
            return True


def create_user_dummy_data():
    users_dummies = [
        User(
            email=f"test{num}@gmail.com",
            password=f"{num}",
            nickname=f"test{num}"
        ) for num in range(1, 1001)
    ]
    try:
        User.objects.bulk_create(users_dummies, batch_size=512, ignore_conflicts=True)
    except Exception as e:
        # TODO 예외 처리
        print(e)
        return False
    else:
        return True


def create_university_preference_data():
    users = User.objects.all()
    preferences = []
    for user in users:
        for _ in range(20):
            university = University.objects.order_by('id')[:50][random.randint(0, 49)]
            preference = UniversityPreference(
                university=university,
                user=user,
            )
            preferences.append(preference)
    try:
        UniversityPreference.objects.bulk_create(preferences, batch_size=512, ignore_conflicts=True)
    except Exception as e:
        # TODO 예외 처리
        print(e)
        return False
    else:
        return True


if __name__ == '__main__':
    collector = CollectData()
    a = collector.collect_country_data()
    b = collector.collect_university_data()
    create_user_dummy_data()
    create_university_preference_data()
