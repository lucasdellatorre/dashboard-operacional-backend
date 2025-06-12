from datetime import datetime
import time 
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
from app.infraestructure.utils.logger import logger
from app.infraestructure.utils.progress_tracker import set_progress

class PlanilhaRepository:
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_all_ordered_by_upload_date(self):
        return self.session.query(Planilha).order_by(Planilha.dataUpload.asc()).all()

    def validate_columns(self, df: pd.DataFrame, required_columns):
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
    def get_or_create_numero(self, numero, cache):
        numero_str = str(numero)
        
        if numero_str in cache:
            return cache[numero_str]
        
        obj = self.session.query(Numero).filter_by(numero=numero_str).first()
        
        if obj is None:
            obj = Numero(numero=numero_str)
            self.session.add(obj)
            cache[numero_str] = obj
        
        else:
            cache[numero_str] = obj

        return cache[numero_str]

    def get_or_create_interceptacao_numero(
            self,
            numero_obj,
            interceptacao,
            is_alvo,
            interceptacao_cache: dict,
            novos: list = None
        ):
            if numero_obj.id is None:
                self.session.flush()

            numero_id = numero_obj.id
            key = f"{numero_id}:{interceptacao.id}"
            if interceptacao_cache.get(key) is not None:
                return

            inter_num = InterceptacaoNumero(
                numeroId=numero_id,
                interceptacaoId=interceptacao.id,
                isAlvo=is_alvo
            )

            if novos is not None:
                novos.append(inter_num)
            else:
                self.session.add(inter_num)

            interceptacao_cache[key] = True

    def get_or_update_interceptacao_numero(
        self,
        numero_obj,
        interceptacao_num_obj_cache: dict
    ):
        if numero_obj.id is None:
            self.session.flush()

        numero_id = numero_obj.id

        if numero_id in interceptacao_num_obj_cache:
            return interceptacao_num_obj_cache[numero_id]

        with self.session.no_autoflush:
            res = self.session.query(InterceptacaoNumero).filter(
                InterceptacaoNumero.numeroId == numero_id,
                InterceptacaoNumero.isAlvo == False
            ).first()

        if res is not None:
            res.isAlvo = True
            self.session.flush()

        interceptacao_num_obj_cache[numero_id] = res
        return res

    def parse_datetime(self, dt_str, fmt="%Y-%m-%d %H:%M:%S"): 
        return datetime.strptime(str(dt_str).replace(" UTC", ""), fmt)

    def parse_date(self, date_str):
        return datetime.strptime(str(date_str)[:10], "%Y-%m-%d").date()

    def parse_time(self, time_str):
        return datetime.strptime(str(time_str), "%H:%M:%S").time() 
    
    def save(self, file_buffer, file_size, filename, operacao_id, job_id=None):
        start_time = time.time()

        sheets_df, row_counts = self._read_sheets(file_buffer)
        total_rows = sum(row_counts.values())
        sheet_order = ["Planilha1", "Planilha4", "Planilha5", "Planilha2", "Planilha3"]
        row_counts = {name: row_counts[name] for name in sheet_order}

        progress_range = (10, 90)
        pesos_planilhas = {
            nome: (row_counts[nome] / total_rows) * (progress_range[1] - progress_range[0])
            for nome in sheet_order
        }

        progresso_acumulado = progress_range[0]

        def make_progress_callback(planilha_nome, peso):
            def update(percentual_local):
                progresso = progresso_acumulado + peso * (percentual_local / 100)
                if job_id:
                    set_progress(job_id, f"Processando ({percentual_local:.0f}%) {planilha_nome}", int(progresso))
            return update

        planilha1, planilha2, planilha3, planilha4, planilha5 = sheets_df

        if job_id:
            set_progress(job_id, "Planilhas carregadas", progress_range[0])

        ticket = str(planilha2.iloc[0]['INTERNAL TICKET NUMBER'])
        numeros_unicos = self._extract_unique_numbers(planilha1, planilha2, planilha3, planilha4, planilha5)

        hash_numeros = self._create_or_get_numeros(numeros_unicos)
        hash_grupos = {}
        hash_interceptacao_numeros = {}

        planilha = Planilha(nome=filename, size=file_size)
        self.session.add(planilha)
        self.session.flush()

        interceptacao = Interceptacao(
            internalTicketNumber=ticket,
            operacaoId=operacao_id,
            planilhaId=planilha.id
        )
        self.session.add(interceptacao)
        self.session.flush()

        for numero, obj in hash_numeros.items():
            if obj.id is None:
                raise RuntimeError(f"Número '{numero}' sem ID mesmo após flush")

        try:
            for nome, df, processor in [
                ("Planilha1", planilha1, self.process_planilha1),
                ("Planilha4", planilha4, self.process_planilha4),
                ("Planilha5", planilha5, self.process_planilha5),
                ("Planilha2", planilha2, self.process_planilha2),
                ("Planilha3", planilha3, self.process_planilha3),
            ]:
                peso = pesos_planilhas[nome]
                callback = make_progress_callback(nome, peso)
                if nome == "Planilha1":
                    processor(df, ticket, interceptacao, hash_numeros, hash_interceptacao_numeros, callback)
                elif nome == "Planilha4":
                    processor(df, ticket, interceptacao, hash_numeros, hash_interceptacao_numeros, callback)
                elif nome == "Planilha5":
                    processor(df, ticket, interceptacao, hash_numeros, hash_grupos, hash_interceptacao_numeros, callback)
                else:
                    processor(df, ticket, interceptacao, hash_numeros, hash_interceptacao_numeros, callback)
                progresso_acumulado += peso
                if job_id:
                    set_progress(job_id, f"Processado {nome}", int(progresso_acumulado))
                    
            if job_id:
                set_progress(job_id, "Commit finalizando", 95)
            self.session.commit()

            if job_id:
                set_progress(job_id, "Concluído", 100)
            logger.info(f"[SUCCESS] Processamento completo em {time.time() - start_time:.2f}s")

        except Exception as e:
            if job_id:
                set_progress(job_id, "Erro ao salvar", 100, erro=True, mensagem=str(e))
            logger.exception(f"[ERROR] Erro ao salvar: {e}")
            self.session.rollback()
            raise


    def _read_sheets(self, file_buffer):
        required_columns = [
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIMESTAMP', 'DATA', 'HORA', 'IP'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'TIMESTAMP', 'DATA', 'HORA', 'MESSAGE ID', 'SENDER', 'RECIPIENTS', 'GROUP ID', 'SENDER IP', 'SENDER PORT', 'SENDER DEVICE', 'TYPE', 'MESSAGE STYLE', 'MESSAGE SYZE'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'CALL ID', 'CALL CREATOR', 'TIMESTAMP', 'DATA', 'HORA', 'TIPO DE MIDIA', 'IP DO CRIADOR', 'PORTA DO CRIADOR', 'RECEPTOR', 'IP DO RECEPTOR', 'PORTA DO RECEPTOR'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'TIPO CONTATO', 'CONTATO'],
            ['INTERNAL TICKET NUMBER', 'ALVO', 'TIPO DE DADO', 'ID', 'CREATION', 'DATA LOCAL', 'HORA LOCAL', 'SIZE', 'DESCRIPTION', 'SUBJECT']
        ]
        sheets_name = ["Planilha1", "Planilha2", "Planilha3", "Planilha4", "Planilha5"]
        sheets_df = []
        row_counts = {}

        with pd.ExcelFile(file_buffer) as xls:
            for idx, sheet_name in enumerate(sheets_name):
                df = pd.read_excel(xls, sheet_name=sheet_name, usecols=required_columns[idx], dtype=str)
                if df.empty:
                    raise ValueError(f'Sheet "{sheet_name}" is empty')
                self.validate_columns(df, required_columns[idx])
                sheets_df.append(df)
                row_counts[sheet_name] = len(df)

        return sheets_df, row_counts

    def _extract_unique_numbers(self, *dfs):
        def extract_column(df, col):
            return df[col].dropna().astype(str).values.tolist()

        def extract_multiple(df, col, sep=","):
            values = []
            for val in df[col].dropna().astype(str).values:
                values.extend([v.strip() for v in val.split(sep) if v.strip()])
            return values

        planilha1, planilha2, planilha3, planilha4, planilha5 = dfs
        return set(
            extract_column(planilha1, "ALVO") +
            extract_column(planilha2, "ALVO") +
            extract_column(planilha2, "SENDER") +
            extract_multiple(planilha2, "RECIPIENTS") +
            extract_column(planilha3, "ALVO") +
            extract_column(planilha3, "CALL CREATOR") +
            extract_column(planilha3, "RECEPTOR") +
            extract_column(planilha4, "ALVO") +
            extract_column(planilha4, "CONTATO") +
            extract_column(planilha5, "ALVO")
        )

    def _create_or_get_numeros(self, numeros):
        existentes = self.session.query(Numero).filter(Numero.numero.in_(numeros)).all()
        hash_numeros = {n.numero: n for n in existentes}
        for numero in numeros:
            if numero not in hash_numeros:
                novo = Numero(numero=numero)
                self.session.add(novo)
                hash_numeros[numero] = novo
        self.session.flush()
        return hash_numeros

    def process_planilha1(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache, update_progress_cb=None):
        ips = []
        hash_update_interceptacao = {}
        novos_interceptacao_numeros = []

        # Renomea colunas para atributos válidos
        df.rename(columns=lambda x: x.strip().upper().replace(" ", "_"), inplace=True)

        df['ALVO'] = df['ALVO'].astype(str)
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'].str.replace(" UTC", ""), format="%Y-%m-%d %H:%M:%S")

        total = len(df)
        progress_interval = max(1, total // 10)

        for idx, row in enumerate(df.itertuples(index=False), start=1):
            try:
                alvo = numeros_cache[row.ALVO]
            except KeyError:
                logger.warning(f"[ERRO] ALVO '{row.ALVO}' não está no cache! Pulando linha {idx}")
                continue

            if alvo.id is None:
                raise ValueError(f"alvo.id ainda é None para {alvo.numero}")

            self.get_or_update_interceptacao_numero(alvo, hash_update_interceptacao)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache, novos_interceptacao_numeros)

            ts_val = row.TIMESTAMP
            internal_ticket = row.INTERNAL_TICKET_NUMBER

            ip = IP(
                ip=str(row.IP),
                versao='NA',
                timestamp=ts_val,
                data=ts_val.date(),
                hora=ts_val.time(),
                numeroId=alvo.id,
                internalTicketNumber=internal_ticket
            )
            ips.append(ip)

            if update_progress_cb and idx % progress_interval == 0:
                percentual = int((idx / total) * 100)
                update_progress_cb(percentual)

        self.session.bulk_save_objects(novos_interceptacao_numeros)
        self.session.bulk_save_objects(ips)

        if update_progress_cb:
            update_progress_cb(100)

    def process_planilha2(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache, update_progress_cb=None):
        df.rename(columns=lambda x: x.strip().upper().replace(" ", "_"), inplace=True)

        novos_interceptacao_numeros = []

        total = len(df)
        progress_interval = max(1, total // 10)

        for idx, row in enumerate(df.itertuples(index=False), start=1):
            alvo = numeros_cache[row.ALVO]
            sender = self.get_or_create_numero(row.SENDER, numeros_cache)

            self.get_or_update_interceptacao_numero(alvo, numeros_cache)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache, novos_interceptacao_numeros)
            self.get_or_create_interceptacao_numero(sender, interceptacao, row.SENDER == row.ALVO, interceptacao_cache, novos_interceptacao_numeros)

            ts_val = self.parse_datetime(row.TIMESTAMP)
            data_val = self.parse_date(row.DATA)
            hora_val = self.parse_time(row.HORA)

            recipients = [r.strip() for r in str(row.RECIPIENTS).split(',')]

            if recipients and recipients != ['']:
                for recipient_num in recipients:
                    recipient = self.get_or_create_numero(recipient_num, numeros_cache)
                    self.get_or_create_interceptacao_numero(recipient, interceptacao, recipient_num == row.ALVO, interceptacao_cache, novos_interceptacao_numeros)

                    def safe_str(val):
                        if pd.isna(val):
                            return None
                        if isinstance(val, str) and val.strip().lower() == 'nan':
                            return None
                        return str(val).strip()

                    group_id = safe_str(row.GROUP_ID)
                    remetente = safe_str(row.SENDER)
                    destinatario = safe_str(recipient_num)

                    mensagem = Mensagem(
                        internalTicketNumber=row.INTERNAL_TICKET_NUMBER,
                        messageExternalId=row.MESSAGE_ID,
                        grupoId=group_id,
                        remetente=remetente,
                        remetenteIp=str(row.SENDER_IP),
                        remetenteDispositivo=row.SENDER_DEVICE,
                        remetentePorta=row.SENDER_PORT,
                        tipoMensagem=row.TYPE,
                        estiloMensagem=row.MESSAGE_STYLE,
                        tamanhoMensagem=row.MESSAGE_SYZE,
                        data=row.DATA,
                        hora=row.HORA,
                        timestamp=ts_val,
                        destinatario=destinatario,
                        numeroId=alvo.id
                    )
                    self.session.add(mensagem)
            else:
                def safe_str(val):
                    if pd.isna(val):
                        return None
                    if isinstance(val, str) and val.strip().lower() == 'nan':
                        return None
                    return str(val).strip()

                group_id = safe_str(row.GROUP_ID)
                remetente = safe_str(row.SENDER)
                destinatario = safe_str(recipient_num)

                mensagem = Mensagem(
                    internalTicketNumber=row.INTERNAL_TICKET_NUMBER,
                    messageExternalId=row.MESSAGE_ID,
                    grupoId=group_id,
                    remetente=remetente,
                    remetenteIp=str(row.SENDER_IP),
                    remetenteDispositivo=row.SENDER_DEVICE,
                    remetentePorta=row.SENDER_PORT,
                    tipoMensagem=row.TYPE,
                    estiloMensagem=row.MESSAGE_STYLE,
                    tamanhoMensagem=row.MESSAGE_SYZE,
                    data=row.DATA,
                    hora=row.HORA,
                    timestamp=ts_val,
                    destinatario=destinatario,
                    numeroId=alvo.id
                )
                self.session.add(mensagem)

            self.session.add(IP(
                ip=str(row.SENDER_IP),
                versao='NA',
                timestamp=ts_val,
                data=data_val,
                hora=hora_val,
                numeroId=sender.id,
                internalTicketNumber=row.INTERNAL_TICKET_NUMBER
            ))

            if update_progress_cb and idx % progress_interval == 0:
                percentual = int((idx / total) * 100)
                update_progress_cb(percentual)

        self.session.bulk_save_objects(novos_interceptacao_numeros)

        if update_progress_cb:
            update_progress_cb(100)

    def process_planilha3(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache, update_progress_cb=None):
        df.rename(columns=lambda x: x.strip().upper().replace(" ", "_"), inplace=True)

        novos_interceptacao_numeros = []
        ips = []
        ligacoes = []

        total = len(df)
        progress_interval = max(1, total // 10)

        for idx, row in enumerate(df.itertuples(index=False), start=1):
            alvo = numeros_cache[row.ALVO]
            self.get_or_update_interceptacao_numero(alvo, numeros_cache)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache, novos_interceptacao_numeros)

            call_creator_numero = row.CALL_CREATOR
            call_creator = self.get_or_create_numero(call_creator_numero, numeros_cache)
            is_alvo_creator = str(call_creator_numero) == str(row.ALVO)
            self.get_or_create_interceptacao_numero(call_creator, interceptacao, is_alvo_creator, interceptacao_cache, novos_interceptacao_numeros)

            ts_val = self.parse_datetime(row.TIMESTAMP)
            data_val = self.parse_date(row.DATA)
            hora_val = self.parse_time(row.HORA)
            internal_ticket = row.INTERNAL_TICKET_NUMBER

            ips.append(IP(
                ip=str(row.IP_DO_CRIADOR),
                versao='NA',
                timestamp=ts_val,
                data=data_val,
                hora=hora_val,
                numeroId=call_creator.id,
                internalTicketNumber=internal_ticket
            ))

            receptor_numero = str(row.RECEPTOR).strip()
            if receptor_numero and receptor_numero.upper() != "NAN":
                receptor = self.get_or_create_numero(receptor_numero, numeros_cache)
                is_alvo_receptor = receptor_numero == str(row.ALVO)
                self.get_or_create_interceptacao_numero(receptor, interceptacao, is_alvo_receptor, interceptacao_cache, novos_interceptacao_numeros)

                ips.append(IP(
                    ip=str(row.IP_DO_RECEPTOR),
                    versao='NA',
                    timestamp=ts_val,
                    data=data_val,
                    hora=hora_val,
                    numeroId=receptor.id,
                    internalTicketNumber=internal_ticket
                ))

            ligacoes.append(Ligacao(
                internalTicketNumber=internal_ticket,
                ligacao_external_id=row.CALL_ID,
                criadorLigacao=row.CALL_CREATOR,
                timestamp=ts_val,
                data=row.DATA,
                hora=row.HORA,
                tipoLigacao=str(row.TIPO_DE_MIDIA),
                criadorIp=str(row.IP_DO_CRIADOR),
                criadorPort=str(row.PORTA_DO_CRIADOR),
                receptor=row.RECEPTOR,
                receptorIp=str(row.IP_DO_RECEPTOR),
                receptorPort=str(row.PORTA_DO_RECEPTOR),
                numeroId=alvo.id
            ))

            if update_progress_cb and idx % progress_interval == 0:
                percentual = int((idx / total) * 100)
                update_progress_cb(percentual)

        self.session.bulk_save_objects(novos_interceptacao_numeros)
        self.session.bulk_save_objects(ips)
        self.session.bulk_save_objects(ligacoes)

        if update_progress_cb:
            update_progress_cb(100)
 
    def process_planilha4(self, df, ticket, interceptacao, numeros_cache, interceptacao_cache, update_progress_cb=None):
        df.rename(columns=lambda x: x.strip().upper().replace(" ", "_"), inplace=True)

        novos_interceptacao_numeros = []
        contatos = []
        hash_update_interceptacao = {}

        total = len(df)
        progress_interval = max(1, total // 10)

        # Garante que todos os números da coluna 'ALVO' estejam no cache
        for val in df['ALVO']:
            val_str = str(val)
            if val_str not in numeros_cache:
                novo = Numero(numero=val_str)
                self.session.add(novo)
                self.session.flush()
                numeros_cache[val_str] = novo

        # Inicializa interceptações para todos os alvos únicos
        hashAlvos = {numeros_cache[str(val)] for val in df['ALVO']}
        for val in hashAlvos:
            self.get_or_update_interceptacao_numero(val, hash_update_interceptacao)
            self.get_or_create_interceptacao_numero(val, interceptacao, True, interceptacao_cache, novos_interceptacao_numeros)

        for idx, row in enumerate(df.itertuples(index=False), start=1):
            alvo = numeros_cache[row.ALVO]
            contato = self.get_or_create_numero(row.CONTATO, numeros_cache)

            self.get_or_update_interceptacao_numero(alvo, hash_update_interceptacao)
            self.get_or_update_interceptacao_numero(contato, hash_update_interceptacao)

            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache, novos_interceptacao_numeros)
            self.get_or_create_interceptacao_numero(contato, interceptacao, row.CONTATO == row.ALVO, interceptacao_cache, novos_interceptacao_numeros)

            if not self.session.query(Contato).filter_by(numeroOrigemId=alvo.id, numeroContatoId=contato.id).first():
                contatos.append(Contato(
                    tipoContato=True,
                    internalTicketNumber = row.INTERNAL_TICKET_NUMBER,
                    numeroOrigemId=alvo.id,
                    numeroContatoId=contato.id
                ))

            if update_progress_cb and idx % progress_interval == 0:
                percentual = int((idx / total) * 100)
                update_progress_cb(percentual)

        self.session.bulk_save_objects(novos_interceptacao_numeros)
        self.session.bulk_save_objects(contatos)

        if update_progress_cb:
            update_progress_cb(100)
            
    def process_planilha5(self, df, ticket, interceptacao, numeros_cache, grupos_cache, interceptacao_cache, update_progress_cb=None):
        df.rename(columns=lambda x: x.strip().upper().replace(" ", "_"), inplace=True)

        novos_interceptacao_numeros = []
        novos_grupos_numeros = []
        hash_update_interceptacao = {}

        total = len(df)
        progress_interval = max(1, total // 10)

        for idx, row in enumerate(df.itertuples(index=False), start=1):
            alvo = numeros_cache[row.ALVO]

            self.get_or_update_interceptacao_numero(alvo, hash_update_interceptacao)
            self.get_or_create_interceptacao_numero(alvo, interceptacao, True, interceptacao_cache, novos_interceptacao_numeros)

            group_external_id = str(row.ID)

            if group_external_id not in grupos_cache:
                ts_val = self.parse_datetime(row.CREATION)
                data_val = self.parse_date(row.DATA_LOCAL)
                hora_local = str(row.HORA_LOCAL)
                internal_ticket = row.INTERNAL_TICKET_NUMBER

                grupo = Grupo(
                    internalTicketNumber=internal_ticket,
                    groupExternalId=group_external_id,
                    criado=ts_val,
                    dataLocal=data_val,
                    descricao=row.DESCRIPTION,
                    horaLocal=hora_local,
                    tamanho=row.SIZE,
                    assunto=row.SUBJECT
                )
                self.session.add(grupo)
                self.session.flush()
                grupos_cache[group_external_id] = grupo

            grupo_id_int = grupos_cache[group_external_id].id
            if not self.session.query(GrupoNumero).filter_by(grupoId=grupo_id_int, numeroId=alvo.id).first():
                novos_grupos_numeros.append(GrupoNumero(grupoId=grupo_id_int, numeroId=alvo.id))

            if update_progress_cb and idx % progress_interval == 0:
                percentual = int((idx / total) * 100)
                update_progress_cb(percentual)

        self.session.bulk_save_objects(novos_interceptacao_numeros)
        self.session.bulk_save_objects(novos_grupos_numeros)

        if update_progress_cb:
            update_progress_cb(100)
