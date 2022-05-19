#!/usr/bin/env python3

# Programa para realizar analise de billing em contas
#
#  Voce passa o profile da conta (-p) ou o arquivo com varios profiles (-f) e ele coleta:
#
#  -- valor total do billing da conta;
#  -- valor total por serviços;
#  -- comparação com o ultimo mes;
#
# Pedacos do codigo vieram do site linuxtut.com (https://www.linuxtut.com/en/e602bb5d3a4950f92dfa/)


import boto3
import os
import argparse
import sys
from error_handler import exception
from datetime import datetime, timedelta, date
from pprint import pprint

@exception
def get_begin_of_month(pshow) -> str:

 if pshow == 1:
  colorlog('DEBUG: {}'.format(date.today().replace(day=1).isoformat()), 'info')

 return date.today().replace(day=1).isoformat()

@exception
def get_last_month(pshow) -> str:
 prev = date.today().replace(day=1) - timedelta(days=1)
 
 if pshow == 1:
  colorlog('DEBUG: {}'.format(prev.replace(day=1)), 'info')

 return prev.replace(day=1)

@exception
def get_today(pshow) -> str:

 if pshow == 1:
  colorlog('DEBUG: {}'.format(date.today().isoformat()), 'info')

 return date.today().isoformat()

@exception
def get_total_cost_date_range(pshow) -> str:
 start_date = get_begin_of_month(pshow)
 end_date = get_today(pshow)

 if pshow == 1:
  colorlog('DEBUG: inicio: {}, final: {}'.format(start_date, end_date), 'info')

#trata se a data inicial for a mesma da final (1º dia do mes)
 if start_date == end_date:
  end_of_month = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=-1)
  begin_of_month = end_of_month.replace(day=1)
  
  if pshow == 1:
   colorlog('DEBUG: inicio:{}, final:{}'.format(begin_of_month.date().isoformat(), end_of_month), 'info')

  return begin_of_month.date().isoformat(), end_date

 return start_date, end_date

@exception
def list_billing(gprofile, pshow) -> dict:
 session = boto3.session.Session(profile_name = str(gprofile))
 conn=session.client('ce')
 
 start_date, end_date = get_total_cost_date_range(pshow)

 response = conn.get_cost_and_usage(
  TimePeriod={
   'Start': start_date,
   'End': end_date
  },
  Granularity='MONTHLY',
   Metrics=[
    'AmortizedCost'
   ]
 )

 if pshow == 1:
  colorlog('DEBUG: response...', 'info')
  pprint(response)
  colorlog('DEBUG: format...', 'info')
  print(f"\
{gprofile},\
{response['ResultsByTime'][0]['TimePeriod']['Start']},\
{response['ResultsByTime'][0]['TimePeriod']['End']},\
{response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount']}\
   ")

 print(f"\
{gprofile},\
{response['ResultsByTime'][0]['TimePeriod']['Start']},\
{response['ResultsByTime'][0]['TimePeriod']['End']},\
{response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount']}\
  ")

 return {
  'start': response['ResultsByTime'][0]['TimePeriod']['Start'],
  'end': response['ResultsByTime'][0]['TimePeriod']['End'],
  'billing': response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount'],
 }

def colorlog ( log, color ) -> dict:
 if color == 'info':    printype = "|  \033[1;33mINFO\033[m    |"
 elif color == 'error': printype = "|  \033[1;31mERROR\033[m   |"
 else:                  printype = "|  \033[1;32mSUCCESS\033[m |"
 timest = datetime.now()
  
 print("{0}{1} |  {2}".format(printype,timest.strftime('%Y/%m/%d_%H:%M:%S'),log))  
 
 return {
  'timestamp':timest.strftime('%Y/%m/%d_%H:%M:%S'),
  'log':log
 }


#==============================================================================
# ---- Inicio do programa
#==============================================================================

if __name__ == '__main__':

 try:
      #Limpa a tela
      #os.system('cls' if os.name == 'nt' else 'clear')

      #ArgParse
  parser = argparse.ArgumentParser(
                        description = 'Modulo para coleta de informacoes em billing',
                        prog ='Jarvis do Sagara',
                        epilog = 'Contato: thiagosagara@gmail.com\n')

  parser.add_argument('-f','--file', action='store',
                        dest='gfile',default = 'notdefined',
                        required = False,
                        help = 'Digite o nome do arquivo onde estão os profiles')

  parser.add_argument('-p','--profile', action='store',
                        dest='gprofile',default = 'Sandbox',
                        required = False,
                        help = 'Digite o nome do profile (~/.aws/credentials)')
                        
  parser.add_argument('-d','--debug', action='store', type=int,
                        dest='pshow', default = 0,
                        required = False,
                        help = 'adicione -d 1 para mostrar em modo debug')

  #Instancia das opcoes

  gfile=parser.parse_args().gfile
  gprofile=parser.parse_args().gprofile
  pshow=parser.parse_args().pshow

      # --------------- Processo em caso de arquivo com os ICs ------------
      # Valida se foi passado o argumento de arquivo
  if gfile != "notdefined":
   profiles = open(gfile)
   print("custumer","start","end","totalbilling",sep=",")
   for profile in profiles:
    profile = profile.strip()
    list_billing(profile, pshow)

  else:
   print("custumer","start","end","totalbilling",sep=",")
   list_billing(gprofile, pshow)

 except KeyboardInterrupt:
  print("Finalizando o script a pedido do user...")
  sys.exit(0)
