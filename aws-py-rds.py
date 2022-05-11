#!/usr/bin/env python3

# Programa para listar os bancos RDS
#
#  Voce passa o profile da conta (-p) e ele vai coletar:
#
#  -- Conta, Regiao, ID da instancia, Tipo da instancia, Lifecycle, Plataforma, Hostname e Status


import boto3
import os
import argparse
import sys
from error_handler import exception
from pprint import pprint


@exception
def list_rds(region, gprofile):
 session = boto3.session.Session(profile_name = str(gprofile), region_name = region)
 conn=session.client('rds')
 
 response = conn.describe_db_instances()
 for i in response['DBInstances']:
  db_name = i['DBInstanceIdentifier']
  db_instance_type = i['DBInstanceClass']
  db_engine = i['Engine']
  db_engine_version = i['EngineVersion']
  db_storage = i['AllocatedStorage']

  print(
f"\
{gprofile},\
{region},\
{db_name},\
{db_instance_type},\
{db_engine},\
{db_engine_version},\
{db_storage}")


 return

@exception
def get_regions(gprofile):
 session = boto3.session.Session(profile_name = gprofile)
 client = session.client('ec2')
 regions = client.describe_regions()
 
 for i in regions['Regions']:
  list_rds(i['RegionName'], gprofile)


#==============================================================================
# ---- Inicio do programa
#==============================================================================

if __name__ == '__main__':

 try:
      #Limpa a tela
      #os.system('cls' if os.name == 'nt' else 'clear')

      #ArgParse
  parser = argparse.ArgumentParser(
                        description = 'Modulo para coleta de informacoes em RDS',
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
#   quit("Feature em desenvolvimento")
   profiles = open(gfile)
   print("custumer","region","name","type","engine","engineversion","storage",sep=",")
   for profile in profiles:
    profile = profile.strip()
    get_regions(profile)

  else:
   print("custumer","region","name","type","engine","engineversion","storage",sep=",")
   get_regions(gprofile)

 except KeyboardInterrupt:
  print("Finalizando o script a pedido do user...")
  sys.exit(0)