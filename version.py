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
      lang_addr = ctypes.c_void_p() # �����-�� �������� �������, ��������� ��������� �� ���, � �� ��� ���, ���� ���� ���������� � ����������� ����� ���������, ���� ���������� ����� ���������
      dwValueLen = ctypes.c_ulong()
      VerQueryValue_res = VerQueryValue(pBuffer, '\VarFileInfo\Translation', ctypes.byref(lang_addr), ctypes.byref(dwValueLen))
      if VerQueryValue_res:  #
        l_num = ctypes.c_int() # 
        l_info = ctypes.c_int() #
        ctypes.memmove(ctypes.byref(l_num), lang_addr.value, 2) # ������� � ���������� �� ��������� 2 ����� � ������ �������� ����
        ctypes.memmove(ctypes.byref(l_info), lang_addr.value + 2, 2) # ������� � ������ ���������� �� ��������� 2 ����� ����� ����� ����������
      else:
        print '��� ���������� � �����' # �� ������� �������� �������� ����������
    else:
      print 'No resGFVI'
  else:
    err = GetLastError() # ����� ������ windows, ������ ��� ���������� � �����
    logging.error('������ Windows') # ����� ������ ���������
    logging.error(err) # 
    logging.error('� ����� ��� ����������.') #
    continue

  parametersList = ['CompanyName', 'FileDescription',
                    'FileVersion', 'InternalName',
                    'LegalCopyright', 'OriginalFileName',
                    'ProductName', 'ProductVersion'] # ������ ������� �����, ������� ����� ��������
  param_addr = ctypes.c_void_p() # � ��� ���������� ����� ������ ����� ��������
  for parameter in parametersList: # ���������� �� ����� ������ �������
    sParam = '\StringFileInfo\%s%s\%s' % (hex(l_num.value)[2:].zfill(4), hex(l_info.value)[2:].zfill(4), parameter)
    # ����� ������ �������� �� ������ ���� \StringFileInfo\<�������� ��������� � 16-������ ���� ������, ���� "11112222">\<�������� ���������>

    VerQueryValue(pBuffer, sParam, ctypes.byref(param_addr), ctypes.byref(dwValueLen)) # ������ ����� ������ ��� ���� � ����� ������

    paramBuffer = ctypes.create_string_buffer(dwValueLen.value) # ������ � ������ ������ ��� ������ ��� ����
    ctypes.memmove(ctypes.byref(paramBuffer), param_addr.value, dwValueLen.value) # ���������� ��������� �� ����� ������ � ���� ������
    print paramBuffer.value # ������ ���������
