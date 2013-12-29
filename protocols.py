# -*- coding: 866 -*-
class IniParser:
  def __init__(self, filename = 'collector.ini'):
    self.lines = [] # все строки файла, кроме строк с комментариями
    self.sections = [] # секции файла
    self.commands = [] # команды shell, которые ВНЕЗАПНО встречаются среди строк
    self.dictofvalues = {} # отформатированный в словарь список секций и адресов
    cfile = open(filename) # считать из файла список строк
    for l in cfile.readlines():
      if l[:3] == 'cmd': # вносим команды из файла в отдельный список, чтобы потом отдельно выполнить перед сбором
        self.commands.append(l[4:-1]) # не записываем последний символ, перевод строки
      if (l != '\n') and (l[0:2] != '//') and (l[:3] != 'cmd'): # не брать пустые строки и комментарии
        self.lines.append(l.decode('cp1251')) # совместимость кодировок в shell и в ini-файле
    cfile.close() # закрываем файл
    self.__ClearLines() # чистим строки от комментариев
    self.__TakeSections() # отдельно выбираем секции
    self.__SetDict() # разбираем адреса по секциям в виде словаря
    self.__AddPaths() # к строкам в "особых" секциях добавляем пути, чтобы они читались

# убирает комментарии из строк
  def __ClearLines(self):    
    for l in self.lines:
      a = l.find('\t')
      ltemp = l[:a]
      i = self.lines.index(l)
      self.lines[i] = ltemp

# выбирает из всего массива строк [секции]
  def __TakeSections(self):
    for l in self.lines:
      if l[0] == '[':
        self.sections.append(l)

# собирает в список все строки от значения startline до stopline
  def __SetValue(self, startline, stopline):
    value = []
    for i in range(startline, stopline):
      value.append(self.lines[i])
    return value

# собирает в словарь все пары "секция - список строк до следующей секции"
  def __SetDict(self):
    for s in self.sections:
      startvalue = self.lines.index(s) + 1
      for i in range(startvalue, len(self.lines)):
        if self.lines[i][0] == '[':
          break
        else:
          stopvalue = i + 1
      self.dictofvalues[s] = self.__SetValue(startvalue, stopvalue)

# добавляем к путям без начала (DATABASE_DIR и PROTOCOL_DIR) их папки
  def __AddPaths(self):
    for sec, vlist in self.dictofvalues.iteritems():
      if sec == '[DATABASE_DIR]':
        for l in vlist:
          i = vlist.index(l)
          vlist[i] = "D:\Bars_Com\Db\\" + l
      if sec == '[PROTOCOL_DIR]':
        for l in vlist:
          i = vlist.index(l)
          vlist[i] = "D:\Bars_Com\Protocol\\" + l
      if sec == '[MOVE_PROTOCOL_DIR_PERIOD]':
        for l in vlist:
          i = vlist.index(l)
          vlist[i] = "C:\Bars_Com\Protocol\MoveProtocol\\" + l # исправить на D:!!!!!!!!!!!!!!!11
      if sec == '[SESSION_PROTOCOL_DIR_PERIOD]':
        for l in vlist:
          i = vlist.index(l)
          vlist[i] = "D:\Bars_Com\Protocol\SessionProtocol\\" + l
      if sec == '[SYS_EVENTVIEWER]':
        for l in vlist:
          i = vlist.index(l)
          vlist[i] = "D:\Bars_Com\Protocol\Sys_Eventviewer\\" + l # уточнить путь, в той строке какая-то ерунда написана через запятую

  def OutputToCopy(self):
    result = []
    for sec, vlist in self.dictofvalues.iteritems():
      if (sec != '[CFG]') and (sec != '[7ZIP'):
        result.extend(vlist)
    return result

#---------------------------------------------- Конец класса

#---------------------------------------------- Пара мелких процедур для сокращения места

def generdate(date):
  from string import zfill
  return zfill(str(date.tm_year), 4) + zfill(str(date.tm_mon), 2) + zfill(str(date.tm_mday), 2)

def genertime(time):
  from string import zfill
  return zfill(str(time.tm_hour), 2) + '-' + zfill(str(time.tm_min), 2) + '-' + zfill(str(time.tm_sec), 2)

#---------------------------------------------- Конец

#----------------------------------------------- Процедура выполнения всех команд из списка команд в парсере

def cmd_exec(cmdlist):
  import os
  for cmd in cmdlist:
    print cmd
    os.system(cmd)

#----------------------------------------------- Конец процедуры выполнения команд

#----------------------------------------------- Меню с выбором файла из списка

def choosefilefromlist():
  import os
  os.system('cls')
  print "Список файлов конфигурации:\n"

  filelist = [n for n in os.listdir('.') if (n[-3:] == 'ini')]
  for i, n in enumerate(filelist, 1):
    print i, '-', n
  print ''
  collector_var = raw_input("Введите номер, соответствующий имени файла: ")
  try:
    collector_name = filelist[int(collector_var) - 1]
  except:
    print "Введено некорректное значение, выходим из программы."
    exit(0)
  return collector_name

