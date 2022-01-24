from django.shortcuts import render
import requests
from django.http import HttpResponse

key = 'ключ'


def func(word):  # основная функция подучения списка разбора слова
    global key
    url_translate = 'https://developers.lingvolive.com/api/v1/WordForms'  # ссыль
    params_wordforms = {
        'text': word,
        'lang': 1049
    }
    try:
        head_trans = {'Authorization': 'Bearer ' + str(key)}
        n = requests.get(url_translate, headers=head_trans, params=params_wordforms)

        return n.json()
    except:
        key = auth_key(key)
        head_trans = {'Authorization': 'Bearer ' + str(key)}
        n = requests.get(url_translate, headers=head_trans, params=params_wordforms)

        return n.json()



def auth_key(key):  # функция для получения суточного ключа сработает только если ключ устаревает
    key_login = 'ZWU2MGQ5ZTctODI4OC00MTBjLWI2ZWMtOTQ0MWVmZjA4ZmUwOmNiY2RhYzM5YmM0YjRmYThiYzg4MDIxM2VlNGY0YTZk'
    URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'  # ссыль для получения суточного ключа
    headers_auth = {'Authorization': 'Basic ' + key_login}  # headers для получения ключа на сутки
    auth = requests.post(URL_AUTH, headers=headers_auth)  # сам пост запрос
    key = auth.text
    return key

def info(request):
    return render(request,'wordforms/info.html')


def home(request):

    return render(request, 'wordforms/home.html')


def results(request):

    word = str(request.GET.get('name_field'))  # получила слово
    word_result = func(word)
    if  'Word not found' in str(word_result):
        return render(request,'wordforms/home.html',{'error':'Ошибка в слове! Проверьте пожалуйста правильность написания и повторите попытку'})
    else:
        logos = word_result[0]['PartOfSpeech']  # часть речи
        name = word_result[0]['ParadigmJson']['Name']  # слово
        basic = word_result[0]['ParadigmJson']['Grammar']  # основная информация

        if logos == 'глагол':  # парсим глагол
            try:
                infin = str(word_result[0]['ParadigmJson']['Groups'][0]['Table'][0][1]['Value'])
            except IndexError:
                infin = ''

            try:
                prezent = [[str(j['Value'] + ' (' + str(j['Prefix'].rstrip()) + ')') for j in i] for i in
                           word_result[0]['ParadigmJson']['Groups'][1]['Table']]  # распарсила json
                prezent = [x for sublist in prezent for x in sublist]  # сделала одномерным (для адекватности шаблона)
            except IndexError:
                prezent = []

            try:
                past = [[str(j['Value'] + ' (' + str(j['Prefix'].rstrip()) + ')') for j in i] for i in
                        word_result[0]['ParadigmJson']['Groups'][2]['Table']]  # распарсила json
                past = [x for sublist in past for x in sublist]  # сделала одномерным
            except IndexError:
                past = []

            try:
                participle = word_result[0]['ParadigmJson']['Groups'][3]['Table'][1]  # причастие
                participle = ', '.join([participle[i]['Value'] for i in range(1, len(participle))])
            except IndexError:
                participle = ''

            try:
                deyeprichastiye = word_result[0]['ParadigmJson']['Groups'][3]['Table'][2]  # deyeprichastiye
                deyeprichastiye = ', '.join([deyeprichastiye[i]['Value'] for i in range(1, len(deyeprichastiye))])
            except IndexError:
                deyeprichastiye = ''

            try:
                imperative = word_result[0]['ParadigmJson']['Groups'][4]['Table'][1]  # повелительное наклонение
                imperative = ', '.join([imperative[i]['Value'] for i in range(1, len(imperative))])
            except IndexError:
                imperative = ''

            context = {'word': word, 'name': name, 'basic': basic, 'logos': logos, 'infin': infin, 'prezent': prezent,
                       'past': past, 'participle': participle, 'deyeprichastiye': deyeprichastiye, 'imperative': imperative}
            return render(request, 'wordforms/results.html', context=context)

        if logos == 'прилагательное':  # парсим прилагательное
            try:
                forms_men = [i['Value'] for i in
                             word_result[0]['ParadigmJson']['Groups'][0]['Table'][1]]  # краткая и полная форма мужской род
                forms_men = ' ,'.join([forms_men[i] for i in range(1, len(forms_men))])
            except IndexError:
                forms_men = ''
            try:
                forms_women = [i['Value'] for i in
                               word_result[0]['ParadigmJson']['Groups'][0]['Table'][
                                   2]]  # краткая и полная форма мужской род
                forms_women = ' ,'.join(
                    [forms_women[i] for i in range(1, len(forms_women))])  # краткая и полная форма женский род
            except IndexError:
                forms_women = ''

            try:
                average = [i['Value'] for i in
                           word_result[0]['ParadigmJson']['Groups'][0]['Table'][3]]  # краткая и полная форма средний род
                average = ' ,'.join([average[i] for i in range(1, len(average))])
            except IndexError:
                average = ''

            try:
                plural = [i['Value'] for i in
                          word_result[0]['ParadigmJson']['Groups'][0]['Table'][4]]  # множественное число
                plural = ' ,'.join([plural[i] for i in range(1, len(plural))])
            except IndexError:
                plural = ''
            try:
                comparative = word_result[0]['ParadigmJson']['Groups'][1]['Table'][0][1]['Value']  # сравнительная степень
            except IndexError:
                comparative = []

            try:
                superlative = word_result[0]['ParadigmJson']['Groups'][2]['Table'][0][1]['Value']  # превосходная степень
            except IndexError:
                superlative = []

            context = {'word': word, 'name': name, 'basic': basic, 'logos': logos, 'superlative': superlative,
                       'comparative': comparative, 'plural': plural, 'average': average, 'forms_men': forms_men,
                       'forms_women': forms_women}
            return render(request, 'wordforms/results.html', context=context)

        if logos == 'числительное' or logos == 'местоимение' or logos == 'существительное':
            try:
                declination = word_result[0]['ParadigmJson']['Groups'][0]['Table']  # склонения
                declination = [[j['Value'] for j in declination[i]] for i in range(1, len(declination))]
                declination = [', '.join(i) for i in declination]
                declination = [i.replace(',', ':', 1) for i in declination]
            except IndexError:
                declination = []

            try:
                forms = [i['Value'] for i in word_result[0]['ParadigmJson']['Groups'][0]['Table'][0]]
                forms = ', '.join(forms).replace(',', '', 1)
            except IndexError:
                forms = ''

            context = {'word': word, 'name': name, 'basic': basic, 'logos': logos, 'declination': declination,
                       'forms': forms}

            return render(request, 'wordforms/results.html', context=context)

        if logos == 'наречие':
            try:
                positive_degree = word_result[0]['ParadigmJson']['Groups'][0]['Table'][0][1][
                    'Value']  # положительная степень
            except IndexError:
                positive_degree = ''
            try:
                comparative = word_result[0]['ParadigmJson']['Groups'][0]['Table'][1][1]['Value']  # сравнительная степень
            except IndexError:
                comparative = ''
            try:
                superlative = word_result[0]['ParadigmJson']['Groups'][0]['Table'][2][1]['Value']  # превосходная степень
            except IndexError:
                superlative = ''

            context = {'word': word, 'name': name, 'basic': basic, 'logos': logos, 'positive_degree': positive_degree,
                       'comparative': comparative, 'superlative': superlative}

            return render(request, 'wordforms/results.html', context=context)
