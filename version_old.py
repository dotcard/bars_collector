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

filenamesList = glob.glob('c:\Python27\DLLs\*.dll') # ������: ��� dll
for filename in filenamesList:
  print filename # ������ ��������
  size = GetFileVersionInfoSize(filename, None) # ������ ���������� � ����� ����� WinAPI ��������
  pBuffer = create_string_buffer(size) # ������ � ������ ������ �������� � ��� ����������

  resGFVI = GetFileVersionInfo(filename, 0, size, pBuffer) # ver - ��������� ����� ���������� �������� size � ����� f � ����� ver_buf
  if resGFVI: # ���� ���������, ��
    lang_addr = LPVOID() # ������� ����� ���������� � ����� � ������
    dwValueLen = c_ulong() # ��������� �� ����� ���� DWORD - ����� ��������� ����

    ''' ������������� ���� ���� ��� ������ ������� ������ � sParam ���� �� ���������: ����� ����������� � �������,
    �������� ������� ����� � ���������; � ��� ���� ������'''

    resVQV = VerQueryValue(pBuffer, '\VarFileInfo\Translation', lang_addr, byref(dwValueLen)) # ������ ����� ���� � �����
    if resVQV:  # ���� ���������, ��
      l_num = c_int() # 
      l_info = c_int() #
      memmove(byref(l_num), lang_addr.value, 2) # ������� � ���������� �� ��������� 2 ����� � ������ �������� ����
      memmove(byref(l_info), lang_addr.value + 2, 2) # ������� � ������ ���������� �� ��������� 2 ����� ����� ����� ����������
    else:
      logging.error('���������� � ����� ����������.') # �� ������� �������� �������� ����������
  else:
    err = windll.kernel32.GetLastError() # ����� ������ windows, ������ ��� ���������� � �����
    logging.error('������ Windows') # ����� ������ ���������
    logging.error(err) # 
    logging.error('� ����� ��� ����������.') #
    continue

  parametersList = ['CompanyName', 'FileDescription',
                    'FileVersion', 'InternalName',
                    'LegalCopyright', 'OriginalFileName',
                    'ProductName', 'ProductVersion'] # ������ ������� �����, ������� ����� ��������
  param_addr = LPVOID() # � ��� ���������� ����� ������ ����� ��������
  for parameter in parametersList: # ���������� �� ����� ������ �������
    sParam = '\StringFileInfo\%s%s\%s' % (hex(l_num.value)[2:].zfill(4), hex(l_info.value)[2:].zfill(4), parameter)
    # ����� ������ �������� �� ������ ���� \StringFileInfo\<�������� ��������� � 16-������ ���� ������, ���� "11112222">\<�������� ���������>

    VerQueryValue(pBuffer, sParam, param_addr, byref(dwValueLen)) # ������ ����� ������ ��� ���� � ����� ������

    paramBuffer = create_string_buffer(dwValueLen.value) # ������ � ������ ������ ��� ������ ��� ����
    memmove(byref(paramBuffer), param_addr.value, dwValueLen.value) # ���������� ��������� �� ����� ������ � ���� ������
    print paramBuffer.value # ������ ���������
    
  
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
