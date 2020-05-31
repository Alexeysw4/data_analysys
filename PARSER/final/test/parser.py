import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import pymorphy2
import os

file = open('data.csv', 'w')

def serfer():
    relic = ''
    absolute_path = r'C:\Users\Пользователь\Desktop\test\data'
    local_path = os.walk(absolute_path)
    for el in os.walk(absolute_path):
        if len(el[1]) > 0:
            list = el[1]
            for el in list:
                relic = el
                path = absolute_path + '\\'+ relic
                extractor1(relic, path)
                extractor2(relic, path)


def extractor1(relic, path):
    os.chdir(path)
    directory = os.listdir(path)

    with open(directory[0], 'r') as file:
        for line in file:
            filler(relic, line)

def extractor2(relic, path):
    os.chdir(path)
    directory = os.listdir(path)

    with open(directory[1], 'r') as file:
        for line in file:
            void(relic, line)






def void(relic, line):
    data = [line]
    data = [el.rstrip() for el in data]
    name = data[0]

    tag_gender = gender_determinant(name)
    data.append(str(tag_gender))

    tag_relic = relic
    data.append(str(tag_relic))

    tag_class = classifier(relic)
    data.append(str(tag_class))

    tag_str_nal = ('-')
    data.append(str(tag_str_nal))

    os.chdir(r'C:\Users\Пользователь\Desktop\test')
    file = open('data.csv', 'a', encoding='utf-8-sig')
    for el in data:
        file.write(el)
        file.write('^')
    file.write('\n')
    file.close()


def filler(relic, line):
        data = []
        html = urllib.request.urlopen(line)
        soup = BeautifulSoup(html, 'html.parser')
        text = str(soup)


        tag_fio =  fio_determinant(text)
        data.append(str(tag_fio))

        tag_gender = gender_determinant(tag_fio)
        data.append(str(tag_gender))

        tag_relic = relic
        data.append(str(tag_relic))

        tag_class = classifier(relic)
        data.append(str(tag_class))

        tag_str_nal = ('+')
        data.append(str(tag_str_nal))

        tag_language = language_definition(text)
        data.append(str(tag_language))

        tag_education_and_kva = education(text)
        data.append(str(tag_education_and_kva))

        tag_quartet = quartet(text)
        data.append(str(tag_quartet))

        tag_rank = rank(text)
        data.append(str(tag_rank))

        tag_file = have_file(text)
        data.append(str(tag_file))

        tag_dr = dr(text)
        data.append(str(tag_dr))

        tag_dol = dol(text)
        data.append(str(tag_dol))

        tag_smi = smi(text)
        data.append(str(tag_smi))

        tag_mono = mono(text)
        data.append(str(tag_mono))

        tag_articles = articles(text)
        data.append(str(tag_articles))

        tag_tez = tez(text)
        data.append(str(tag_tez))

        tag_books = books(text)
        data.append(str(tag_books))

        os.chdir(r'C:\Users\Пользователь\Desktop\test')
        file = open('data.csv', 'a', encoding='utf-8-sig')
        for el in data:
            x = data[0]
            if x[0] == '^':
                pass
            else:
                file.write(el)
                file.write('^')

        file.write('\n')
        file.close()

def fio_determinant(text):
    split = text.split('<title>')
    split2 = split[1].split('.')
    return split2[0]


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


