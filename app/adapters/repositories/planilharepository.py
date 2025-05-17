from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session
from app.adapters.repositories.entities.gruponumero import GrupoNumero
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.operacao import Operacao
from app.adapters.repositories.entities.numero import Numero
from app.adapters.repositories.entities.mensagens import Mensagem
from app.adapters.repositories.entities.ligacao import Ligacao
from app.adapters.repositories.entities.contatos import Contato
from app.adapters.repositories.entities.grupos import Grupo
from app.adapters.repositories.entities.planilha import Planilha
from app.adapters.repositories.entities.interceptacao import Interceptacao
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero
from app.adapters.repositories.entities.ip import IP

class PlanilhaRepository:
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_all_ordered_by_upload_date(self):
        return self.session.query(Planilha).order_by(Planilha.dataUpload.asc()).all()

    def validate_columns(self, df: pd.DataFrame, required_columns):
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
    def get_or_create_numero(self, numero, ticket, cache):
        numero_str = str(numero)
        if numero_str not in cache:
            obj = Numero(numero=numero_str, internalTicketNumber=ticket)
            self.session.add(obj)
            self.session.flush()
            cache[numero_str] = obj
        return cache[numero_str]

    def get_or_create_interceptacao_numero(self, numero_obj, interceptacao, is_alvo, cache):
        if cache.get(numero_obj.numero) != interceptacao.id:
            inter_num = InterceptacaoNumero(
                numeroId=numero_obj.id,
                interceptacaoId=interceptacao.id,
                isAlvo=is_alvo
            )
            self.session.add(inter_num)
            cache[numero_obj.numero] = interceptacao.id
            
    def get_or_update_interceptacao_numero(self, alvo, cache):
        alvo_id = alvo.id
        if alvo_id not in cache:
            res = self.session.query(InterceptacaoNumero).filter(
                InterceptacaoNumero.numeroId == alvo_id,
                InterceptacaoNumero.isAlvo == False
            ).first()

            if res is not None:
                res.isAlvo = True
                self.session.flush()

            cache[alvo_id] = res
        return cache[alvo_id]

    def parse_datetime(self, dt_str, fmt="%Y-%m-%d %H:%M:%S"): 
        return datetime.strptime(str(dt_str).replace(" UTC", ""), fmt)

    def parse_date(self, date_str):
        return datetime.strptime(str(date_str)[:10], "%Y-%m-%d").date()

    def parse_time(self, time_str):
        return datetime.strptime(str(time_str), "%H:%M:%S").time()

    def save(self, file_buffer, file_size, filename, operacao_id):
        required_columns = [
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIMESTAMP', 'DATA', 'HORA', 'IP'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'TIMESTAMP', 'DATA', 'HORA', 'MESSAGE ID', 'SENDER', 'RECIPIENTS', 'GROUP ID', 'SENDER IP', 'SENDER PORT', 'SENDER DEVICE', 'TYPE', 'MESSAGE STYLE', 'MESSAGE SYZE'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'CALL ID', 'CALL CREATOR', 'TIMESTAMP', 'DATA', 'HORA', 'TIPO DE MIDIA', 'IP DO CRIADOR', 'PORTA DO CRIADOR', 'RECEPTOR', 'IP DO RECEPTOR', 'PORTA DO RECEPTOR'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'TIPO CONTATO', 'CONTATO'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'ID', 'CREATION', 'DATA LOCAL', 'HORA LOCAL', 'SIZE', 'DESCRIPTION', 'SUBJECT']
        ]
        sheets_name = ["Planilha1", "Planilha2", "Planilha3", "Planilha4", "Planilha5"]
        sheets_df = []

        with pd.ExcelFile(file_buffer) as xls:
            for idx, sheet_name in enumerate(sheets_name):
                df = pd.read_excel(xls, sheet_name=sheet_name)
                if df.empty:
                    raise ValueError(f'Sheet "{sheet_name}" is empty')
                self.validate_columns(df, required_columns[idx])
                sheets_df.append(df)

        planilha1, planilha2, planilha3, planilha4, planilha5 = sheets_df
        ticket = str(planilha2.iloc[0]['INTERNAL TICKET NUMBER'])

        if self.session.query(Interceptacao).filter_by(internalTicketNumber=ticket).first():
            raise ValueError(f'Ticket Number {ticket} already exists in the database')
        
        interceptacao = self.session.query(Interceptacao).filter_by(internalTicketNumber=ticket).first()
        if not interceptacao:
            planilha = Planilha(nome=filename, size=file_size)
            self.session.add(planilha)
            self.session.flush()
            interceptacao = Interceptacao(internalTicketNumber=ticket, operacaoId=operacao_id, planilhaId=planilha.id)
            self.session.add(interceptacao)

        hash_numeros, hash_grupos, hash_interceptacao_numeros = {}, {}, {}
        
        try:
            self.process_planilha1(planilha1, ticket, interceptacao, hash_numeros, hash_interceptacao_numeros)
            self.process_planilha4(planilha4, ticket, interceptacao, hash_numeros, hash_interceptacao_numeros)
            self.process_planilha5(planilha5, ticket, interceptacao, hash_numeros, hash_grupos, hash_interceptacao_numeros)
            self.process_planilha2(planilha2, ticket, interceptacao, hash_numeros, hash_interceptacao_numeros)
            self.process_planilha3(planilha3, ticket, interceptacao, hash_numeros, hash_interceptacao_numeros)
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def process_planilha1(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache):
        for _, row in df.iterrows():
            alvo = self.get_or_create_numero(row['ALVO'], ticket, numeros_cache)
            self.get_or_update_interceptacao_numero(alvo, numeros_cache)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache)

            ts_val = self.parse_datetime(row["TIMESTAMP"])
            data_val = self.parse_date(row["DATA"])
            hora_val = self.parse_time(row["HORA"])

            self.session.add(IP(ip=str(row['IP']), versao='NA', timestamp=ts_val, data=data_val, hora=hora_val, numeroId=alvo.id, internalTicketNumber=row['INTERNAL TICKET NUMBER']))

    def process_planilha2(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache):
        for _, row in df.iterrows():
            alvo = self.get_or_create_numero(row['ALVO'], ticket, numeros_cache)
            self.get_or_update_interceptacao_numero(alvo, numeros_cache)
            sender = self.get_or_create_numero(row['SENDER'], ticket, numeros_cache)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache)
            self.get_or_create_interceptacao_numero(sender, interceptacao, row['SENDER'] == row['ALVO'], interceptacao_cache)

            ts_val = self.parse_datetime(row["TIMESTAMP"])
            data_val = self.parse_date(row["DATA"])
            hora_val = self.parse_time(row["HORA"])
        
            recipients = [r.strip() for r in str(row['RECIPIENTS']).split(',')]
            
            if recipients and recipients != ['']:
                for recipient_num in recipients:
                    recipient = self.get_or_create_numero(recipient_num, ticket, numeros_cache)
                    self.get_or_create_interceptacao_numero(
                        recipient,
                        interceptacao,
                        recipient_num == row['ALVO'],
                        interceptacao_cache
                    )

                    mensagem = Mensagem(
                        internalTicketNumber=row['INTERNAL TICKET NUMBER'],
                        messageExternalId=row['MESSAGE ID'],
                        grupoId=str(row['GROUP ID']),
                        remetente=row['SENDER'],
                        remetenteIp=str(row['SENDER IP']),
                        remetenteDispositivo=row['SENDER DEVICE'],
                        remetentePorta=row['SENDER PORT'],
                        tipoMensagem=row['TYPE'],
                        estiloMensagem=row['MESSAGE STYLE'],
                        tamanhoMensagem=row['MESSAGE SYZE'],
                        data=row['DATA'],
                        hora=row['HORA'],
                        timestamp=ts_val,
                        destinatario=recipient_num,
                        numeroId=alvo.id
                    )
                    self.session.add(mensagem)
            else:
                mensagem = Mensagem(
                    internalTicketNumber=row['INTERNAL TICKET NUMBER'],
                    messageExternalId=row['MESSAGE ID'],
                    grupoId=str(row['GROUP ID']),
                    remetente=row['SENDER'],
                    remetenteIp=str(row['SENDER IP']),
                    remetenteDispositivo=row['SENDER DEVICE'],
                    remetentePorta=row['SENDER PORT'],
                    tipoMensagem=row['TYPE'],
                    estiloMensagem=row['MESSAGE STYLE'],
                    tamanhoMensagem=row['MESSAGE SYZE'],
                    data=row['DATA'],
                    hora=row['HORA'],
                    timestamp=ts_val,
                    destinatario=row['RECIPIENTS'],
                    numeroId=alvo.id
                )
                self.session.add(mensagem)

            self.session.add(IP(ip=str(row['SENDER IP']), versao='NA', timestamp=ts_val, data=data_val, hora=hora_val, numeroId=sender.id, internalTicketNumber=row['INTERNAL TICKET NUMBER']))
            
    def process_planilha3(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache):
        for _, row in df.iterrows():
            # Alvo
            alvo = self.get_or_create_numero(row['ALVO'], ticket, numeros_cache)
            self.get_or_update_interceptacao_numero(alvo, numeros_cache)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache)

            # Call creator
            call_creator = self.get_or_create_numero(row['CALL CREATOR'], ticket, numeros_cache)
            is_alvo_creator = (str(row['CALL CREATOR']) == str(row['ALVO']))
            self.get_or_create_interceptacao_numero(call_creator, interceptacao, is_alvo_creator, interceptacao_cache)

            # Parse timestamps
            ts_val = self.parse_datetime(row["TIMESTAMP"])
            data_val = self.parse_date(row["DATA"])
            hora_val = self.parse_time(row["HORA"])

            # Add IP for creator
            self.session.add(IP(
                ip=str(row['IP DO CRIADOR']),
                versao='NA',
                timestamp=ts_val,
                data=data_val,
                hora=hora_val,
                numeroId=call_creator.id,
                internalTicketNumber=row['INTERNAL TICKET NUMBER']
            ))

            # Receptor
            receptor_numero = str(row['RECEPTOR'])
            if receptor_numero and receptor_numero.lower() != 'nan':
                receptor = self.get_or_create_numero(receptor_numero, ticket, numeros_cache)
                is_alvo_receptor = (receptor_numero == str(row['ALVO']))
                self.get_or_create_interceptacao_numero(receptor, interceptacao, is_alvo_receptor, interceptacao_cache)

                self.session.add(IP(
                    ip=str(row['IP DO RECEPTOR']),
                    versao='NA',
                    timestamp=ts_val,
                    data=data_val,
                    hora=hora_val,
                    numeroId=receptor.id,
                    internalTicketNumber=row['INTERNAL TICKET NUMBER']
                ))

            # Ligacao
            ligacao = Ligacao(
                internalTicketNumber=row['INTERNAL TICKET NUMBER'],
                ligacao_external_id=row['CALL ID'],
                criadorLigacao=row['CALL CREATOR'],
                timestamp=ts_val,
                data=row['DATA'],
                hora=row['HORA'],
                tipoLigacao=str(row['TIPO DE MIDIA']),
                criadorIp=str(row['IP DO CRIADOR']),
                criadorPort=str(row['PORTA DO CRIADOR']),
                receptor=row['RECEPTOR'],
                receptorIp=str(row['IP DO RECEPTOR']),
                receptorPort=str(row['PORTA DO RECEPTOR']),
                numeroId=alvo.id,
            )
            self.session.add(ligacao)
            
    def process_planilha4(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache):
        for _, row in df.iterrows():
            alvo = self.get_or_create_numero(row['ALVO'], ticket, numeros_cache)
            self.get_or_update_interceptacao_numero(alvo, numeros_cache)
            contato = self.get_or_create_numero(row['CONTATO'], ticket, numeros_cache)

            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache)
            self.get_or_create_interceptacao_numero(contato, interceptacao, row['CONTATO'] == row['ALVO'], interceptacao_cache)

            if not self.session.query(Contato).filter_by(numeroOrigemId=alvo.id, numeroContatoId=contato.id).first():
                self.session.add(Contato(tipoContato=True, internalTicketNumber=row['INTERNAL TICKET NUMBER'], numeroOrigemId=alvo.id, numeroContatoId=contato.id))

    def process_planilha5(self, df, ticket, interceptacao, numeros_cache, grupos_cache, interceptacao_cache):
        for _, row in df.iterrows():
            alvo = self.get_or_create_numero(row['ALVO'], ticket, numeros_cache)
            self.get_or_update_interceptacao_numero(alvo, numeros_cache)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache)

            group_id = str(row['ID'])
            if group_id not in grupos_cache:
                ts_val = self.parse_datetime(row['CREATION'])
                data_val = self.parse_date(row['DATA LOCAL'])

                grupo = Grupo(
                    internalTicketNumber=row['INTERNAL TICKET NUMBER'],
                    groupExternalId=group_id,
                    criado=ts_val,
                    dataLocal=data_val,
                    descricao=row['DESCRIPTION'],
                    horaLocal=str(row['HORA LOCAL']),
                    tamanho=row['SIZE'],
                    assunto=row['SUBJECT']
                )
                self.session.add(grupo)
                self.session.flush()
                grupos_cache[group_id] = grupo

            if not self.session.query(GrupoNumero).filter_by(grupoId=grupos_cache[group_id].id, numeroId=alvo.id).first():
                self.session.add(GrupoNumero(grupoId=grupos_cache[group_id].id, numeroId=alvo.id))

