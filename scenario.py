scenario = [
    {
        "stepId": "1",
        "question": "Привет! Я бот, который может помочь с покупками, созданием диаграмм или прогнозом покупок. Чем могу помочь? Выберите один из предложенных вариантов или напишите свой ответ:",
        "answersGenerator": "intentAnswers",
        "jumpTo": {
            "make_Purchase": "2",
            "draw_Diagram": "intentNotImplemented",
            "predict_Purchase": "intentNotImplemented"
        }
    },
    {
        "stepId": "2",
        "question": "Какой товар вы хотите купить? Выберите один из предложенных вариантов или напишите свой ответ:",
        "answersGenerator": "getAssetName",
        "jumpTo": {
            "assetNameProvided": "3"
        }
    },
    {
        "stepId": "3",
        "question": "Сколько единиц товара '${lastAssetName}' вы хотите купить? Выберите один из предложенных вариантов или напишите свой ответ:",
        "answersGenerator": "getAssetQuantity",
        "jumpTo": {
            "quantityProvided": "4"
        }
    },
    {
        "stepId": "4",
        "question": "Какую характеристику товара '${lastAssetName}' вы хотите заполнить? Выберите один из предложенных вариантов или напишите свой ответ:",
        "answersGenerator": "getAssetCharacteristic",
        "jumpTo": {
            "characteristicValueProvided": "5"
        }
    },
    {
        "stepId": "5",
        "question": "Введите значение для характеристики '${lastCharacteristic}'. Пожалуйста, напишите свой ответ:",
        "answersGenerator": "getCharacteristicValue",
        "jumpTo": {
            "characteristicValueProvided": "6"
        }
    },
    {
        "stepId": "6",
        "question": "Хотите добавить еще одну характеристику для этого товара? Выберите один из предложенных вариантов или напишите свой ответ:",
        "answersGenerator": "yesNoAnswers",
        "jumpTo": {
            "yes": "4",
            "no": "7"
        }
    },
    {
        "stepId": "7",
        "question": "Хотите добавить еще один товар? Выберите один из предложенных вариантов или напишите свой ответ:",
        "answersGenerator": "yesNoAnswers",
        "jumpTo": {
            "yes": "2",
            "no": "8"
        }
    },
    {
        "stepId": "8",
        "question": "Вот список ваших покупок: $answersData. Все верно?",
        "answersGenerator": "confirmationAnswers",
        "jumpTo": {
            "yes": "9",
            "no": "2"
        }
    },
    {
        "stepId": "9",
        "question": "Заполняю данные покупки...",
        "answersGenerator": "endConversation",
        "jumpTo": {}
    },
    {
        "stepId": "intentNotImplemented",
        "question": "Извините, эта функция пока не реализована. Попробуйте другой запрос.",
        "answersGenerator": "endConversation",
        "jumpTo": {}
    }
]