def classifier(relic):
    ob = ['Высшая школа бизнеса',
          'Высшая школа государственного и муниципального управления КФУ',
          'Институт международных отношений',
          'Институт социально-философских наук и массовых коммуникаций',
          'Институт управления, экономики и финансов',
          'Юридический факультет']

    tech = ['Высшая школа информационных технологий и интеллектуальных систем',
            'Инженерный институт',
            'Институт вычислительной математики и информационных технологий',
            'Институт математики и механики им.Н.И.Лобачевского',
            'Институт физики',
            'Региональный научно-образовательный математический центр',
            'Центр квантовых технологий',
            'Центр цифровых трансформаций']

    est = ['Институт геологии и нефтегазовых технологий',
           'Институт фундаментальной медицины и биологии',
           'Институт экологии и природопользования',
           'Медико-санитарная часть КФУ',
           'Междисциплинарный центр Аналитическая микроскопия',
           'НОЦ фармацевтики',
           'Общеуниверситетская кафедра физического воспитания и спорта',
           'Химический институт им. А.М. Бутлерова']

    hum = ['Институт передовых образовательных технологий КФУ',
           'Институт психологии и образования',
           'Институт филологии и межкультурной коммуникации',
           'Подготовительный факультет для иностранных учащихся',
           'Центр повышения квалификации и переподготовки научно-педагогических кадров']

    other = ['Общеобразовательная школа-интернат IT-лицей ФГАОУ ВО Казанский (Приволжский) федеральный университет',
             'Общеобразовательная школа-интернат Лицей имени Н.И. Лобачевского']

    for el in ob:
        if el == relic:
            return 'Общественные науки'

    for el in tech:
        if el == relic:
            return 'Технические науки'

    for el in est:
        if el == relic:
            return 'Естественные науки'

    for el in hum:
        if el == relic:
            return 'Гуманитарные  науки'

    for el in ob:
        if el == relic:
            return 'Не указано'

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
        return 'None^None'
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

        tag_education = tag_edu + '^' + tag_kva
        return tag_education


def quartet(text):
    param = 'Ученые степени'
    data = cleaner(param, text)
    if data == None:
        return 'None^None^None^None'
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
                if len(param1) > 2:
                    dat = param1[1].split('(')
                    dis_data = dat[1]
                else: pass

            if el.find('специаль') != -1:
                if el.find('диссер') != -1:
                    split = el.split('специальности')
                    spe = split[1].split(', название диссертации')
                    spec = spe[0]
                    dis_name = spe[1]
                else:
                    pass

        result = step + '^' + spec + '^' + dis_name + '^' + dis_data
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
        return '-'


def dr(text):
    param = 'Дата рождения'
    data = cleaner(param, text)
    if data == None:
        return 'None'
    else:
        split = data.split('>')
        return split[1]


def dol(text):
    param = 'Занимаемые должности'
    data = cleaner(param, text)
    if data == None:
        return 'None'
    else:
        mas = []
        word = ''
        selection = purifier(data)

        split = data.split('>')
        mas = []
        mas2 = []
        mas3 = []
        mas4 = []
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
            split = el.split(',')
            mas3.append(split[0])

        for el in mas3:
            if el.find('/') == -1:
                mas4.append(el)

        for el in mas4:
            if el != mas4[-1]:
                word = word + el + ', '
            else:
                word = word + el
    return word


def smi(text):
    param = 'Публикации в СМИ'
    x = cleaner_2(param, text)
    return x


def mono(text):
    param = 'Монографии'
    x = cleaner_3(param, text)
    return x


def articles(text):
    param = 'Статьи'
    x = cleaner_3(param, text)
    return x


def tez(text):
    param = 'Тезисы и материалы конференций'
    x = cleaner_3(param, text)
    return x


def books(text):
    param = 'Учебники и учебные пособия'
    x = cleaner_4(param, text)
    return x


def cleaner_2(param, text):
    x = text.find(param)
    if x == -1:
        return 'None'
    else:
        data = []
        split = text.split(param)
        split2 = split[0].split('<a href="')
        split3 = split2[-1].split('"')
        href = split3[0]
        y = href.split('amp;')
        href_try = ''

        for el in y:
            href_try = href_try + el

        url = urllib.request.urlopen(href_try)
        soup = BeautifulSoup(url, 'html.parser')
        html = str(soup)
        spl = html.split('<li class="li_spec">')
        for el in spl:
            if el == spl[0]:
                pass
            else:
                z = el.split('<a href=')
                data.append(z[0])
        word = ''
        data = [line.rstrip() for line in data]

        for el in data:
            if el != data[-1]:
                word = word + el + ','
            else:
                word = word + el

        os.chdir(r'C:\Users\Пользователь\Desktop\test')
        file = open('meta.csv', 'w', encoding='utf-8-sig')
        file.write(word)
        file.close()

        with open('meta.csv', encoding='utf-8') as f:
            lst = f.read().splitlines()

        result = ''

        for el in lst:
            if el != lst[-1]:
                result = result + el + ','
            else:
                result = result + el

        file = open('meta.csv', 'w', encoding='utf-8-sig')
        file.write(result)
        file.close()

        result = ''
        for el in lst:
            if len(el) > 6:
                result = result + el
        return result


