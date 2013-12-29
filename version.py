# -*- coding: cp1251 -*-
import sys, os, glob, logging

def crc(filename):
  import zlib
  prev = 0
  for line in open(filename, 'rb'):
    prev = zlib.crc32(line, prev)
  return '%i' % (prev & 0xffffffff)

import ctypes, ctypes.wintypes
from ctypes import c_int

GetFileVersionInfoSize = ctypes.windll.version.GetFileVersionInfoSizeA
GetFileVersionInfo = ctypes.windll.version.GetFileVersionInfoA
VerQueryValue = ctypes.windll.version.VerQueryValueA
GetLastError = ctypes.windll.kernel32.GetLastError

filenameslist = glob.glob('c:\Python27\DLLs\*.dll')
for filename in filenameslist:
  print filename
  f_pointer = ctypes.c_char_p(filename)
  size = GetFileVersionInfoSize(f_pointer, None)
  if size:
    pBuffer = ctypes.create_string_buffer(size)
    GetFileVersionInfo_res = GetFileVersionInfo(f_pointer, 0, size, pBuffer)
    if GetFileVersionInfo_res:
      lang_addr = ctypes.c_void_p() # какой-то странный костыль, требуется указатель на тип, а не сам тип, хотя если сравнивать с исполнением через прототипы, типы переменных здесь совпадают
      dwValueLen = ctypes.c_ulong()
      VerQueryValue_res = VerQueryValue(pBuffer, '\VarFileInfo\Translation', ctypes.byref(lang_addr), ctypes.byref(dwValueLen))
      if VerQueryValue_res:  #
        l_num = ctypes.c_int() # 
        l_info = ctypes.c_int() #
        ctypes.memmove(ctypes.byref(l_num), lang_addr.value, 2) # скинуть в переменную по указателю 2 байта с адреса языковой инфы
        ctypes.memmove(ctypes.byref(l_info), lang_addr.value + 2, 2) # скинуть в другую переменную по указателю 2 байта сразу после предыдущей
      else:
        print 'Нет информации о языке' # не удалось вычитать языковую информацию
    else:
      print 'No resGFVI'
  else:
    err = GetLastError() # узнаём ошибку windows, почему нет информации о файле
    logging.error('Ошибка Windows') # пишем всякие сообщения
    logging.error(err) # 
    logging.error('В файле нет информации.') #
    continue

  parametersList = ['CompanyName', 'FileDescription',
                    'FileVersion', 'InternalName',
                    'LegalCopyright', 'OriginalFileName',
                    'ProductName', 'ProductVersion'] # список свойств файла, которые можно вычитать
  param_addr = ctypes.c_void_p() # в эту переменную будем писать адрес свойства
  for parameter in parametersList: # проходимся по всему списку свойств
    sParam = '\StringFileInfo\%s%s\%s' % (hex(l_num.value)[2:].zfill(4), hex(l_info.value)[2:].zfill(4), parameter)
    # будем искать свойство по строке типа \StringFileInfo\<языковые параметры в 16-ричном виде подряд, типа "11112222">\<название параметра>

    VerQueryValue(pBuffer, sParam, ctypes.byref(param_addr), ctypes.byref(dwValueLen)) # читаем адрес нужной нам инфы в общем буфере

    paramBuffer = ctypes.create_string_buffer(dwValueLen.value) # создаём в памяти строку под нужную нам инфу
    ctypes.memmove(ctypes.byref(paramBuffer), param_addr.value, dwValueLen.value) # перемещаем результат из общей памяти в нашу строку
    print paramBuffer.value # выдать результат