#----------------------------------------------- Конец меню

#----------------------------------------------- Составление списка на архивацию

def list2arch(templslist, datef, datel):
  import glob
  import re
  list2return = []
# делим даты на числа, которые потом будем сравнивать
  datePattern = re.compile(r'(\d{4})(\d{2})(\d{2})')
  dateFtuple = datePattern.search(datef).groups() # кортеж с годом, месяцем, днём первой даты
  dateLtuple = datePattern.search(datel).groups() # кортеж с годом, месяцем, днём второй даты
# проходим по шаблонам из ini-файла
  for l in templslist:
    fileslist = glob.glob(l)
# проходим по файлам в каждом из шаблонов
    for file_i in fileslist:
# ищем файлы с числами
      datePattern = re.compile(r'_(\d{4})(\d{2})(\d{2})')
      dateC = datePattern.search(file_i) 
      if dateC:
        dateCtuple = datePattern.search(file_i).groups()
        if (dateCtuple < dateFtuple) or (dateCtuple > dateLtuple):
          break
      list2return.append(file_i)
  return list2return

#----------------------------------------------- Конец составления списка

#----------------------------------------------- Архивация

def z(fileslist, zipfilename = 'archive.zip'):
  import zipfile
  tryzip = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
  for file_i in fileslist:
    tryzip.write(file_i, file_i[0] + file_i[2:])
    print "Заархивирован:", file_i
  tryzip.close()

#----------------------------------------------- Конец архивации

#----------------------------------------------- Из-за того, что 7z не умеет записывать с путями, будем копировать и архивировать

def copyfiles(copylist):
  import os, shutil
  for file_i in copylist:
    try:
      diroffile = os.path.dirname(file_i)
      diroffile = diroffile[0] + diroffile[2:] # прибавляем к ней путь на диске до файла, все папки
      if not os.path.exists(diroffile):
        os.makedirs(diroffile) # создаём дерево папок внутри временной
      shutil.copy2(file_i, diroffile) # копируем файл внутрь дерева папок; грубо сделано, каждый раз пытаемся создать каталог
      print "Скопирован файл:", file_i
    except IOError:
      print "Не удалось скопировать файл", file_i
    except WindowsError:
      pass

#----------------------------------------------- Конец копирования

#----------------------------------------------- Архивация с помощью 7z

def z7(zipfilename = 'archive.zip', wayto7z = r'C:\Program Files\7-ZIP\7z'):
  import os, shutil
  os.system('"' + wayto7z + '" a ' + zipfilename + ' ' + 'C')
  os.system('"' + wayto7z + '" a ' + zipfilename + ' ' + 'D')
  try:
    shutil.rmtree('C')
    shutil.rmtree('D')
  except WindowsError:
    pass


#----------------------------------------------- Конец архивации

if __name__ == '__main__':
  import sys
  import re
  from time import localtime
#  форма запроса: protocols.py -az дата1 дата2 ini-файл

  comstr = "".join(sys.argv[1:]) # строка, собранная из параметров командной строки
  comstrPattern = re.compile(r'(-az)? *(\d{8})? *(\d{8})? *(\D*.ini)? *$') # задаём регулярное выражение для параметров командной строки
  comstrList = comstrPattern.search(comstr).groups() # разбиваем на группы параметры командной строки
  az = comstrList[0] # значение - либо "-az", либо None
  col_name = comstrList[3] # берём имя ini-файла из последнего члена
  if not(col_name):             # если пустое, то...
    col_name = choosefilefromlist() # ... выбираем файл из списка
  datef = comstrList[1] # в середине стоят две даты, которые могут быть None
  datel = comstrList[2] # сначала тупо присваиваем
  if not(datef): # если дат в командной строке не найдено...
    datel = datef = generdate(localtime()) # ... то обе даты задать текущей датой
    print 'Не найдено дат в командной строке; собираем протоколы за текущую дату.'
  if datef and not(datel):
    datel = datef # если была только одна дата, вторую ставим автоматом такой же и собираем за тот день
  if datef and datel and (int(datef) > int(datel)): # если конечная дата больше начальной...
    datef, datel = datel, datef # ... то меняем их местами

  parser = IniParser(col_name)
  cmd_exec(parser.commands)
  gatherlist = list2arch(parser.OutputToCopy(), datef, datel)
  archivename = 'archive_' + generdate(localtime()) + '-' + genertime(localtime())
  wayto7z = parser.dictofvalues['[7-ZIP]'][0]
  del parser 

  if az:
    z(gatherlist, archivename + '.zip') # архивирование всех файлов встроенным архиватором
  else:
    copyfiles(gatherlist)
    z7(archivename, wayto7z) # архивирование с помощью 7z

# замечание в строке 74, 66