def cleaner_3(param, text):
    x = text.find(param)
    if x == -1:
        return 'None'
    else:
        data = []
        data2 = []
        split = text.split(param)
        split2 = split[0].split('<a href="')
        split3 = split2[-1].split('"')
        href = split3[0]
        y = href.split('amp;')
        href_try = ''

        for el in y:
            href_try = href_try + el

        url = urllib.request.urlopen(href_try)
        soup = BeautifulSoup(url, 'html.parser')
        html = str(soup)
        spl = html.split('<li class="li_spec">')
        for el in spl:
            if el == spl[0]:
                pass
            else:
                z = el.split('<a href=')
                data.append(z[1])
        word = ''
        data = [line.rstrip() for line in data]

        for el in data:
            spl = el.split('>')
            data2.append(spl[1])
        for el in data2:
            if el != data2[-1]:
                word = word + el + ','
            else:
                word = word + el

        os.chdir(r'C:\Users\Пользователь\Desktop\test')
        file = open('meta.csv', 'w', encoding='utf-8-sig')
        file.write(word)
        file.close()

        with open('meta.csv', encoding='utf-8') as f:
            lst = f.read().splitlines()

        result = ''

        file = open('meta.csv', 'w', encoding='utf-8-sig')
        file.write(result)
        file.close()
        
        data3 = []

        result = ''
        for el in lst:
            el.replace('</a', '')
            data3.append(el)


        for el in data3:
            if len(el) > 6:
                if el != data3[-1]:
                    result = result + el + ','
                else:
                    result = result + el
        return result


def cleaner_4(param, text):
    x = text.find(param)
    if x == -1:
        return 'None'
    else:
        data = []
        data2 = []
        split = text.split(param)
        split2 = split[0].split('<a href="')
        split3 = split2[-1].split('"')
        href = split3[0]
        y = href.split('amp;')
        href_try = ''

        for el in y:
            href_try = href_try + el

        url = urllib.request.urlopen(href_try)
        soup = BeautifulSoup(url, 'html.parser')
        html = str(soup)
        spl = html.split('<li class="li_spec">')
        for el in spl:
            if el == spl[0]:
                pass
            else:
                z = el.split('<a href=')
                data.append(z[1])
        word = ''
        data = [line.rstrip() for line in data]

        for el in data:
            spl = el.split('>')
            data2.append(spl[1])

        for el in data2:
            if el != data2[-1]:
                word = word + el + ','
            else:
                word = word + el

        os.chdir(r'C:\Users\Пользователь\Desktop\test')
        file = open('meta.csv', 'w', encoding='utf-8-sig')
        file.write(word)
        file.close()

        with open('meta.csv', encoding='utf-8') as f:
            lst = f.read().splitlines()

        result = ''

        for el in lst:
            if len(el) > 6:
                if el != lst[-1]:
                    result = result + el + ','
                else:
                    result = result + el

        file = open('meta.csv', 'w', encoding='utf-8-sig')
        file.write(result)
        file.close()


        return result



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
                if param == 'Ученые звания':
                    if el[9] == param[7] and el[10] == param[8] and el[11] == param[9]:
                        s = el.split('</div>')
                        return s[1].replace("\n", "")
                else:
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
    parameter = ['ФИО',
                 'Пол',
                 'Подразделение',
                 'Классификация направления',
                 'Наличие Страницы',
                 'Знание языков',
                 'Образование',
                 'Квалификация',
                 'Ученые степени',
                 'Специальность',
                 'Название диссертации',
                 'Дата защиты',
                 'Ученые звания',
                 'Наличие прикрепленных файлов',
                 'Дата рождения',
                 'Занимаемые должности',
                 'Список публикаций в СМИ',
                 'Монографии',
                 'Статьи',
                 'Тезисы и материалы конференций',
                 'Учебники и учебные пособия',
                 'удалить']
    # дописать метод для загрузки url всего факультета
    file = open('data.csv', 'a', encoding='utf-8-sig')
    for el in parameter:
        if el == parameter[-1]:
            file.write(el)
        else:
            file.write(el)
            file.write('^')
    file.write('\n')
    file.close()
    serfer()


main()