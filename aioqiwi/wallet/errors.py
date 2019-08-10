# parsed from https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html?http#errors

qiwiErrorIds = {
    0:    "OK",
    3:    "Техническая ошибка, нельзя отправить запрос провайдеру",
    4:    "Неверный формат счета/телефона",
    5:    "Номер не принадлежит оператору",
    8:    "Прием платежа запрещен по техническим причинам",
    131:  "Платежи на выбранного провайдера запрещено проводить из данной страны.",
    202:  "Ошибка в параметрах запроса",
    220:  "Недостаточно средств",
    241:  "Сумма платежа меньше минимальной",
    242:  "Сумма платежа больше максимальной",
    319:  "Платеж невозможен",
    500:  "По техническим причинам этот платеж не может быть выполнен."
          " Для совершения платежа обратитесь, пожалуйста, в свой обслуживающий банк",
    522:  "Неверный номер или срок действия карты получателя",
    547:  "Ошибка в сроке действия карты получателя",
    548:  "Истек срок действия карты получателя",
    561:  "Платеж отвергнут оператором банка получателя",
    702:  "Платеж не проведен из-за ограничений у получателя. Подробности по телефону: 8-800-707-77-59",
    705:  "Ежемесячный лимит платежей и переводов для статуса Стандарт - 200 000 р."
          " Для увеличения лимита пройдите идентификацию.",
    746:  "Превышен лимит по платежам в пользу провайдера",
    852:  "Превышен лимит по платежам в пользу провайдера",
    893:  "Срок действия перевода истек",
    1050: "Превышен лимит на операции, либо превышен дневной лимит на переводы на карты Visa/MasterCard",
}

httpRequestErrors = {
    400: "Ошибка синтаксиса запроса (неправильный формат данных)",
    401: "Неверный токен или истек срок действия токена",
    403: "Нет прав на данный запрос (недостаточно разрешений у токена)",
    404: "Не найдена транзакция или отсутствуют платежи с указанными признаками",
    422: "Неправильно указаны домен/подсеть/хост веб-хука(в параметре URL),"
         " неправильно указаны тип хука или тип транзакции, попытка создать хук при наличии уже созданного",
    423: "Слишком много запросов, сервис временно недоступен",
    500: "Внутренняя ошибка сервиса (превышена длина URL)",
}
