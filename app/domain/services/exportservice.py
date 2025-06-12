import csv
import io
import zipfile
from datetime import datetime
from typing import List
from flask import send_file
from app.application.dto.filtrodto import FiltroDTO
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.mensagemservice import MensagemService

class ExportService:
    def __init__(self, suspeito_service: SuspeitoService, mensagem_service: MensagemService):
        self.suspeito_service = suspeito_service
        self.mensagem_service = mensagem_service

    def gerar_csvs(self, filtros: List[FiltroDTO]):
        try:
            output = io.BytesIO()
            with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
                for idx, filtro in enumerate(filtros):
                    suspeitos = self.suspeito_service.buscar_por_filtro(filtro) or []
                    mensagens = self.mensagem_service.buscar_por_filtro(filtro) or []

                    suspeito_csv = io.StringIO()
                    writer1 = csv.writer(suspeito_csv)
                    writer1.writerow(["ID", "Nome", "Apelido", "Números"])

                    for s in suspeitos:
                        numeros = [ns.numero.numero for ns in s.numerosuspeito if ns.numero]
                        writer1.writerow([
                            s.id,
                            s.nome,
                            s.apelido,
                            ";".join(numeros)
                        ])

                    zipf.writestr(f"suspeitos_{idx}.csv", suspeito_csv.getvalue())

                    mensagem_csv = io.StringIO()
                    writer2 = csv.writer(mensagem_csv)
                    writer2.writerow(["ID", "Remetente", "Destinatário", "Tipo", "Data/Hora"])

                    for m in mensagens:
                        writer2.writerow([
                            m.get("id", ""),
                            m.get("remetente", ""),
                            m.get("destinatario", ""),
                            m.get("tipoMensagem", ""),
                            str(m.get("timestamp", ""))
                        ])

                    zipf.writestr(f"mensagens_{idx}.csv", mensagem_csv.getvalue())

            output.seek(0)
            filename = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            return send_file(output, mimetype="application/zip", as_attachment=True, download_name=filename)

        except Exception as e:
            print(f"[ExportService] Erro ao gerar CSVs: {e}")
            raise
