# -*- coding: 866 -*-
class IniParser:
  def __init__(self, filename = 'collector.ini'):
    self.lines = [] # �� ��ப� 䠩��, �஬� ��ப � ��������ﬨ
    self.sections = [] # ᥪ樨 䠩��
    self.commands = [] # ������� shell, ����� �������� ��������� �।� ��ப
    self.dictofvalues = {} # ���ଠ�஢���� � ᫮���� ᯨ᮪ ᥪ権 � ���ᮢ
    cfile = open(filename) # ����� �� 䠩�� ᯨ᮪ ��ப
    for l in cfile.readlines():
      if l[:3] == 'cmd': # ���ᨬ ������� �� 䠩�� � �⤥��� ᯨ᮪, �⮡� ��⮬ �⤥�쭮 �믮����� ��। ᡮ஬
        self.commands.append(l[4:-1]) # �� �����뢠�� ��᫥���� ᨬ���, ��ॢ�� ��ப�
      if (l != '\n') and (l[0:2] != '//') and (l[:3] != 'cmd'): # �� ���� ����� ��ப� � �������ਨ
        self.lines.append(l.decode('cp1251')) # ᮢ���⨬���� ����஢�� � shell � � ini-䠩��
    cfile.close() # ����뢠�� 䠩�
    self.__ClearLines() # ��⨬ ��ப� �� �������ਥ�
    self.__TakeSections() # �⤥�쭮 �롨ࠥ� ᥪ樨
    self.__SetDict() # ࠧ��ࠥ� ���� �� ᥪ�� � ���� ᫮����
    self.__AddPaths() # � ��ப�� � "�ᮡ��" ᥪ��� ������塞 ���, �⮡� ��� �⠫���

# 㡨ࠥ� �������ਨ �� ��ப
  def __ClearLines(self):    
    for l in self.lines:
      a = l.find('\t')
      ltemp = l[:a]
      i = self.lines.index(l)
      self.lines[i] = ltemp

# �롨ࠥ� �� �ᥣ� ���ᨢ� ��ப [ᥪ樨]
  def __TakeSections(self):
    for l in self.lines:
      if l[0] == '[':
        self.sections.append(l)

# ᮡ�ࠥ� � ᯨ᮪ �� ��ப� �� ���祭�� startline �� stopline
  def __SetValue(self, startline, stopline):
    value = []
    for i in range(startline, stopline):
      value.append(self.lines[i])
    return value

# ᮡ�ࠥ� � ᫮���� �� ���� "ᥪ�� - ᯨ᮪ ��ப �� ᫥���饩 ᥪ樨"
  def __SetDict(self):
    for s in self.sections:
      startvalue = self.lines.index(s) + 1
      for i in range(startvalue, len(self.lines)):
        if self.lines[i][0] == '[':
          break
        else:
          stopvalue = i + 1
      self.dictofvalues[s] = self.__SetValue(startvalue, stopvalue)

# ������塞 � ���� ��� ��砫� (DATABASE_DIR � PROTOCOL_DIR) �� �����
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
          vlist[i] = "C:\Bars_Com\Protocol\MoveProtocol\\" + l # ��ࠢ��� �� D:!!!!!!!!!!!!!!!11
      if sec == '[SESSION_PROTOCOL_DIR_PERIOD]':
        for l in vlist:
          i = vlist.index(l)
          vlist[i] = "D:\Bars_Com\Protocol\SessionProtocol\\" + l
      if sec == '[SYS_EVENTVIEWER]':
        for l in vlist:
          i = vlist.index(l)
          vlist[i] = "D:\Bars_Com\Protocol\Sys_Eventviewer\\" + l # ��筨�� ����, � ⮩ ��ப� �����-� ��㭤� ����ᠭ� �१ �������

  def OutputToCopy(self):
    result = []
    for sec, vlist in self.dictofvalues.iteritems():
      if (sec != '[CFG]') and (sec != '[7ZIP'):
        result.extend(vlist)
    return result

#---------------------------------------------- ����� �����

#---------------------------------------------- ��� ������ ��楤�� ��� ᮪�饭�� ����

def generdate(date):
  from string import zfill
  return zfill(str(date.tm_year), 4) + zfill(str(date.tm_mon), 2) + zfill(str(date.tm_mday), 2)

def genertime(time):
  from string import zfill
  return zfill(str(time.tm_hour), 2) + '-' + zfill(str(time.tm_min), 2) + '-' + zfill(str(time.tm_sec), 2)

#---------------------------------------------- �����

#----------------------------------------------- ��楤�� �믮������ ��� ������ �� ᯨ᪠ ������ � �����

def cmd_exec(cmdlist):
  import os
  for cmd in cmdlist:
    print cmd
    os.system(cmd)

#----------------------------------------------- ����� ��楤��� �믮������ ������

#----------------------------------------------- ���� � �롮஬ 䠩�� �� ᯨ᪠

def choosefilefromlist():
  import os
  os.system('cls')
  print "���᮪ 䠩��� ���䨣��樨:\n"

  filelist = [n for n in os.listdir('.') if (n[-3:] == 'ini')]
  for i, n in enumerate(filelist, 1):
    print i, '-', n
  print ''
  collector_var = raw_input("������ �����, ᮮ⢥�����騩 ����� 䠩��: ")
  try:
    collector_name = filelist[int(collector_var) - 1]
  except:
    print "������� �����४⭮� ���祭��, ��室�� �� �ணࠬ��."
    exit(0)
  return collector_name

#----------------------------------------------- ����� ����

#----------------------------------------------- ���⠢����� ᯨ᪠ �� ��娢���

