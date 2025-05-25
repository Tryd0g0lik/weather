# Weather

Приложение имеет два модуля:
- 'dashboard' - регистрация и логирование пользователя
- 'weather' - сам сервис прогноза погоды.

# DASHBOARD
Своя модель пользователя '`Users`' построенная на '`AbstractUser`'.\

## Регистрация пользователей
*`dashboard/views::UsersViewSet.create`* проходит по умолчанию Django.

## Login пользователя
*`dashboard/views::UsersViewSet.login_user`* проходит по умолчанию Django, плюс\
пользователь получает базовые '`latitude`' & '`longitude`'.
**Note**: *Добавлены и к пользователю, чтоб  забронировать возможность \
расширения модели пользователя*.\
### '`latitude`' & '`longitude`'
https://members.ip-api.com/ \
**Note**: *Сервис платный. Но, бесплатный тариф позволяет 50 d месяц*.\
Делая запрос на логирование, из браузера получаем '`IP`' адрес.\
По '`IP`' адресу получаем примерные '`latitude`' & '`longitude`' нахождения провайдера (у пользователя):\
```JS
{'status': 'success', 
  'country': 'Россия', 
  'countryCode': 'RU', 
  'region': 'MOW', 
  'regionName': 'Москва', 
  'city': 'Москва', 
  'zip': '', 
  'lat': 55.8049, 'lon': 37.5207,
  'timezone': 'Europe/Moscow',
  'isp': '"Domain names registrar REG.RU", Ltd', 
  'org': '"Domain names registrar REG.RU", Ltd', 
  'as': 'AS197695 Domain names registrar REG.RU, Ltd', 
  'query': '83.166.245.197'}
```
**Note**: *'`dashboard/views.py`' IP "`83.166.245.197`" изменить на представленный выше '`user_ip_address`'*.\

Для примера:
- UTC +7 моё положение;
- UTC +3 есть основной офис моего провайдера.

В первичное открытие сервиса, ориентируясь на данные '`latitude`' & '`longitude`', \
пользователь получает прогноз.

## JWT для пользователя
- '`settings.SIMPLE_JWT`';
- '`settings.REST_FRAMEWORK`' настройки по умолчанию

## О разном
В '`settings`':
 - База данных настроена на '`Postgres`'; 
 - Проверка '`username`' на дублирование; 
 - Hash паролей и проверка при авторизации;
 - '`LANGUAGE_CODE`' = '`ru`'; 
 - '`TIME_ZONE`' = '`Asia/Krasnoyarsk`'; 
 - CORS и '`CSRF_TRUSTED_ORIGINS`';
 - '`WEBPACK_LOADER`'

'`help_text`' настройка '`LANGUAGE_CODE`' совершается перевод строки. \
Чаще всего видно при использовании форм django. '`<label>`' & '`help_text`' при \
публикации - **ПЕРЕВОДИТСЯ АВТОМАТОМ** на язык из указанной зоны.

