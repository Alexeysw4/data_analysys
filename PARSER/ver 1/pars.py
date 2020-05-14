import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import pymorphy2

file = open('data.csv', 'w')
users_with_information = []
users_without_information = []


def columns(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')[1:]
    link_divisor = str(trs).split('</span>')

    users = []

    for element in range(len(link_divisor)):
        line = link_divisor[element]
        splitter = line.split('class="fio">')
        finder = line.find('class="fio"')

        if finder > 0:
            users.append(splitter[-1])

    for element in range(len(users)):
        if users[element].find('href') > 0:
            users_with_information.append(users[element])
        else:
            users_without_information.append(users[element])


def speaker_maker(users_with_information):
    links = []
    for element in range(len(users_with_information)):
        splitter = str(users_with_information[element]).split('"')
        links.append(splitter[1])


def filler():
    lol = ['<a href="https://kpfu.ru/Michael.Abramsky" target="_blank">Арсланов Камиль Маратович</a>']
    #for element in users_with_information:
    for element in lol:
        split1 = str(element).split('>')
        split2 = str(split1[1]).split('<')
        split3 = str(split1[0]).split('"')
        data = []

        fio = split2[0]
        url = split3[1]
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        text = str(soup)

        tag_fio = fio
        data.append(str(tag_fio))

        tag_gender = gender_determinant(fio)
        data.append(str(tag_gender))

        tag_str_nal = ('+')
        data.append(str(tag_str_nal))

        tag_language = language_definition(text)
        data.append(str(tag_language))

        tag_education_and_kva = education(text)
        data.append(str(tag_education_and_kva))

        tag_teh_or_hum = 'Не готово'
        data.append(str(tag_teh_or_hum))

        tag_quartet = quartet(text)
        data.append(str(tag_quartet))

        # tag_rank = rank(text)
        # data.append(str(tag_rank))
        #
        # tag_file = have_file(text)
        # data.append(str(tag_file))
        #
        # tag_dr = dr(text)
        # data.append(str(tag_dr))
        #
        # tag_dop_sv = dop_sv(text)
        # data.append(str(tag_dop_sv))
        #
        # tag_dol = dol(text)
        # data.append(str(tag_dol))

        file = open('data.csv', 'a', encoding='utf-8-sig')
        for el in data:
            file.write(el)
            file.write('|')
        file.write('\n')
        file.close()


def gender_determinant(fio):
    split = fio.split(' ')
    fam = split[0]
    name = split[1]
    gen = 'debug'
    if fam[-1] == 'а':
        gen = 'Ж'
    else:
        morph = pymorphy2.MorphAnalyzer()
        parsed_word = morph.parse(str(name))[0]
        if parsed_word.tag.gender == 'masc':
            gen = 'М'
        if parsed_word.tag.gender == 'femn':
            gen = 'Ж'

    return gen


def language_definition(text):
    param = 'Знание языков'
    data = cleaner(param, text)
    if data == None:
        return 'None'
    else:
        mas = []
        word = ''
        selection = purifier(data)

        for el in selection:
            mas.append(el)

        for el in mas:
            word = word + el + ' '
        return word


def education(text):
    param = 'Образование'
    data = cleaner(param, text)
    if data == None:
        return 'None|None'
    else:
        double = purifier(data)
        edu = []
        kva = []
        tag_edu = ''
        tag_kva = ''

        for el in double:
            if el.find('валификация') != -1:
                split = el.split('валификация: ')
                split1 = split[0].split('<')
                x = split1[0]
                edu.append(x)
                kva.append(split[1])
            else:
                split = el.split('<')
                x = split[0]
                edu.append(x)

        l = [line.rstrip() for line in edu]
        for el in l:
            tag_edu = tag_edu + el + '; '

        if len(kva) > 0:
            n = [line.rstrip() for line in kva]
            for el in n:
                tag_kva = tag_kva + el + '; '
        else:
            tag_kva = 'None'

        tag_education = tag_edu + '|' + tag_kva
        return tag_education


def quartet(text):
    param = 'Ученые степени'
    data = cleaner(param, text)
    if data == None:
        return 'None|None|None|None'
    else:
        quart = purifier(data)
        step = 'None'
        spec = 'None'
        dis_name = 'None'
        dis_data = 'None'
        for el in quart:
            if el.find('доктор') != -1 or el.find('кандидат') != -1:
                param1 = el.split(')')
                step = param1[0] + ')'
                dat = param1[1].split('(')
                dis_data = dat[1]

            if el.find('специаль') != -1:
                if el.find('диссер') != -1:
                    split = el.split('специальности')
                    spe = split[1].split(', название диссертации')
                    spec = spe[0]
                    dis_name = spe[1]
                else:
                    pass

        result = step + '|' + spec + '|' + dis_name + '|' + dis_data + '|'
        return result

def rank(text):
    param = 'Ученые звания'
    data = cleaner(param, text)

    if data == None:
        return 'None'
    else:
        mas = []
        word = ''
        selection = purifier(data)
        for el in selection:
            mas.append(el)

        for el in mas:
            word = word + el + ' '
        return word

def have_file(text):
    if '>Файлы' in text:
        return '+'
    else:
        return 'None'

def dr(text):
    param = 'Дата рождения'
    data = cleaner(param, text)
    if data == None:
        return 'None'
    else:
        split = data.split('>')
        return split[1]

def dop_sv(text):
    if '<b>Дополнительные сведения' in text:
        return 'Не готово'
    else:
        return 'Не готово'

def dol(text):
    param = 'Занимаемые должности'
    data = cleaner(param, text)
    if data == None:
        return 'Не готово'
    else:
        mas = []
        word = ''
        selection = purifier(data)

        split = data.split('/')
        print(split)
        for el in split:
            print(el)
        mas = []
        mas2 = []
        word = ''

        for el in split:
            if 'href' in el:
                mas.append(el)
            else:
                if '=' in el:
                    pass
        for el in mas:
            split = el.split('<')
            mas2.append(split[0])

        for el in mas2:
            word = word + el









def cleaner(param, text):
    if text.find(param) > -1:
        if 'font-weight:bold;margin-bottom:2px;' in text:
            split = text.split('font-weight:bold;margin-bottom:2px;')
            del split[0]
            for el in split:
                if el[2] == param[0] and el[3] == param[1] and el[4] == param[2] and param in el:
                    s = el.split('</div>')
                    return s[1].replace("\n", "")
        if 'font-weight:bold;width:420px;margin-bottom:2px;' in text:
            split = text.split('font-weight:bold;width:420px;margin-bottom:2px;')
            del split[0]
            for el in split:
                if el[2] == param[0] and el[3] == param[1] and el[4] == param[2]:
                    s = el.split('</div>')
                    return s[1].replace("\n", "")
    else:
        return None

def purifier(data):
    split = data.split('<li class="li_spec">')
    mass = []
    del split[0]
    for el in split:
        split2 = el.split('</li>')
        carrier = split2[0]
        mass.append(carrier)
    return mass


def main():
    parameter = ['ФИО', 'Пол', 'Наличие Страницы', 'Знание языков', 'Образование', 'Квалификация',
                 'Техническое/Гуманитарное', 'Ученые степени', 'Специальность',
                 'Название диссертации', 'Дата защиты', 'Ученые звания', 'Наличие прикрепленных файлов',
                 'Дата рождения', 'Список публикаций в СМИ', 'Монографии', 'Статьи',
                 'Тезисы и материалы конференций', 'Учебники и учебные пособия']
    # дописать метод для загрузки url всего факультета
    file = open('data.csv', 'a', encoding='utf-8-sig')
    for el in parameter:
        file.write(el)
        file.write('|')
    file.write('\n')
    file.close()

    q = ['https://kpfu.ru/main_page?p_sub=7860&p_id=6895&p_order=1']
    # выгрузка всех преподов со всех факультетов со страницами и без в 2 списка
    columns(q[0])
    # очищает все ссылки преподов со страницами и заполняет поле уникальных параметров для таблицы
    speaker_maker(users_with_information)

    filler()
main()