def list2arch(templslist, datef, datel):
  import glob
  import re
  list2return = []
# ����� ���� �� �᫠, ����� ��⮬ �㤥� �ࠢ������
  datePattern = re.compile(r'(\d{4})(\d{2})(\d{2})')
  dateFtuple = datePattern.search(datef).groups() # ���⥦ � �����, ����楬, ��� ��ࢮ� ����
  dateLtuple = datePattern.search(datel).groups() # ���⥦ � �����, ����楬, ��� ��ன ����
# ��室�� �� 蠡����� �� ini-䠩��
  for l in templslist:
    fileslist = glob.glob(l)
# ��室�� �� 䠩��� � ������ �� 蠡�����
    for file_i in fileslist:
# �饬 䠩�� � �᫠��
      datePattern = re.compile(r'_(\d{4})(\d{2})(\d{2})')
      dateC = datePattern.search(file_i) 
      if dateC:
        dateCtuple = datePattern.search(file_i).groups()
        if (dateCtuple < dateFtuple) or (dateCtuple > dateLtuple):
          break
      list2return.append(file_i)
  return list2return

#----------------------------------------------- ����� ��⠢����� ᯨ᪠

#----------------------------------------------- ��娢���

def z(fileslist, zipfilename = 'archive.zip'):
  import zipfile
  tryzip = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
  for file_i in fileslist:
    tryzip.write(file_i, file_i[0] + file_i[2:])
    print "����娢�஢��:", file_i
  tryzip.close()

#----------------------------------------------- ����� ��娢�樨

#----------------------------------------------- ��-�� ⮣�, �� 7z �� 㬥�� �����뢠�� � ���ﬨ, �㤥� ����஢��� � ��娢�஢���

def copyfiles(copylist):
  import os, shutil
  for file_i in copylist:
    try:
      diroffile = os.path.dirname(file_i)
      diroffile = diroffile[0] + diroffile[2:] # �ਡ���塞 � ��� ���� �� ��᪥ �� 䠩��, �� �����
      if not os.path.exists(diroffile):
        os.makedirs(diroffile) # ᮧ��� ��ॢ� ����� ����� �६�����
      shutil.copy2(file_i, diroffile) # �����㥬 䠩� ������ ��ॢ� �����; ��㡮 ᤥ����, ����� ࠧ ��⠥��� ᮧ���� ��⠫��
      print "�����஢�� 䠩�:", file_i
    except IOError:
      print "�� 㤠���� ᪮��஢��� 䠩�", file_i
    except WindowsError:
      pass

#----------------------------------------------- ����� ����஢����

#----------------------------------------------- ��娢��� � ������� 7z

def z7(zipfilename = 'archive.zip', wayto7z = r'C:\Program Files\7-ZIP\7z'):
  import os, shutil
  os.system('"' + wayto7z + '" a ' + zipfilename + ' ' + 'C')
  os.system('"' + wayto7z + '" a ' + zipfilename + ' ' + 'D')
  try:
    shutil.rmtree('C')
    shutil.rmtree('D')
  except WindowsError:
    pass


#----------------------------------------------- ����� ��娢�樨

if __name__ == '__main__':
  import sys
  import re
  from time import localtime
#  �ଠ �����: protocols.py -az ���1 ���2 ini-䠩�

  comstr = "".join(sys.argv[1:]) # ��ப�, ᮡ࠭��� �� ��ࠬ��஢ ��������� ��ப�
  comstrPattern = re.compile(r'(-az)? *(\d{8})? *(\d{8})? *(\D*.ini)? *$') # ����� ॣ��୮� ��ࠦ���� ��� ��ࠬ��஢ ��������� ��ப�
  comstrList = comstrPattern.search(comstr).groups() # ࠧ������ �� ��㯯� ��ࠬ���� ��������� ��ப�
  az = comstrList[0] # ���祭�� - ���� "-az", ���� None
  col_name = comstrList[3] # ���� ��� ini-䠩�� �� ��᫥����� 童��
  if not(col_name):             # �᫨ ���⮥, �...
    col_name = choosefilefromlist() # ... �롨ࠥ� 䠩� �� ᯨ᪠
  datef = comstrList[1] # � �।��� ���� ��� ����, ����� ����� ���� None
  datel = comstrList[2] # ᭠砫� �㯮 ��ᢠ�����
  if not(datef): # �᫨ ��� � ��������� ��ப� �� �������...
    datel = datef = generdate(localtime()) # ... � ��� ���� ������ ⥪�饩 ��⮩
    print '�� ������� ��� � ��������� ��ப�; ᮡ�ࠥ� ��⮪��� �� ⥪���� ����.'
  if datef and not(datel):
    datel = datef # �᫨ �뫠 ⮫쪮 ���� ���, ����� �⠢�� ��⮬�⮬ ⠪�� �� � ᮡ�ࠥ� �� �� ����
  if datef and datel and (int(datef) > int(datel)): # �᫨ ����筠� ��� ����� ��砫쭮�...
    datef, datel = datel, datef # ... � ���塞 �� ���⠬�

  parser = IniParser(col_name)
  cmd_exec(parser.commands)
  gatherlist = list2arch(parser.OutputToCopy(), datef, datel)
  archivename = 'archive_' + generdate(localtime()) + '-' + genertime(localtime())
  wayto7z = parser.dictofvalues['[7-ZIP]'][0]
  del parser 

  if az:
    z(gatherlist, archivename + '.zip') # ��娢�஢���� ��� 䠩��� ���஥��� ��娢��஬
  else:
    copyfiles(gatherlist)
    z7(archivename, wayto7z) # ��娢�஢���� � ������� 7z

# ����砭�� � ��ப� 74, 66
