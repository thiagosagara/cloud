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
from calendar import monthrange


@exception
def get_begin_of_month() -> str:

 if pshow == 1:
  colorlog('DEBUG: {}'.format(date.today().replace(day=1).isoformat()), 'info')

 return date.today().replace(day=1).isoformat()

@exception
def get_last_month() -> str:
 #pega o primeiro dia do ultimo mes
 lstart_date = date.today().replace(day=1) - timedelta(days=1)
 lstart_date = lstart_date.replace(day=1)

 #pega o ultimo dia do ultimo mes
 lend_date = date(int(lstart_date.strftime("%Y")), int(lstart_date.strftime("%m")), monthrange(int(lstart_date.strftime("%Y")), int(lstart_date.strftime("%m")))[1])
 
 if pshow == 1:
  colorlog('DEBUG: start: {}, end: {}'.format(lstart_date, lend_date), 'info')

 return lstart_date, lend_date

@exception
def get_today() -> str:

 if pshow == 1:
  colorlog('DEBUG: {}'.format(date.today().isoformat()), 'info')

 return date.today().isoformat()

@exception
def get_total_cost_date_range(gstart=True, gend=True) -> str:
 global start_date
 global end_date
 if gstart == True:
  start_date = get_begin_of_month()
  end_date = get_today()
 else:
  start_date = gstart
  end_date = gend  

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
def get_total_billing(gstart=True, gend=True) -> dict:
 if gstart == True:
  start_date, end_date = get_total_cost_date_range()
 else:
  start_date, end_date = get_total_cost_date_range(str(gstart), str(gend))

 response = gconn.get_cost_and_usage(
  TimePeriod={
   'Start': start_date,
   'End': end_date
  },
  Granularity='MONTHLY',
  Metrics=['AmortizedCost']
 )
 
 total_billing = round(float(response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount']),2)
 
 if pshow == 1:
  colorlog('DEBUG: StartTime: {}'.format(start_date), 'info')
  colorlog('DEBUG: EndTime: {}'.format(end_date), 'info')
  colorlog('DEBUG: TotalBilling: {}'.format(total_billing), 'info')
  colorlog('DEBUG: reponse...', 'info')
  pprint(response)

 return { 'total':{'total':total_billing } }
 
@exception
def get_service_billing() -> dict:
 start_date, end_date = get_total_cost_date_range()
 
 response = gconn.get_cost_and_usage(
  TimePeriod={
   'Start': start_date,
   'End': end_date
  },
  Granularity='MONTHLY',
  Metrics=['AmortizedCost'],
  GroupBy=[{
   'Type':'DIMENSION',
   'Key':'SERVICE'
  }]
 )
 
 services_billing = {}

 for item in response['ResultsByTime'][0]['Groups']:
  service = {
   'name': item['Keys'][0],
   'billing': round(float(item['Metrics']['AmortizedCost']['Amount']),2)
  }

  services_billing[service['name']] = service
  
 if pshow == 1:
  colorlog('DEBUG: response...', 'info')
  pprint(response)
  colorlog('DEBUG: services...', 'info')
  pprint(services_billing)

 return services_billing

#em desenvolvimento
def main_process(customer) -> dict:
 
 cur_total_billing = get_total_billing()
 #cur_service_billing = get_service_billing()
 
 lstart_date, lend_date = get_last_month()
 last_total_billing = get_total_billing(lstart_date, lend_date)

 #for k, v in cur_service_billing.items():
  #print(f"{customer},{start_date},{end_date},{k},{v['billing']},last,current")

 for ck, cv in cur_total_billing.items():
  for lk, lv in last_total_billing.items():
   print(f"{customer},{start_date},{end_date},{ck},{cv['total']},{lv['total']},same")

 return {
  'customer': gprofile,
  'start':'carlos',
  'end':'adao',
  'totalbilling':'mais_de_8000'
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

  parser.add_argument('-m','--lastmonth', action='store',
                        dest='gmonth',default = 'lastmonth',
                        required = False,
                        help = 'compara com o ultimo mes')

  parser.add_argument('-c','--currentmonth', action='store',
                        dest='gcurm',default = 'currentmonth',
                        required = False,
                        help = 'compara no mes atual')


  parser.add_argument('-d','--debug', action='store', type=int,
                        dest='pshow', default = 0,
                        required = False,
                        help = 'adicione -d 1 para mostrar em modo debug')

  #Instancia as opcoes

  gfile=parser.parse_args().gfile
  gprofile=parser.parse_args().gprofile
  pshow=parser.parse_args().pshow
  gcurm=parser.parse_args().gcurm
  gmonth=parser.parse_args().gmonth

  # --------------- Processo em caso de arquivo com os Profiles ------------
  # Valida se foi passado o argumento de arquivo
  if gfile != "notdefined":
   profiles = open(gfile)
   print("custumer","startdate","enddate","servicename","currentbilling","lastbilling","correlation",sep=",")
   for profile in profiles:
    profile = profile.strip()
    
    session = boto3.session.Session(profile_name = str(profile))
    gconn=session.client('ce')

    main_process(profile)

  else:
   print("custumer","startdate","enddate","servicename","currentbilling","lastbilling","correlation",sep=",")
   
   session = boto3.session.Session(profile_name = str(gprofile))
   gconn=session.client('ce')
   
   main_process(gprofile)

 except KeyboardInterrupt:
  print("Finalizando o script a pedido do user...")
  sys.exit(0)
