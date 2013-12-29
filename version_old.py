# -*- coding: cp1251 -*-
import sys
import os
import glob
import logging

def crc(filename):
  import zlib
  prev = 0
  for line in open(filename, 'rb'):
    prev = zlib.crc32(line, prev)
  return '%i' % (prev & 0xffffffff)

from ctypes.wintypes import LPCSTR, DWORD, BOOL, LPCVOID, LPVOID, UINT
from ctypes import WINFUNCTYPE, windll, c_int, c_ulong, POINTER, memmove, byref, create_string_buffer

prototype = WINFUNCTYPE(c_int, LPCSTR, POINTER(DWORD))
paramflags = (1, "lptstrFilename"), (1, "lpdwHandle")
GetFileVersionInfoSize = prototype(("GetFileVersionInfoSizeA", windll.version), paramflags)

prototype = WINFUNCTYPE(BOOL, LPCSTR, DWORD, DWORD, LPVOID)
paramflags = (1, "lptstrFilename"), (1, "dwHandle"), (1, "dwLen"), (1, "lpData")
GetFileVersionInfo = prototype(("GetFileVersionInfoA", windll.version), paramflags)

prototype = WINFUNCTYPE(BOOL, LPCVOID, LPCSTR, POINTER(LPVOID), POINTER(UINT))
paramflags = (1, "pBlock"), (1, "lpSubBlock"), (1, "lplpBuffer"), (1, "puLen")
VerQueryValue = prototype(("VerQueryValueA", windll.version), paramflags)
print VerQueryValue

filenamesList = glob.glob('c:\Python27\DLLs\*.dll') # шаблон: все dll
for filename in filenamesList:
  print filename # выдать название
  size = GetFileVersionInfoSize(filename, None) # размер информации о файле узнаём WinAPI функцией
  pBuffer = create_string_buffer(size) # создаём в памяти строку размером с эту информацию

  resGFVI = GetFileVersionInfo(filename, 0, size, pBuffer) # ver - результат сбора информации размером size о файле f в буфер ver_buf
  if resGFVI: # если ненулевая, то
    lang_addr = LPVOID() # будущий адрес информации о языке в буфере
    dwValueLen = c_ulong() # указатель на число типа DWORD - длину языкового поля

    ''' задействовать инфу выше для замены корявой строки в sParam ниже не получится: числа считываются в порядке,
    обратном порядку чисел в параметре; а так идея хороша'''

    resVQV = VerQueryValue(pBuffer, '\VarFileInfo\Translation', lang_addr, byref(dwValueLen)) # читаем адрес инфы о языке
    if resVQV:  # если ненулевая, то
      l_num = c_int() # 
      l_info = c_int() #
      memmove(byref(l_num), lang_addr.value, 2) # скинуть в переменную по указателю 2 байта с адреса языковой инфы
      memmove(byref(l_info), lang_addr.value + 2, 2) # скинуть в другую переменную по указателю 2 байта сразу после предыдущей
    else:
      logging.error('Информация о языке недоступна.') # не удалось вычитать языковую информацию
  else:
    err = windll.kernel32.GetLastError() # узнаём ошибку windows, почему нет информации о файле
    logging.error('Ошибка Windows') # пишем всякие сообщения
    logging.error(err) # 
    logging.error('В файле нет информации.') #
    continue

  parametersList = ['CompanyName', 'FileDescription',
                    'FileVersion', 'InternalName',
                    'LegalCopyright', 'OriginalFileName',
                    'ProductName', 'ProductVersion'] # список свойств файла, которые можно вычитать
  param_addr = LPVOID() # в эту переменную будем писать адрес свойства
  for parameter in parametersList: # проходимся по всему списку свойств
    sParam = '\StringFileInfo\%s%s\%s' % (hex(l_num.value)[2:].zfill(4), hex(l_info.value)[2:].zfill(4), parameter)
    # будем искать свойство по строке типа \StringFileInfo\<языковые параметры в 16-ричном виде подряд, типа "11112222">\<название параметра>

    VerQueryValue(pBuffer, sParam, param_addr, byref(dwValueLen)) # читаем адрес нужной нам инфы в общем буфере

    paramBuffer = create_string_buffer(dwValueLen.value) # создаём в памяти строку под нужную нам инфу
    memmove(byref(paramBuffer), param_addr.value, dwValueLen.value) # перемещаем результат из общей памяти в нашу строку
    print paramBuffer.value # выдать результат
    
  
'''
win32api version:
from win32api import GetFileVersionInfo, LOWORD, HIWORD
l = glob.glob('c:\Python27\DLLs\*.dll')
for f in l:
  try:
    ms = GetFileVersionInfo(f, '\\')['FileVersionMS']
    ls = GetFileVersionInfo(f, '\\')['FileVersionLS']
    print f + ':', str(HIWORD(ls)) + '.' + str(LOWORD(ls)) + '.' + str(HIWORD(ms)) + '.' + str(LOWORD(ms))
  except: print f, ':', crc(f)

'''
