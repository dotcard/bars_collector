# -*- coding: cp1251 -*-

def crc(filename):
  import zlib
  prev = 0
  res = 0
  with open(filename, 'rb') as f:
    for line in f:
      prev = zlib.crc32(line, prev)
    res = prev & 0xffffffff
  return res

def file_version(filename):
  import logging
  import ctypes
  from ctypes import c_int, c_char_p, c_void_p, byref, memmove, create_string_buffer, c_ulong

  GetFileVersionInfoSize = ctypes.windll.version.GetFileVersionInfoSizeA
  GetFileVersionInfo = ctypes.windll.version.GetFileVersionInfoA
  VerQueryValue = ctypes.windll.version.VerQueryValueA
  GetLastError = ctypes.windll.kernel32.GetLastError

  p_filename = c_char_p(filename)
  filesize = GetFileVersionInfoSize(p_filename, None)
  if filesize:
    pBuffer = create_string_buffer(filesize)
    GetFileVersionInfo_res = GetFileVersionInfo(p_filename, 0, filesize, pBuffer)
    if GetFileVersionInfo_res:
      lang_addr = c_void_p()
      dwValueLen = c_ulong()
      VerQueryValue_res = VerQueryValue(pBuffer, '\VarFileInfo\Translation', byref(lang_addr), byref(dwValueLen))
      if VerQueryValue_res:  #
        lang_num = c_int() # 
        lang_info = c_int() #
        memmove(byref(lang_num), lang_addr.value, 2) # скинуть в переменную по указателю 2 байта с адреса языковой инфы
        memmove(byref(lang_info), lang_addr.value + 2, 2) # скинуть в другую переменную по указателю 2 байта сразу после предыдущей
        param_addr = c_void_p() # в эту переменную будем писать адрес свойства
        parameter = 'FileVersion' #
        sParam = '\StringFileInfo\%s%s\%s' % (hex(lang_num.value)[2:].zfill(4), hex(lang_info.value)[2:].zfill(4), parameter) # будем искать свойство по строке типа \StringFileInfo\<языковые параметры в 16-ричном виде подряд, типа "11112222">\<название параметра>
        VerQueryValue(pBuffer, sParam, byref(param_addr), byref(dwValueLen)) # читаем адрес нужной нам инфы в общем буфере
        paramBuffer = create_string_buffer(dwValueLen.value) # создаём в памяти строку под нужную нам инфу
        memmove(byref(paramBuffer), param_addr.value, dwValueLen.value) # перемещаем результат из общей памяти в нашу строку
        return paramBuffer.value # выдать результат
      else:
        return 'Нет информации о языке' # не удалось вычитать языковую информацию
    else:
      return 'No result of GetFileVersionInfo'
  else:
    err = GetLastError() # узнаём ошибку windows, почему нет информации о файле
    logging.error('Ошибка Windows') # пишем всякие сообщения
    logging.error(err) # 
    logging.error('В файле нет информации.') #
    return 'Нет информации о файле'

if __name__ == '__main__':
  import glob
  for fn in glob.glob('c:\Python27\DLLs\*.dll'):
    print fn
    print file_version(fn)
