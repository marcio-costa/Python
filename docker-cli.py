#!/usr/bin/env python3

import docker
import argparse
import sys
from datetime import datetime


def logando(mensagem, e, logfile="docker-cli.log"):
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open('docker-cli.log', 'a') as log:
        texto = "%s \t %s \t %s \n" % (data_atual, mensagem, str(e))
        log.write(texto)

#def criar_container(imagem, comando):
#    client = docker.from_env()
#    executando = client.containers.run(imagem, comando)
#    print(executando)

def criar_container_args(args):
    try:
        client = docker.from_env()
        executando = client.containers.run(args.imagem, args.comando)
        print(executando)
        return (executando)
    except docker.errors.ImageNotFound as e:
        logando("Erro: Esta imagem não existe!", e)
    except docker.errors.NotFound as e:
        logando("Erro: Este comando não existe!", e)
    except Exception as e:
        logando("Erro! Falha não prevista!", e)
    finally:
        print("Execuntando...!")

def listar_containers():
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            print ("O container %s utiliza a imagem %s rodando o comando %s" %(conectando.short_id, conectando.attrs['Config']['Image'], conectando.attrs['Config']['Cmd']))
    except Exception as e:
        logando("Erro: Contatar seu administrator", e)

def procurar_container(imagem):
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            imagem_container = conectando.attrs['Config']['Image']
            if str(imagem).lower() in str(imagem_container).lower():
                print ("Achei o container %s que contem a palavra %s no nome da sua imagem %s" %(conectando.short_id, imagem, imagem_container))
    except Exception as e:
        logando("Erro: Contatar seu administrator", e)    

def remover_container():
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            portas = conectando.attrs['HostConfig']['PortBindings']
            if isinstance(portas,dict):
                for porta, porta1 in portas.items():
                    porta1 = str(porta1)
                    porta2 = ''.join(filter(str.isdigit, porta1))
                    if int(porta2) <= 1024:
                        print("Removendo o container %s que esta escutando na porta %s e bindando no host na porta %s" % (cada_container.short_id, porta, porta2))
                        removendo = cada_container.remove(force=True)
    except Exception as e:
        logando("Erro: Contatar seu administrator", e)


parser = argparse.ArgumentParser(description="docker-cli criado na aula de python")
subparser = parser.add_subparsers()

criar_opt = subparser.add_parser('criar')
criar_opt.add_argument('--imagem', required=True)
criar_opt.add_argument('--comando', required=True)
criar_opt.set_defaults(func=criar_container_args)

cmd = parser.parse_args()
cmd.func(cmd)


#listar_containers()
#criar_container("alpine", "echo vAII")
#procurar_container("nginx")
#remover_container()